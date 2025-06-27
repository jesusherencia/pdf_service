# Frontend application for pdf editor

This is the front component of the pdf editor app.
It comunicates through rest api published by backend component.

## To run docker

- Build image :
> docker build -t <image_name> .
- Start container :
> docker run -d --name <container_name> -v ${PWD}:/app -p 8080:8080 <image_name>