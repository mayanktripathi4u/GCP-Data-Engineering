Before we start with the execution of commands, lets maks sure we are authorized and authenticated.

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
5. Verifying the Current Project
To verify that the project has been set correctly, you can run:
```bash
gcloud config get-value project
```