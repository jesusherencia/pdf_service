FROM python:3.12.8

RUN apt-get update
RUN apt-get -y install git
RUN apt-get -y install curl
RUN apt-get -y install iputils-ping
# if datetime issues try using ntp to fix timzeone issues
RUN apt-get -y install ntp

RUN mkdir app

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

ENTRYPOINT ["tail", "-f", "/dev/null"]
#ENTRYPOINT ["/bin/bash", "-c", "chmod -R +x ./scripts/ && source ./scripts/pythonpath.sh && source ./scripts/extra_envs.sh && ./scripts/run_webapp.sh && tail -f /dev/null"]
#CMD ["python", "src/app.py"]
#CMD [ "python3", "-m" , "flask", "--app", "src/app.py", "-p", "8080", "--debug", "run" ]
