FROM python:latest

RUN apt-get update -y
RUN apt-get install python3-pip curl -y
RUN apt-get install build-essential libssl-dev libffi-dev python-dev -y
RUN mkdir configs
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash -
RUN apt install nodejs -y
RUN npm install -g serverless
RUN npm install serverless-python-requirements
RUN npm install serverless-step-functions

RUN mkdir app
WORKDIR /app

COPY . .

RUN rm pyproject.toml

# Define default command.
CMD ["/usr/bin/sls", "deploy"]