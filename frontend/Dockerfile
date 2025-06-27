FROM node:22.14.0

RUN apt-get -y update
RUN apt-get -y install git
RUN apt-get -y install curl
RUN apt-get -y install iputils-ping

WORKDIR /app

# necessary as package.json can modify package-lock.json & node_modules
COPY . .

RUN npm install -g --silent @angular/cli@17.3.0
RUN npm install --silent

ENTRYPOINT ["tail", "-f", "/dev/null"]