# BUilding ETL Pipeline using Dataflow

## Steps
* Input Source --> Cloud Storage
* Transformation --> Apache Beam (Python SDK)
* Sink --> Big Query


## DataFlow Job.
Script: [data_ingestion.py](/GCP-Data-Engineering/ETL-Project/data_ingestion.py)

### Code Explaination
At a high level, this script reads data from a CSV file, processes it, and writes the transformed data to a BigQuery table. 

Let's break down the code step-by-step:
* Imports
  * argparse: Used for parsing command-line arguments.
  * logging: For logging messages, which can help with debugging and monitoring the script.
  * re: Provides support for regular expressions, used here for string manipulation.
  * apache_beam: The main library for building data processing pipelines.
  * PipelineOptions: Used to specify various options for the pipeline execution.
* DataIngestion Class
  * `DataIngestion`: A class that contains methods for processing the input data.
  * `parse_method`: This method takes a string input (a line from the CSV file) and processes it:
    * Removes carriage returns, newlines, and quotes from the string using re.sub.
    * Splits the cleaned string by commas into a list of values.
    * Creates a dictionary by zipping predefined column names (like 'state', 'gender', etc.) with the list of values, returning this as a structured row.
* Main Function
  * `run` function: This function sets up and executes the data processing pipeline.
  * Argument Parsing:
    * `--input`: Specifies the input file path, defaulting to a Google Cloud Storage (GCS) bucket.
    * `--output`: Specifies the output BigQuery table name.
* Pipeline Setup
```bash
    # Parse arguments from the command line
    known_args, pipeline_args = parser.parse_known_args(args=argv)

    # Data Ingestion is a class we built in this script to hold the logic for transofming the file into a BQ table.
    deata_ingestion = DataIngestion()

    # Initiate the pipeline using the pipeline arguments passed in from the command line
    p = beam.Pipeline(options=PipelineOptions(pipeline_args))
```
  * Parses the command-line arguments and initializes an instance of the DataIngestion class.
  * Initializes an Apache Beam pipeline with any additional options passed from the command line.
* Pipeline Operations
```bash
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
```
  * The pipeline consists of a series of transformations:
    * **Read from a File**: Reads the input CSV file from GCS, skipping the header line.
    * **String to BQ Row**: Maps each line from the CSV to a dictionary row using the parse_method.
  * **Write to BQ**: Writes the processed rows to a specified BigQuery table.
    * `schema`: Specifies the schema of the BigQuery table.
    * `created_disposition`: If the table does not exist, it will be created.
    * `write_disposition`: If the table already exists, it will be truncated before writing new data.
* Running the Pipeline
  * `    p.run().wait_until_finish()   `
  * Runs the pipeline and waits for it to finish execution.
* Entry Point
```bash
if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    run()
```
  * Sets the logging level to INFO and calls the run function when the script is executed directly.

## Run the Dataflow JOb

1. Make sure API for BQ, Cloud Storage and Cloud Dataflow services are enabled.
2. Activate the Cloud Shell or Mac Terminal or Windows Powershell.
3. Activate Account with the below command if not already done. If activated in past skip the steps.
```bash
gcloud auth list

gcloud auth login
```
4. List the Project ID with the command
```bash
gcloud config list project
```
5. Run the following command to get the Dataflow Python example from GCP github Repo to local.
```bash
gsutil -m cp -R gs://splc/gsp290/dataflow-python-examples .
```
6. Now set a Project Variable
```bash
export PROJECT="my-project-abc"
export REGION="us-central1
```
7. Create Cloud Storage Bucket.
    * Create a Standard Storage Class bucket
```bash
gsutil mb -c standard -l us-east1 gs://$PROJECT
```
    * Copy files to your Bucket
```bash
gsutil cp gs://spls/gsp290/data_files/usa_names.csv gs://$PROJECT/data_files/

gsutil cp gs://spls/gsp290/data_files/head_usa_names.csv gs://$PROJECT/data_files/
```
8. Create the BigQuert Dataset
```bash
bq nk usnames
```
9. Build a Dataflow Pipeline
    * Build a BigData ETL pipeine with a TextIO source and a BQIO destination to ingest data into BQ.
    * It will do the following
      * Ingest the files from Cloud Storage
      * Convert the lines read to dictionary objects
      * Transform the data which contains the year to a format BQ understands as a date.
      * Output the rows to BQ
    * The Dataflow job for this demo requires Python3.7 or higher.
```bash
docker run -it -e PROJECT=$PROJECT -v $(pwd)/dataflow-python-examples:/dataflow python:3.7 /bin/bash
```
    * Run the command to install apache-beam
```bash
pip install apache-beam[gcp]==2.24.0
```
    * navigate to the path
```bash
cd dataflow/dataflow_python_examples
```
    * Execute the below command
```bash
python data_ingestion.py \
    --project=my-project-abc \
    --job_name='my-dataflow-job-name' \
    --region=us=central1 \
    --runner=DataflowRunner \
    --staging_location=gs://my-project-abc/test \
    --temp_location gs://my-project-abc/test \
    --input 'gs://my-project-abc/data_files/head_usa_names.csv' \
    --output 'usnames.usa_names' \
    --save_main_session \ 
    --service_account_email my-sa-dataflow-runner@myprojectabc.gserviceaccount.com

``` 