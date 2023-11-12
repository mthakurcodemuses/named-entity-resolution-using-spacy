import argparse
import os

from app.data_ingestion.messaging.queue_manager_handler import QueueManagerHandler
from app.data_ingestion.messaging.queue_wrapper import QueueWrapper
from app.data_ingestion.models.post import Post
from app.data_ingestion.persistence.firestore_persistence import persist_no_op, get_database_client, persist
from app.data_ingestion.processor.data_persistor_worker import DataPersistorWorker
from app.data_ingestion.processor.text_processor_worker import TextProcessorWorker
from app.data_ingestion.processor.worker_process_manager import register_shutdown_handlers
from app.data_ingestion.processor.worker_process_manager import start_processes
from app.data_ingestion.shutdown.shutdown_watcher import ShutdownWatcher
from app.data_ingestion.utils.app_constants import INPUT_QUEUE_NAME, OUTPUT_QUEUE_NAME


def main():
    process_count = (os.cpu_count() - 1) or 1
    parser_arguments = [
        ('--iproc_num', {'help': 'Number of Input Queue Workers', 'default': process_count, 'type': int}),
        ('--oproc_num', {'help': 'number of output queue workers', 'default': process_count, 'type': int}),  # noqa
        ('--iport', {'help': 'input queue port cross proc messaging', 'default': 50_000, 'type': int}),  # noqa
        ('--no_persistence', {'help': 'disable database persistence', 'action': 'store_true'}),  # noqa
        ('--agg_cache_size', {'help': 'aggregator cache size', 'default': 25_000, 'type': int}),  # noqa
    ]

    parser = argparse.ArgumentParser()
    for name, args in parser_arguments:
        parser.add_argument(name, **args)

    args = parser.parse_args()

    iproc_num = args.iproc_num
    oproc_num = args.oproc_num
    iport = args.iport
    cache_sz = args.agg_cache_size
    # A tuple containing the db client and method for persisting message
    # For testing, the no_persistence flag allows us to use a null client with a no op function.
    if args.no_persistence:
        persistable = (None, persist_no_op)
    else:
        persistable = (get_database_client(), persist)

    # Setup the input and output queues
    input_queue = QueueWrapper(name=INPUT_QUEUE_NAME)
    output_queue = QueueWrapper(name=OUTPUT_QUEUE_NAME)

    queue_manager_handler = QueueManagerHandler()
    # Register and start the input queue manager for remote connection
    # This allows the front end to put messages on the queue
    queue_manager_handler.register_manager(INPUT_QUEUE_NAME, input_queue)
    input_queue_server = queue_manager_handler.create_queue_manager(iport)
    input_queue_server.start()

    # Start up the worker/saver processes
    text_worker_processes = start_processes(iproc_num, TextProcessorWorker, [input_queue, output_queue, cache_sz])
    data_persistor_worker_processes = start_processes(oproc_num, DataPersistorWorker, [output_queue, *persistable])

    # Set up the shutdown handlers to gracefully shut down the processes
    register_shutdown_handlers([input_queue, output_queue], [text_worker_processes, data_persistor_worker_processes])

    input_queue.put(Post(content="John has $1000 for a new Apple Product that he intends to buy", publication='me'))
    input_queue.put(Post(content="Ben has $1000 for a new Apple Product that he intends to buy", publication='me'))

    with ShutdownWatcher() as watcher:
        watcher.serve_forever()
    exit(0)


if __name__ == "__main__":
    print("Starting ingestor process")
    main()
