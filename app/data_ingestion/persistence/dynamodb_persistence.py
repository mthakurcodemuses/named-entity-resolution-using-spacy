import boto3
from botocore.exceptions import ClientError

from app.data_ingestion.models.call_transcript import CallTranscript
from app.data_ingestion.utils.app_logger import app_logger as log


class CallTranscriptsDynamoDBPersistence:

    def __init__(self):
        session = boto3.Session()
        dynamodb = session.resource("dynamodb")
        self.table = dynamodb.Table("call_transcripts")

    def persist(self, call_transcripts: [CallTranscript]):
        try:
            log.info(f"Saving {len(call_transcripts)} call transcripts into table %s", self.table.name)
            with self.table.batch_writer() as writer:
                for call_transcript in call_transcripts:
                    writer.put_item(Item=call_transcript)
        except ClientError as err:
            log.error(
                "Couldn't save call transcript into table %s. Here's why: %s: %s",
                self.table.name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise

    def persist_no_op(self, *args, **kwargs):
        pass