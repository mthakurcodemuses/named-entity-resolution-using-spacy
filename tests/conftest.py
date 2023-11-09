import pytest


@pytest.fixture(scope="function", autouse=True)
def logger_teardown(request):
    def teardown_function():
        """Remove handlers from all loggers"""
        import logging
        loggers = [logging.getLogger()] + \
                  list(logging.Logger.manager.loggerDict.values())
        for logger in loggers:
            handlers = getattr(logger, 'handlers', [])
            for handler in handlers:
                logger.removeHandler(handler)

    request.addfinalizer(teardown_function)
