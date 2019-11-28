## Deploying as an Azure Web App

(Based on tutorial at https://docs.microsoft.com/bs-latn-ba/azure/app-service/containers/tutorial-multi-container-app )

### Prerequisites

* Recent version of Azure command-line tools (```brew update && brew install azure-cli```, or you can run in a docker container to ensure you have the latest version ```docker run -it mcr.microsoft.com/azure-cli```)
* Docker and docker compose (https://docs.docker.com/)
* An account on DockerHub (https://hub.docker.com/signup)  (could alternatively use Azure Container Registry).
* An Azure subscription (https://azure.microsoft.com)

### Create docker image and push to dockerhub

From this directory, do
```
docker build -t <docker_username>/image_labeller:latest -f Dockerfile .
```
Once this is built, login to docker hub and push the image:
```
docker login
docker push <docker_username>/image_labeller:latest
```

### Create Azure resource group and App Service Plan
```
az login
az account set --subscription <subscription_id>
az group create --name <resource_group_name> --location "UK South"
az appservice plan create --name <service_plan_name> --resource-group <resource_group_name> --sku F1 --is-linux
```
For the SKU, "F1" is the free plan (for testing and development), there is also "B1","B2", or "B3" in the "Basic Service Plan" tier, or "S1", "S2", "S3" in the "Standard Service Plan" tier.  See (https://azure.microsoft.com/en-gb/pricing/details/app-service/linux/)[here] for pricing details.

### Create a docker-compose app

Ensure that the `docker-compose.yml` is using an "image" (the one you pushed to dockerhub earlier) rather than a "dockerfile" in the "build" section of your frontend container configuration.
```
 az webapp create --resource-group <resource_group_name> --plan <service_plan_name> --name <app_name> --multicontainer-config-type compose --multicontainer-config-file docker-compose.yml
```
Here the "<app name>" is what will end up in the URL of your app - needs to be globally unique and only contain URL-friendly characters!

### Stop and start, and check status, from the Azure portal.

From the (https://portal.azure.com)[Azure portal] you can click on "App Services" and then navigate to your new app to check on it.  This will also give you the URL for your app (usually https://<app_name>.azurewebsites.net).  Note that it might take several minutes for the app to start the first time as it needs to pull the docker image.  You might be able to see progress by clicking on  "Container settings" on the left sidebar.
