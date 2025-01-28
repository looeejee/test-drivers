# Use a base image that has Python, Java, and Node.js installed
FROM ubuntu:20.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary packages
RUN apt-get update && \
    apt-get install -y python3 python3-pip openjdk-17-jdk maven nodejs npm && \
    apt-get clean

# Set the working directory
WORKDIR /app

COPY . /app

RUN cd /app/node-driver && npm install

RUN cd /app/python-driver && pip3 install -r ./requirements.txt

RUN cd /app/java-driver && mvn clean install

WORKDIR /app
RUN echo '#!/bin/bash\n' \
    'echo "#### PYTHON SCRIPT RUNNING ####"\n' \
    'python3 /app/python-driver/main.py\n' \
    'echo "#### Java SCRIPT RUNNING ####"\n' \
    'java -jar /app/java-driver/target/java-driver-1.0-SNAPSHOT.jar\n' \
    'echo "#### Node SCRIPT RUNNING ####"\n' \
    'node /app/node-driver/index.js' > run_apps.sh && \
    chmod +x run_apps.sh

# Set the entry point to run the shell script
CMD ["./run_apps.sh"]
