from collections import Counter

import spacy

from app.data_ingestion.models.call_transcript import CallTranscript
from app.data_ingestion.models.post import Post
from app.data_ingestion.models.processed_post import ProcessedPost
from app.data_ingestion.utils.app_constants import EXCLUDED_ENTITIES_SPACY
from app.data_ingestion.utils.app_logger import app_logger as log


class TextProcessor:

    def __init__(self):
        log.info('Loading spacy model...')
        self.nlp = spacy.load('en_core_web_sm')
        log.info('Spacy model loaded.')
        self.excluded_entities = EXCLUDED_ENTITIES_SPACY

    def get_entities_count(self, spacy_document) -> Counter:
        """
        Extracts entities from a document and returns a Counter object
        :param nlp_document: an NLP document
        :return: Counter object
        """
        entities = [entity.text.lower() for entity in spacy_document.ents if entity.label_ not in self.excluded_entities]
        return Counter(entities)

    def get_entities(self, text:str):
        log.info(f"Processing text to extract entities: {text} ")
        processed_document = self.nlp(text)
        return {"entities": self.get_entities_count(processed_document)}

    def process_message(self, post: Post) -> ProcessedPost:
        log.info(f"Processing Post: {post}")
        return ProcessedPost(
            **{
                **post.dict(),
                **self.get_entities(post.content)
            }
        )

    def process_transcript(self, transcript: str) -> CallTranscript:
        log.info(f"Processing Transcript: {transcript}")

        return ProcessedPost(
            **{
                **self.get_entities(transcript)
            }
        )