"""
Use Case: Batch Data Processing.
1. Read / Extract data from CSV file available in GCS Bucket.
2. Perform series of transformations to clean, aggregate, format data using Apache Beam Transformations.
3. Write data into BQ Table. (Make sure DataSet exists in BQ; Table will get created if not exists.)

How to Run this...

python 02_Batch_Data_Processing \
 --input gs://dataflow-demo/batch/bulk.csv \
 --output gs://dataflow-demo/output/out.txt \
 --project gcp-hde-prim-dev \
 --region us-central1 \
 --staging_location gs://dataflow-demo/staging \
 --temp_location gs://dataflow-demo/temp \
 --runner DataflowRunner
"""

import argparse
import logging
import apache_beam as beam
import re
from apache_beam.io import ReadFromText
from apache_beam.io import WriteToText
from apache_beam.options.pipeline_options import PipelineOptions

# ParDo class for parallel processing by applying user define transformation
class scrip_val(beam.DoFn):
    def process(self, element):
        try:
            line = element.split('"')
            if line[9] == "BUY":
                tp = line[3] + ',' + line[11].replace(',', '')
            else:
                tp = line[3] + ',-' + line[11].replace(',', '')
            tp = tp.split()
            return tp
        except:
            logging.info("Some error occured.")


# Entry Run Method for triggering pipeline
def run():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input',
        dest='input',
        default="gs://dataflow-demo"
        help="Input the file for processing."
    )
    parser.add_argument(
        '--output',
        dest="output",
        required=True,
        help="Output file to write results to."
    )
    known_args, pipeline_args = parser.parse_known_args()

    # Function to Sun grouped elements
    def sum_groups(word_ones):
        (word, ones) = word_ones
        return word + ',' + str(sum(ones))
    
    # Function to parse and format given input to BQ readable JSON format
    def parse_method(string_input):
        values = re.split(",", re.sub("\r\n", '', re.sub(u'"', '', string_input)))
        row = dict(
            zip(('SYMBOL', 'BUY_SELL_QTY'),
                values)
        )
        return row
    
    # Main Pipeline
    with beam.Pipeline(options=PipelineOptions(pipeline_args)) as p:
        lines = p | "Read" >> ReadFromText(known_args.input, skip_header_lines=1)
        counts = (
            lines
            | "Get Required Tuple" >> beam.ParDo(scrip_val())
            | "PairWithValue" >> beam.Map(lambda x: (x.split(',')[0], int(x.split(',')[1])))
            | "Group By Key" >> beam.GroupByKey()
            | "Sum Group" >> beam.Map(sum_groups)
            | "To String" >> beam.Map(lambda s: str(s))
            | "String to BQ Row" >> beam.Map(lambda s:parse_method(s))
            # | "Format" >> beam.Map(format_result)
            # | "Print" >> beam.Map(print)
            # | "Write" >> WriteToText(known_args.output)
        )

        # Write to BQ Sink
        counts | 'Write to BQ' >> beam.io.Write(
            beam.io.WriteToBigQuery(
                table='batch_data',
                dataset='dataflow_demo',
                project="my-project-abc",
                schema="SYMBOL:STRING, BUY_SELL_QTY:INTEGER",
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE
            )
        )

# Trigger entry function
if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    run()
