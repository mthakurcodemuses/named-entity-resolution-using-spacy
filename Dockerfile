# Use the official Python 3.11 image as a base image
FROM python:3.11-slim-buster

# Set the environment variable PYTHONUNBUFFERED to ensure that Python output is logged
ENV PYTHONUNBUFFERED 1

# Set the optimization level of the Python interpreter
ENV PYTHONOPTIMIZE=2

# Set the working directory in the Docker container
WORKDIR /nlp-using-spacy-app

COPY . .

# Install the Python packages specified in the requirements.txt file
RUN pip install --no-cache-dir -r requirements.txt