# Requirement
- Create a GKE cluster with mllp-adapter, and this mllp-adapter will parse the HL7v2 messages and store it to HL7v2 store in GCP.
- Python Code which will push the HL7 message to mll-adapter for parsing, and once parsed will get stored in HL7v2 store in google cloud healthcare API service.
- mllp-adapter will keep track of all received messages; parsed successful; failed or nack etc.


# Solution
Here is the Terraform and Python code to implement above requirement.

The code provisions the GKE cluster with the MLLP adapter and includes a Python script to push HL7v2 messages for parsing.

## Terraform Code:
1. Provider and Project Setup
   Create a [main.tf](/GCP-Data-Engineering/Health/Lab-1/main.tf) file to define the Google Cloud provider and enable required APIs.

2. Create a GKE Cluster.
   Create a [cluster.tf](/GCP-Data-Engineering/Health/Lab-1/cluster.tf) file.

3. Deploy MLLP Adapter to GKE
   You can use a `kubernetes_manifest.yaml` to deploy the MLLP adapter with configuration pointing to the HL7v2 store. The Terraform code integrates this manifest. [Refer code](/GCP-Data-Engineering/Health/Lab-1/mllp_adapter.tf)

## Python Code for Message Submission
1. Install the required libraries
```bash
pip install google-cloud-healthcare
```
2. Python Script [send_hl7_message.py](/GCP-Data-Engineering/Health/Lab-1/send_hl7_message.py)

## GKE Service for MLLP Adapter
You need to expose the MLLP adapter using a Kubernetes Service:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: mllp-adapter-service
  namespace: mllp-adapter
spec:
  ports:
    - protocol: TCP
      port: 2575
      targetPort: 2575
  selector:
    app: mllp-adapter
```

# Additional Notes:
1. MLLP Adapter Monitoring:
* Use a logging and monitoring solution (e.g., Google Cloud Operations Suite) to track message statuses like "successful", "failed", or "nack".

2. Authentication:
* Ensure the Python script authenticates to GCP using a service account with the roles/healthcare.hl7V2StoreEditor role.

3. Deployment:
* Apply the Terraform code and use kubectl to deploy Kubernetes manifests.


# What is `kubernetes_manifest.yaml`?
The `kubernetes_manifest.yaml` is a Kubernetes configuration file written in YAML format. It defines the desired state of Kubernetes resources (e.g., Deployments, Services, ConfigMaps, etc.) for the application. In this context, it specifies the deployment configuration for the MLLP adapter.

It is not a predefined or universally common file — it must be created and customized for our own use case. Here's an example configuration for the `kubernetes_manifest.yaml` that deploys the MLLP adapter.

[Code](/GCP-Data-Engineering/Health/Lab-1/kubernetes_manifest.yaml)

## What Does This File Contain?
1. Deployment:

* Specifies the application (`mllp-adapter`) to be deployed.
* Includes container information such as the Docker image (`gcr.io/cloud-healthcare-containers/mllp-adapter:latest`).
2. Environment Variables:

* HL7V2_STORE: The HL7v2 store in the Google Cloud Healthcare API where parsed messages will be stored.
3. Ports:

* The MLLP adapter listens on port 2575 for incoming HL7v2 messages.

## Associated Service Configuration
You may also need a Kubernetes Service to expose the MLLP adapter:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: mllp-adapter-service
  namespace: mllp-adapter
spec:
  selector:
    app: mllp-adapter
  ports:
  - protocol: TCP
    port: 2575
    targetPort: 2575
  type: LoadBalancer
```

This configuration:
* Maps external traffic to the MLLP adapter on port 2575.
* Uses a LoadBalancer service type to expose the application outside the cluster.

## Placement of the Manifest File
The `kubernetes_manifest.yaml` file should be placed in a directory where you store Kubernetes configurations for your project. Common practices include:

* Keeping it in a `manifests/` or `kubernetes/` directory in your repository.
* Using version control (e.g., Git) to track changes to the file.

For Terraform, if you're dynamically deploying resources, you can inline the configuration into the Terraform code using `resource "kubernetes_deployment"`, but managing it as a separate file is often preferred for better modularity and collaboration