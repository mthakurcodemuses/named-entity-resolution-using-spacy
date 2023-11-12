import signal
from collections import defaultdict
from multiprocessing import Process

from app.data_ingestion.messaging.queue_wrapper import QueueWrapper
from app.data_ingestion.models.processed_post import ProcessedPost
from app.data_ingestion.utils.app_logger import app_logger as log
from .text_processor import TextProcessor


class TextProcessorWorker(Process):
    """
    DataProcessorWorker is a multiprocessing.Process subclass that
    is responsible for fetching data from the input queue
    and extracting known entities
    """

    def __init__(self, input_queue: QueueWrapper,
                 output_queue: QueueWrapper, cache_size: int = 25_000):
        self.input_queue = input_queue
        self.output_queue = output_queue
        self._cache_size: int = cache_size
        log.debug(f"Cache size: {cache_size}")
        self._count: int = 0
        self.reset_cache()
        super(TextProcessorWorker, self).__init__()

    def shutdown(self, *args):
        log.info("Shutting down the text processor worker")
        self.input_queue.put("STOP")

    def count(self, incr_num: int = None) -> str:
        """
        Count increments the counter by the given value and returns the total
        If no value is given, the current value is returned
        """
        if incr_num is not None:
            self._count += incr_num
        return self._count

    def reset_cache(self):
        self._cache = defaultdict(ProcessedPost)

    def cache(self, msg: ProcessedPost) -> int:
        """
        Cache messages until flush_cache is called
        Returns the number of currently cached values
        """
        log.info(f"Caching the processed message {msg}")
        self._cache[msg.pub_key] += msg
        return self.count(1)

    def flush_cache(self):
        log.info("Flushing cache to database")
        for post in self._cache.values():
            self.output_queue.put_many(post.transform_for_database())
        self.reset_cache()

    def run(self):
        # Register the shutdown handler for this process
        signal.signal(signal.SIGTERM, self.shutdown)
        # Only the worker processes need to use the data processor
        # The text processor uses Spacy for its processing
        # Spacy can take up a lot of memory, depending on the model
        # If we instantiate in the __init__ method, the process that 
        # creates Workers ends up using more memory than needed
        processor = TextProcessor()
        # self.input_queue.get() blocks until a message is available
        # This will repeatedly call get and wait for an object to be pulled from the queue
        # until the get call returns the sentinel 'STOP'
        for msg in iter(self.input_queue.get, 'STOP'):
            log.info(f"Received message {msg} from queue")
            if self.cache(processor.process_message(msg)) == self._cache_size:
                self.flush_cache()
        # Leaving the process with a status code of 0, if all went well
        self.flush_cache()
        exit(0)
