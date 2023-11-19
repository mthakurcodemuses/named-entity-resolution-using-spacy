#!/usr/bin/env bash

# Start the ingest proces in the background
ingestdata --iproc_num $MESSAGE_WRITER_PROCESS_COUNT --oproc_num $MESSAGE_READER_PROCESS_COUNT --no_persistence --agg_cache_size $CACHE_SIZE &
# Start the web server
uvicorn app.data_ingestion.app_web_server:app --port 8000 --host 0.0.0.0 --reload
