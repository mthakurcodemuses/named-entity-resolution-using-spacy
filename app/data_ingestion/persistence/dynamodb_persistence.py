import boto3
from botocore.exceptions import ClientError

from app.data_ingestion.utils.app_logger import app_logger as log

session = boto3.Session()
dynamodb = session.resource("dynamodb")
table_name = os.getenv("CALL_TRANSCRIPTS_TABLE_NAME", "call_transcript")
table = dynamodb.Table(table_name)

def persist(call_transripts: [CallTranscript]):
    try:
        with table.batch_writer() as writer:
            for call_transript in call_transripts:
                writer.put_item(Item=call_transript)
    except ClientError as err:
        logger.error(
            "Couldn't save call transcript into table %s. Here's why: %s: %s",
            table.name,
            err.response["Error"]["Code"],
            err.response["Error"]["Message"],
        )
        raise

def persist_no_op(*args, **kwargs):
    pass