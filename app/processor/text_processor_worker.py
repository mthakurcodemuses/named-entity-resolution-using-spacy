from multiprocessing import Process
from app.models.processed_post import ProcessedPost
from app.messaging.queue_wrapper import QueueWrapper
import signal

class DataProcessorWorker(Process):
    """
    DataProcessorWorker is a multiprocessing.Process subclass that
    is responsible for fetching data from the input queue
    and extracting known entities
    """
    def __init__(self, input_queue: QueueWrapper, 
                 output_queue: QueueWrapper, cache_size: int = 25_000):
        self.input_queue = input_queue
        self.output_queue = output_queue
        super(DataProcessorWorker, self).__init__()


    def shutdown(self, *args):
        pass

    def count(self, incr_num: int = None) -> str:
        """
        Count increments the counter by the given value and returns the total
        If no value is given, the current value is returned
        """
        return 0
    
    def reset_cache(self):
        pass

    def cache(self, msg: ProcessedPost) -> int:
        """
        Cache messages until flush_cache is called
        Returns the number of currently cached values
        """
        return 0
    
    def flush_cache(self):
        pass

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
            self.output_queue.put(processor.process(msg))
        # Leaving the process with a status code of 0, if all went well
        exit(0)


