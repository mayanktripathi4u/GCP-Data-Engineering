# Complete Python + Flask App in Google Cloud

# Pre-requisite
1. Google Cloud Account.
2. Install Google Cloud Command Line (CLI) on your local working station.
   * Make sure Python version is compitable.
   * Authenticate Cloud Shell (CLI) usign `gcloud init`
3. Docker (Docker Desktop) is installed on your working / local machine.
4. Configure `gcloud` with Docker.
   * Use the command `gcloud auth configure-docker` --> This is to configure Docker to authenticate with google cloud container registry where we are going to upload all our containers. 
5. Install dependencies, for now start with `Flask`, and later as we need will add in `requirements.txt` so that we would have to just run this `.txt` to install all dependencies. 
6. Create below folder structure.
```bash
    |
    |- BACKEND
        |-- app.py
        |-- Dockerfile
        |-- helpers/ --> all helper functions.
        |-- endpoints/ --> to have the logic for all endpoints.
        |-- middleware/ --> some code that is going to be run for all the endpoints. Ex. Authentication.
        |-- config/ --> to save any configuration files.
```

# Steps
1. [Dockerfile](./BACKEND/Dockerfile)
2. [app.py](./BACKEND/app.py)
3. [options_helper.py](./BACKEND/helpers/options_helper.py)
4. [check_api_key.py](./BACKEND/middleware/check_api_key.py)
5. [get_info.py](./BACKEND/endpoints/get_info.py)
6. [SA.json](./BACKEND/config/serviceAccountKey.json)
7. `pip3 freeze > requirements.txt` to create `requirements.txt`.
8. Build Docker Image for Google Cloud Artifact Registery --> `docker build -t us-central1-docker.pkg.dev/gcphde-prim-dev-data/gcp-artifact-repo-maya/backend-image:v1 .`
9. CHeck Docker Images --> `docker images`
10. Push to Artifact Registry --> `docker push us-central1-docker.pkg.dev/gcphde-prim-dev-data/gcp-artifact-repo-maya/backend-image:v1` In case it fails, you may have to run `gcloud auth login`.
11. next to run deployment --> 
```bash
gcloud run deploy backend \
--image us-central1-docker.pkg.dev/gcphde-prim-dev-data/gcp-artifact-repo-maya/backend-image \
--platform managed \
--region us-central1 \
--allow-unauthenticated
```
12. Once deployed successfully, it will provide the Service URL which we could use, however in our case we have defined the acceess based on key, so it will fail. Right approach is to use curl command and call the url with key.
```bash
curl -X POST https://backend-image-<numeric ID>.us-central1.run.app/v1/getInfo \
-H "X-API-KEY:axsdTypoiUYTfsv89**hqiu19&&&" \
-H "Content-Type: application/json"
-d '{"key1": "value-1", "key2": "valie-2"}'
```
13. 

gcloud auth print-access-token | docker login -u oauth2accesstoken --password-stdin https://us-central1-docker.pkg.dev

Log into gcloud: gcloud auth login
Configure docker: gcloud auth configure-docker us-central1-docker.pkg.dev (make sure to specify appropriate region)

you must manually create the Artifact Registry repository before pushing Docker images to it. The repository acts as a storage location for your Docker images, and it needs to exist in your Artifact Registry project before you can push any images into it.

Here’s how you can create a repository in Google Artifact Registry and then push your Docker images:

1. Create an Artifact Registry Repository
To create a repository, you can use the gcloud command:

bash
Copy code
gcloud artifacts repositories create [REPOSITORY_NAME] \
    --repository-format=docker \
    --location=[REGION] \
    --description="Repository for Docker images"
Replace the placeholders:

[REPOSITORY_NAME] – the name of the repository you want to create (e.g., backend).
[REGION] – the region where you want to store the repository (e.g., us-central1).
Example:

bash
Copy code
gcloud artifacts repositories create backend \
    --repository-format=docker \
    --location=us-central1 \
    --description="Docker images for backend service"
This command creates a new Docker-format repository in Artifact Registry in the us-central1 region.

2. Push Docker Image
Once the repository is created, you can push your Docker image using the correct format for the Artifact Registry repository.

Assuming your repository is named backend in the us-central1 region, the full image path would be:

bash
Copy code
us-central1-docker.pkg.dev/gcphde-prim-dev-data/backend/[IMAGE_NAME]
For example, to push the image my-backend-image:

bash
Copy code
docker tag my-backend-image us-central1-docker.pkg.dev/gcphde-prim-dev-data/backend/my-backend-image
docker push us-central1-docker.pkg.dev/gcphde-prim-dev-data/backend/my-backend-image
Replace my-backend-image with the name of your Docker image.

3. Verify the Repository Exists
You can verify that the repository has been created and list all repositories in a region by running:

bash
Copy code
gcloud artifacts repositories list --location=us-central1
This will list all repositories in the us-central1 region, and you should see the one you just created.

4. Permissions Check (if needed)
If you are pushing to the repository and encounter any permission issues, ensure that the account has the necessary permissions. The Artifact Registry Administrator role should grant the permissions needed to push images.

Summary:
Yes, you must create the repository manually before you can push Docker images to it. The steps are:

Create the Artifact Registry repository using gcloud artifacts repositories create.
Tag the Docker image with the correct repository URL.
Push the Docker image to the newly created repository.
Let me know if you need more guidance on any of these steps!
