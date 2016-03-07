# Use debian as base image.
FROM debian

MAINTAINER Giovanni Damiola

# apt upgrade 
RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get --no-install-recommends -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" upgrade

# Install dependencies
RUN DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y git vim sudo ssh curl libxml2-dev libxslt1-dev zlib1g-dev libjpeg-dev
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python python-dev python-pip

# Installing mongodb
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y mongodb

RUN apt-get clean

# Cloning cumo repository
#RUN git clone https://github.com/gdamdam/sumo.git
ADD . /sumo

# Install Sumo's dependencies
RUN pip install -r /sumo/requirements.txt
RUN python /sumo/requirements_nltk.py

EXPOSE 5000

WORKDIR /sumo

ENTRYPOINT service mongodb restart && python sumo_server.py -s 0.0.0.0

