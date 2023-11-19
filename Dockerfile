# Use the official Python 3.9 image as a base image
FROM python:3.9-slim-buster

# Install system dependencies required for building certain Python packages
# This includes the GCC compiler and other necessary tools
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the environment variable PYTHONUNBUFFERED to ensure that Python output is logged
ENV PYTHONUNBUFFERED 1

# Set the optimization level of the Python interpreter
ENV PYTHONOPTIMIZE=2

# Set the working directory in the Docker container
WORKDIR /nlp-using-spacy-app

COPY . .

# Install the Python packages specified in the requirements.txt file
RUN pip install -r requirements.txt

# Download the en_core_web_sm spacy model
RUN python -m spacy download en_core_web_sm

# Install your module
RUN pip install .

# Expose the port that uvicorn listens on
EXPOSE 8000

# Start the uvicorn server
#CMD ["uvicorn", "app.data_ingestion.app_web_server:app", "--port", "8000", "--host", "0.0.0.0", "--reload"]
#CMD ["sh", "-c",  "ingestdata --iproc_num $MESSAGE_WRITER_PROCESS_COUNT --oproc_num $MESSAGE_READER_PROCESS_COUNT --no_persistence --agg_cache_size $CACHE_SIZE"]
ENTRYPOINT ["./entrypoint.sh"]