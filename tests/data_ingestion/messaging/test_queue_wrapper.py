import pytest
from app.data_ingestion.messaging.queue_wrapper import QueueWrapper
from multiprocessing import Queue
from unittest.mock import MagicMock


@pytest.fixture(scope='function')
def queue_wrapper():
    return QueueWrapper('test_queue', q=Queue())


def test_empty(queue_wrapper):
    assert queue_wrapper.q.qsize() == 0
    assert queue_wrapper.empty
    queue_wrapper.put('message')
    assert queue_wrapper.q.qsize() == 1
    assert not queue_wrapper.empty


def test_get_message(queue_wrapper):
    queue_wrapper.put('message1')
    queue_wrapper.put('message2')
    assert queue_wrapper.get() == 'message1'
    assert queue_wrapper.get() == 'message2'
    assert queue_wrapper.empty


def test_get_with_error_returns_stop(queue_wrapper):
    queue_wrapper.q.get == MagicMock(side_effect=Exception('failed'))
    assert queue_wrapper.get() == 'STOP'


def test_queue_draining(queue_wrapper):
    assert queue_wrapper.is_writable
    assert queue_wrapper.empty
    queue_wrapper.prevent_writes()
    assert not queue_wrapper.is_writable
    assert queue_wrapper.is_drained
