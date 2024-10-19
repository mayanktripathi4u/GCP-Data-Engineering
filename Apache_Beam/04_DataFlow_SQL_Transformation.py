"""
Use Case: Batch Data Processing.
1. 

How to Run this...

python 04_DataFlow_SQL_Transformation \
 --input gs://dataflow-demo/batch/beam_sql.csv \
 --output gs://dataflow-demo/output/out.txt \
 --project gcp-hde-prim-dev \
 --region us-central1 \
 --staging_location gs://dataflow-demo/staging \
 --temp_location gs://dataflow-demo/temp \
 --save_main_session True
"""

import argparse
import logging
import apache_beam as beam
import re
from apache_beam.io import ReadFromText
from apache_beam.io import WriteToText
from apache_beam.transforms.sql import SqlTransform
from apache_beam.options.pipeline_options import PipelineOptions

# ParDo class for parallel processing by applying user define transformation
class convert_row(beam.DoFn):
    def process(self, element):
        try:
            line = element.split(',')
            tp = line[0], ',' + line[1] + ',' + line[2] + line[3]
            tp = tp.replace('"', '')
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

    qry = '''
    SELECT Symbol, SUM(QuantityTraded) as QuantityTraded
        FROM (
            SELECT  Symbol,
                    CASE WHEN BuyOrSell = 'BUY' THEN CAST(replace(QuantityTraded, ',', '') as int64)
                    else -cast(replace(QuantityTraded, ',', '') as int64) end as QuantityTraded
            FROM PCOLLECTION
        )
        GROUP BY 1
    '''
    
    # Main Pipeline
    with beam.Pipeline(options=PipelineOptions(pipeline_args)) as p:
        lines = p | "Read" >> ReadFromText(known_args.input, skip_header_lines=1)
        counts = (
            lines
            # Read data from a file and format it as readable lines of strings
            | "Formatted rows of strings" >> beam.ParDo(convert_row())
            # Convert collection of strings to beam SQL Rows
            | "Convert as table rows" >> beam.Map(lambda x: beam.Row(Symbol = str(x.split(','), BuyOrSell = str(x.split(',')[1], QuantityTraded = str(x.split(',')[2])))))
            # Applying sql transformation using zetasql
            | "GroupSum" >> SqlTransform(query=qry, dialect='zetasql')
            # Convert resultant rows to BQ readable dict format rows
            | "Convert to BQ readable Dict" >> beam.Map(lambda row: row._asdict())
            # | "Print" >> beam.Map(print)
            # | "Write" >> WriteToText(known_args.output)
        )

        # Write to BQ Sink
        counts | 'Write to BQ' >> beam.io.Write(
            beam.io.WriteToBigQuery(
                table='batch_data',
                dataset='dataflow_demo',
                project="my-project-abc",
                schema="SYMBOL:STRING,QuantityTraded:INTEGER",
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE
            )
        )

# Trigger entry function
if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    run()
