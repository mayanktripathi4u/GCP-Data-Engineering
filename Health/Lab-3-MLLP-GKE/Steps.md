Working on a POC to process `HL7 v2` messages using an `MLLP adapter` in a `GKE cluster`, I'll be using Python script to generate HL7 messages and send them via MLLP. 

[Refer Google Docs](https://cloud.google.com/healthcare-api/docs/how-tos/mllp-adapter)
[About MLLP](https://cloud.google.com/healthcare-api/docs/concepts/hl7v2#mllp_and_the_google_cloud_platform_mllp_adapter)



## Step 1: Install Required Libraries
First, we need to install the required Python libraries. You can do this using pip:

```bash
pip install hl7
```

## Step 2: Generate HL7 Messages
Use the hl7 library to generate HL7 messages.

<!-- 
## Step 3: Send HL7 Messages via Socket
Use the following code to send the HL7 message to an MLLP server:

Ensure you have an MLLP server running on `localhost` at port `2575`. -->
## Step 3: Create Resources
Create a Healthcare Dataset: If you haven't already created a Cloud Healthcare API dataset, create a dataset by completing the following steps:

```bash
gcloud healthcare datasets create poc_hl7v2_store \
    --location=us-central1
```

Creating a Pub/Sub topic and subscription: To receive notifications when messages are created or ingested, you need to configure a Pub/Sub topic with your HL7v2 store

```bash
gcloud pubsub topics create projects/gcphde-prim-dev-data/topics/poc_hl7_topic

gcloud pubsub subscriptions create poc_hl7_subscription \
    --topic=projects/gcphde-prim-dev-data/topics/poc_hl7_topic
```
Creating an HL7v2 store configured with a Pub/Sub topic: Create an HL7v2 store and configure it with a Pub/Sub topic. 

```bash
curl -X POST \
    --data "{
      'notificationConfigs': [
        {
          'pubsubTopic': 'projects/gcphde-prim-dev-data/topics/poc_hl7_topic',
          'filter': ''
        }
      ]
    }" \
    -H "Authorization: Bearer $(gcloud auth application-default print-access-token)" \
    -H "Content-Type: application/json; charset=utf-8" \
    "https://healthcare.googleapis.com/v1/projects/gcphde-prim-dev-data/locations/us-central1/datasets/poc_hl7v2_store/hl7V2Stores?hl7V2StoreId=HL7V2_STORE_ID"
```

Pull Docker Pre-Built Image
```bash
docker pull gcr.io/cloud-healthcare-containers/mllp-adapter:latest
```

To test the adapter locally as a receiver: On the machine where you pulled the pre-built Docker image, run the following command:

```bash
docker run \
    --network=host \
    -v ~/.config:/root/.config \
    gcr.io/cloud-healthcare-containers/mllp-adapter \
    /usr/mllp_adapter/mllp_adapter \
    --hl7_v2_project_id=gcphde-prim-dev-data \
    --hl7_v2_location_id=us-central1 \
    --hl7_v2_dataset_id=poc_hl7v2_store \
    --hl7_v2_store_id=HL7V2_STORE_ID \
    --export_stats=false \
    --receiver_ip=0.0.0.0 \
    --port=2575 \
    --api_addr_prefix=https://healthcare.googleapis.com:443/v1 \
    --logtostderr
```


## Step 4: Configuring the MLLP Adapter
* Make sure to enable the necessary APIs: 
    * Cloud Healthcare API, 
    * Google Kubernetes Engine (GKE), 
    * Container Registry, and 
    * Pub/Sub.
* Create a Docker Repository
  * Create a Docker repository in Google Container Registry (GCR) to store the MLLP adapter image
* Build the MLLP Adapter Image
* 



------------------------

https://cloud.google.com/healthcare-api/docs/how-tos/mllp-adapter#deploying_the_mllp_adapter_to_google_kubernetes_engine 

```bash
# To create the service account
gcloud iam service-accounts create poc-mllp-gke-sa

# grant each role to the service account
gcloud projects add-iam-policy-binding gcphde-prim-dev-data \
  --member=serviceAccount:poc-mllp-gke-sa@gcphde-prim-dev-data.iam.gserviceaccount.com \
  --role=roles/pubsub.subscriber

gcloud projects add-iam-policy-binding gcphde-prim-dev-data \
  --member=serviceAccount:poc-mllp-gke-sa@gcphde-prim-dev-data.iam.gserviceaccount.com \
  --role=roles/healthcare.hl7V2Ingest

gcloud projects add-iam-policy-binding gcphde-prim-dev-data \
  --member=serviceAccount:poc-mllp-gke-sa@gcphde-prim-dev-data.iam.gserviceaccount.com \
  --role=roles/monitoring.metricWriter

# Create Cluster
gcloud container clusters create mllp-adapter \
    --zone=us-central1-a \
    --service-account poc-mllp-gke-sa@gcphde-prim-dev-data.iam.gserviceaccount.com

```

If you got error 
```bash
CRITICAL: ACTION REQUIRED: gke-gcloud-auth-plugin, which is needed for continued use of kubectl, was not found or is not executable. Install gke-gcloud-auth-plugin for use with kubectl by following https://cloud.google.com/kubernetes-engine/docs/how-to/cluster-access-for-kubectl#install_plugin
```
It looks like you need to install the `gke-gcloud-auth-plugin` to continue using `kubectl` with your GKE cluster. Here's how you can install it:

### Installation Steps

1. **Open a Terminal or Command Prompt**:
   - Ensure you have the Google Cloud SDK installed.

2. **Install the Plugin**:
   - Run the following command to install the `gke-gcloud-auth-plugin`:
```sh
gcloud components install gke-gcloud-auth-plugin
```

3. **Verify the Installation**:
   - Check if the plugin was installed successfully by running:
```sh
gke-gcloud-auth-plugin --version
```
   - If the installation was successful, you should see the version number of the plugin.

4. **Configure kubectl**:
   - Update your `kubectl` configuration to use the plugin:
```sh
gcloud container clusters get-credentials CLUSTER_NAME --region=COMPUTE_REGION
```

By following these steps, you should be able to resolve the error and continue using `kubectl` with your GKE cluster.



After creating the cluster, GKE creates three Compute Engine VM instances. You can verify this by listing the instances with the following command:

```bash
gcloud compute instances list
```

**Configuring the deployment**

When deploying an application to GKE, you define properties of the deployment using a deployment manifest file, which is typically a YAML file. 

Open a separate terminal.

Using a text editor, create a deployment manifest file called `mllp_adapter.yaml`.
To make the MLLP adapter accessible to applications outside of the cluster (such as a care center), you must configure an internal load balancer.

Deploying the deployment
To deploy the adapter to a GKE cluster, in the directory containing the mllp_adapter.yaml deployment manifest file, run the following command:

```bash
kubectl apply -f mllp_adapter.yaml
```