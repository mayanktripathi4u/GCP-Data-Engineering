"""
Use Case: Stream Data Processing.
1. Publish message at every 1 Min time interval to Pub/Sub topic using Cloud Scheduler.
2. Read / Extract message from Pub/Sub Topic into Dataflow pipeline.
3. Append arrival timestamp, numeric key to each message received from Pub/Sub topic.
4. Group messages based on fixed time window time duration (2 min in this case) and write the data to BQ

How to Run this...

python 03_Stream_Data_Processing.py
 --project=my-gcp-project-abc \
 --region=us-central1 \
 --input_topic=projects/my-gcp-project-abc/stream_dataflow_topic \
 --output_path= gs://dataflow-demo/output \
 --runner=DataflowRunner \
 --window_size=2 \
 --num_shards=2 \
 --temp_location=gs://dataflow_demo_19/temp
"""

import argparse
import logging
import apache_beam as beam
from apache_beam import DoFn, GroupByKey, io, ParDo, Pipeline, PTransform, WindowInto, WithKeys
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.transforms.window import FixedWindows
from datetime import datetime
import random

class GroupMessagesByFixedWindows(PTransform):
    def __init__(self, window_size, num_shards=5):
        self.window_size = int(window_size * 60)
        self.sum_shards = num_shards

    def expand(self, pcoll):
        return (
            pcoll
            #Bind wondow info to each element using element timestamp for publish time
            | "Window into fixed interval" >> WindowInto(FixedWindow(self.window_size))
            | "Add timestamp to windowed elements" >> ParDo(AddTimestamp())
            # Assign a random key to each window elementbased on the number of shard
            | "Add Key" >> WithKeys(lambda _:random.randint(0, self.num_shards - 1))
            # Group windowed elements by Key
            | "Group By Key " >> GroupByKey()
        )

class AddTimestamp(DoFn):
    def process(self, element, publish_time=DoFn.TimestampParam):
        yield(
            element.decode("utf-8"),
            datetime.utcfromtimestamp(float(publish_time)).strftime(
                "%Y-%m-%d %H:%M:%S.%f"
            ),
        )

# Function to parse and format given input to BQ readable Dict format
def parse_method(string_input):
    row = {'bathc_num':string_input[0], 'message':string_input[1][0][0], 'send_time':string_input[1][0][1]}
    return row


def run(input_topic, putput_topic, window_size = 1.0, num_shards = 5, pipeline_agrs=None):
    # Set 'save_maiN_session' to True so DoFn can access globally imported modules 
    pipeline_options = PipelineOptions(
        pipeline_agrs, streaming = True, save_main_session = True
    )
    
    # Main Pipeline
    with Pipeline(options=pipeline_options) as p:
        (
            p
            #  Reading data from Pub/Sub Topic
            | "Read from Pub/Sub" >> io.ReadFromPubSub(topic=input_topic)
            | "Window into" >> GroupMessagesByFixedWindows(window_size, num_shards)
            | "Tuple to BQ Row" >> beam.Map(lambda s: parse_method(s))
            | "Write to BQ" >> beam.io.Write(
                beam.io.WriteToBigQuery(
                    table='stream_data',
                    dataset='my-bq-dataset',
                    project='my-gc-project',
                    schema='batch_num:STRING,message:STRING,send_time:TIMESTAMP',
                    create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                    write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
                )
            )
        )

# Trigger entry function
if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input_topic',
        help="The Cloud Pub/Sub topic to read from,"
        '"projects/topics/".',
    )
    parser.add_argument(
        '--window_size',
        type=float,
        default=1.0,
        help="Output file's window size in minutes."
    )
    parser.add_argument(
        "--output_path",
        help="Path of the output GCS file including the prefix.",
    )
    parser.add_argument(
        "--num_shards",
        type=int,
        default=5,
        help="Number of shards to use when writing windowed elements to GCS.",
    )
    known_args, pipeline_args = parser.parse_known_args()

    run(
        known_args.input_topic,
        known_args.output_path,
        known_args.window_size,
        known_args.num_shards,
        pipeline_agrs=pipeline_args
    )
