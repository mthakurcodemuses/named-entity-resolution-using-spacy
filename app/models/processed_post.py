from pydantic import BaseModel
from collections import Counter
from typing import List, Tuple, Dict

class ProcessedPost(BaseModel):
    publications: str
    entities:Counter = Counter()
    article_count: int = 0

    @property
    def pub_key(self) -> str
        return None
    
    def transform_for_database(self, top_n=2000) -> List[Tuple[str, str, str, Dict]]:
        return None
    
    def __add__(self, other) -> ProcessedPost:
        return self