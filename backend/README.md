# Pdf editor web service

The idea is to have a python app to edit pdf files.
This could be deployed in a docker container, so anyone can deploy and use it in local environment.

# Swagger

By using FastAPI we get swagger-ui by default

- <url>/docs

a link to download an OpenAPI file is shown in the page

## To run docker

- Build image :
> docker build -t <image_name> .
- Start container :
> docker run -d --name <container_name> -v ${PWD}:/app -p 8000:8000 <image_name>