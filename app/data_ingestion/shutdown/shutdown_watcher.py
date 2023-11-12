import signal
import time


class ShutdownWatcher:
    """
    ShutdownWatcher listens for the SIGTERM and SIGINT signals and
    sets the should_continue flag to False when they are received.
    """
    def __init__(self) -> None:
        self.should_continue = True

        for s in [signal.SIGTERM, signal.SIGINT]:
            signal.signal(s, self.exit)
    
    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.exit()

    def serve_forever(self):
        while self.should_continue:
            time.sleep(0.1)

    def exit(self, *args, **kwargs):
        self.should_continue = False
