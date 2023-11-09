from multiprocessing import Event, Queue
from typing import Any, List

from app.utils.app_logger import app_logger as log


class QueueWrapper(object):

    def __init__(self, name: str, q: Queue = None, prevent_writes: Event = None):
        self.name = name
        self.q = q or Queue()
        self._prevent_writes = prevent_writes or Event()

    def get(self) -> Any:
        if self.is_drained:
            return 'STOP'
        try:
            self.q.get()
        except:
            log.info("q.get() interrupted")
            return 'STOP'

    def put(self, message: object):
        if self.is_writable:
            self.q.put(message)

    def put_many(self, messages: List[object]):
        for message in messages:
            self.put(message)

    def prevent_writes(self):
        """
            Prevents external writes to the queue
            This is useful for shutting down or dealing with back pressure
        """
        log.info(f"Preventing writes to queue - {self.name}")
        self._prevent_writes.set()

    @property
    def is_writable(self) -> bool:
        """read-only property indicating if the queue is writable"""
        return not self._prevent_writes.is_set()

    @property
    def is_drained(self) -> bool:
        """if the queue is not writable and is empty the queue is draining"""
        return not self.is_writable and self.empty

    @property
    def empty(self) -> bool:
        """read only property indicating if the queue is empty"""
        return self.q.empty()
