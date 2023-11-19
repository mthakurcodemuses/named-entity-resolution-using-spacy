from .queue_manager import QueueManager
from .queue_wrapper import QueueWrapper


class QueueManagerHandler:

    def register_manager(self, name: str, queue: QueueWrapper = None):
        if queue:
            QueueManager.register(name, callable=lambda: queue)
        else:
            QueueManager.register(name)

    def create_queue_manager(self, port: int) -> QueueManager:
        """
            Binds to 127.0.0.1 on the given port
            Using localhost on at least Debian systems results in extremely slow put() class
        """
        print("Creating QueueManager on port {}".format(port))
        return QueueManager(address=('127.0.0.1', port), authkey=b'document_ingest_queue')
