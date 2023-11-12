import logging
from collections import Counter
from typing import List, Tuple, Dict
from app.data_ingestion.utils.app_logger import app_logger as log

from pydantic import BaseModel


class ProcessedPost(BaseModel):
    publication: str = None  # Not-required on creation
    entities: Counter = Counter()
    article_count: int = 0

    @property
    def pub_key(self) -> str:
        return self.publication.strip().lower()

    def _transform(self, top_n: int) -> Tuple[str, str, str, Dict]:
        # Return the top n entities
        for word, count in self.entities.most_common(top_n):
            yield self.pub_key, 'ent', str(hash(word)), {'word': word, 'count': count}
        # Return the total count for the publication
        yield self.pub_key, None, None, {'count': self.article_count}

    def transform_for_database(self, top_n=2000) -> List[Tuple[str, str, str, Dict]]:
        """Returns a list of tuples containing one of two types of message.

        For messages used as Firestore documents storing the word and count:
            (publication, collection, doc_id, document_dict)

        For messages used to increment the publication's document count
            publication, None, None, {'count': 1}
            When consuming this type of message check the collection or doc_id for None values
        """
        log.info("Transforming document for storage in database")
        return list(self._transform(top_n))

    def __add__(self, other):
        self.article_count += 1
        self.publication = other.publication
        self.entities += other.entities
        return self
