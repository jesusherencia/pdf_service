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

## To run webapp

- Run webapp python:
From root folder: 
> python -m web.webapp

## Action Params

For "/pdf_file/webactions" endpoint:

- SHRINK & ROTATE

```json
{
  "file_id": "1772ed86-4810-4a85-99b4-20f7a77a457c",
  "webactions": [
    {
      "type": "SHRINK",
      "params": {
        "quality": 50,
        "dpi": 150
      }
    },
    {
      "type": "ROTATE",
      "params": {
        "rotate_degree": 90
      }
    }
  ]
}
```