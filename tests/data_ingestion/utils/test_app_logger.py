from app.data_ingestion.utils import app_logger


def test_get_app_logger():
    assert app_logger.app_logger
