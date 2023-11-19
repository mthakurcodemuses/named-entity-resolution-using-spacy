from fastapi import Security, Depends, status, HTTPException, APIRouter
from fastapi.security import APIKeyHeader

from app.data_ingestion.messaging.queue_connnector import QueueConnector
from app.data_ingestion.messaging.queue_wrapper import QueueWrapper
from app.data_ingestion.models.post import Post
from app.data_ingestion.utils.app_logger import app_logger as log

# Use an access token to secure the post/message uri
API_KEY_HEADER = APIKeyHeader(name='access_token', auto_error=False)

queue_connector = QueueConnector()
message_sender_router = APIRouter()

def check_auth_header(api_key_header: str = Security(API_KEY_HEADER)):
    if api_key_header == 'api_free_pass':
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API key provided in the header"
    )


@message_sender_router.post("/post/message", status_code=status.HTTP_201_CREATED)
def post_message(message: Post, queue: QueueWrapper = Depends(queue_connector),
                 authenticated: bool = Depends(check_auth_header)):
    log.info(f"Received message to queue {message}")
    try:
        queue.put(message)
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
