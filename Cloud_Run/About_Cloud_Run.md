# Cloud Run

# Cloud Run Service
Mainly for continuously running apps like website.

# Cloud Run Job
Manily for job which initiates and terminates once the job is completed.

## Demo
1. [Demo-1](./CloudRun_Job/Demo-1/)
    * Python script which extract data and load to GCS bucket
    * Will build container image for this task
    * Will push image to artifact registry
    * Deploy to Cloud Run as Job
    * Test Job

2. 