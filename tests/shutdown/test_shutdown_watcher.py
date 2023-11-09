import pytest
from app.shutdown.shutdown_watcher import ShutdownWatcher
import os
import time
import sched
import signal
from unittest.mock import MagicMock

@pytest.fixture
def watcher():
    return ShutdownWatcher()

@pytest.mark.parametrize('sig', [signal.SIGINT, signal.SIGTERM])
def test_shutdown_watcher(watcher, sig):
    assert watcher.should_continue

    s = sched.scheduler(time.time, time.sleep)
    # Schedule the signal to be sent 0.2 seconds after scheduler.run is called
    s.enter(0.1, 1, lambda: os.kill(os.getpid(), sig))

    with watcher as w:
        s.run()
        w.serve_forever()

    assert not watcher.should_continue