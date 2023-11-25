import signal
from multiprocessing import Process

from app.data_ingestion.messaging.queue_wrapper import QueueWrapper
from app.data_ingestion.utils.app_logger import app_logger as log


class DataPersistorWorker(Process):
    """
    DataPersistorWorker is a multiprocessing.Process subclass that
    is responsible for fetching data from the input queue
    and persisting it to the database
    """

    def __init__(self, queue: QueueWrapper, db_client, persistence_fn_name):
        assert callable(persistence_fn_name)
        self.queue = queue
        self.db_client = db_client
        self.persistence_fn = persistence_fn_name
        super(DataPersistorWorker, self).__init__()

    def shutdown(self, *args):
        log.info("Shutting down the DataPersistor Worker")
        self.queue.put("STOP")

    def run(self):
        signal.signal(signal.SIGTERM, self.shutdown)
        for msg in iter(self.queue.get, 'STOP'):
            log.info(f"Saving extracted entities in the database for message: {msg}")
            persistence_fn = getattr(self.db_client, self.persistence_fn)
            log.info(f"Persistence Function: {persistence_fn}")
            persistence_fn(*msg)
            self.db_client.persist(*msg)
        exit(0)
