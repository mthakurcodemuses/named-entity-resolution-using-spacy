import os
import signal
from multiprocessing import Process
from typing import List
import atexit

from app.data_ingestion.messaging.queue_wrapper import QueueWrapper
from app.data_ingestion.utils.app_logger import app_logger as log


def start_processes(process_count: int, process: Process, process_args: List[object]) -> List[Process]:
    """
    Instantiates and starts the given process
    and returns the process handles
    """
    log.info(f"Initializing {process_count} worker processes and process args: {process_args}")
    process_handles = [process(*process_args) for _ in range(process_count)]
    for process_handle in process_handles:
        process_handle.start()
    return process_handles


def shutdown_processes(queue_wrapper: QueueWrapper, processes: List[Process]):
    """
    Shuts down the given processes using the following steps
    1. Disable writes to the given QueueWrapper
    2. Send SIGTERM signals to each of the given processes
    3. Calls join on the procs, blocking until they complete
    :return:
    """
    queue_wrapper.prevent_writes()
    log.info(f"Sending SIGTERM to processes")
    [os.kill(process.pid, signal.SIGTERM) for process in processes]
    log.info("Joining Processes")
    [process.join for process in processes]


def register_shutdown_handlers(queues, processes):
    """
    Creates shutdown handlers to be kicked off on exit
    :param queues:
    :param processes:
    :return:
    """

    def shutdown_gracefully():
        log.info("Shutting down gracefully")
        for args in zip(queues, processes):
            shutdown_processes(*args)
    atexit.register(shutdown_gracefully)
