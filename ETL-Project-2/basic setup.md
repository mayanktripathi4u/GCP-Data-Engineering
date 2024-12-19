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
6. To set the Project, if not in the desired project.
```bash
gcloud config set project budgetdatabase-395201
```
Make sure to update the **Quota Project for Application Default Credentials**.
To update the quota project for your Application Default Credentials, you can use the following command:
```bash
gcloud auth application-default set-quota-project budgetdatabase-395201
```
7. 