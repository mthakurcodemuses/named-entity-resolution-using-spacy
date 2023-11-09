from multiprocessing import Process

class DataPersistorWorker(Process):
    """
    DataPersistorWorker is a multiprocessing.Process subclass that
    is responsible for fetching data from the input queue
    and persisting it to the database
    """