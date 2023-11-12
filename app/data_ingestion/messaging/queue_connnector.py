from app.data_ingestion.messaging.queue_manager_handler import QueueManagerHandler
from app.data_ingestion.utils.app_constants import INPUT_QUEUE_NAME


class QueueConnector:
    """
    This class is used to manage the connection to the input queue
    The queue manager requires a call to .connect() to establish a connection
    By reusing connections we can better manage our network resources
    """

    def __init__(self):
        queue_manager_handler = QueueManagerHandler()
        queue_manager_handler.register_manager(INPUT_QUEUE_NAME)
        self.queue_manager = queue_manager_handler.create_queue_manager(5000)
        self.input_queue = None

    def __call__(self):
        """Returns a connected input queue manager or raises an error"""
        if self.input_queue:
            return self.input_queue

        try:
            self.input_queue = self.queue_manager.input_queue()
            return self.input_queue
        except AssertionError as ae:
            if ae.args == ('server not yet started',):
                try:
                    self.queue_manager.connect()
                except ConnectionRefusedError:
                    raise

                return self()
        except:
            raise
