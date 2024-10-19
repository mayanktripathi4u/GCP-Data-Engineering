import argparse
import logging
import re
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import os

class DataIngestion:
    def parse_method(self, string_input):
        # dtrip out carriage return newline and quote char.
        values = re.split(",", re.sub('\r\n', '', re.sub('"', '', string_input)))
        row = dict(
            zip(('state', 'gender', 'year', 'name', 'number', 'created_date'), values)
        )
        return row
    
def run(argv = None):
    # The main function which creates the pipeline and runs it.

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input',
        dest='input',
        required=False,
        help='Input file to read. This can be a local file or a file in GCS Bucket',
        default="gs://my-gcs-bucket/head_usa_names.csv"
    )
    parser.add_argument(
        '--output',
        dest='output',
        required=False,
        help='Output BQ Table to write results to.',
        default='lake.usa_names'
    )

    # Parse arguments from the command line
    known_args, pipeline_args = parser.parse_known_args(args=argv)

    # Data Ingestion is a class we built in this script to hold the logic for transofming the file into a BQ table.
    deata_ingestion = DataIngestion()

    # Initiate the pipeline using the pipeline arguments passed in from the command line
    p = beam.Pipeline(options=PipelineOptions(pipeline_args))

    (
        p
        | 'Read from a File' >> beam.io.ReadFromText(known_args.input, skip_header_lines = 1)
        | 'String to BQ Row' >> beam.Map(lambda s: deata_ingestion.parse_method(s))
        | 'Write to BQ' >> beam.io.Write(
            beam.io.BigQuerySink(
                known_args.output,
                schema = 'state:STRING,gender:STRING,year:STRING,name:STRING,number:STRING,created_date:STRING',
                created_disposition = beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                write_disposition = beam.io.BigQueryDisposition.WRITE_TRUNCATE
            )
        )
    )
    p.run().wait_until_finish()

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    run()

    