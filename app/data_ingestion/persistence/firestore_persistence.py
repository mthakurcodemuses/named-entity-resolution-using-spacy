from google.cloud import firestore

from app.data_ingestion.utils.app_logger import app_logger as log


def get_database_client():
    return firestore.Client()


def persist(client, publication_name, collname, doc_id, document_dict):
    # Check these values to determine if this is a Publication count increment message
    if collname is None or doc_id is None:
        increment_publication(client, publication_name, document_dict['count'])
    else:
        # Map the increment class to the count value
        document_dict['count'] = firestore.Increment(document_dict['count'])
        # pubdoc is the firestore document for the given publication
        pubdoc = client.collection(u'publications').document(publication_name)
        # wrddoc is the document that stores the word and count
        wrddoc = pubdoc.collection(collname).document(doc_id)
        # Merge will allow the counter to be incremented
        wrddoc.set(document_dict, merge=True)
        log.debug("incremented word counter")

def persist_no_op(*args, **kwargs):
    pass


def increment_publication(client, publication_name, count):
    # pubdoc is the firestore document for the given publication
    pubdoc = client.collection(u'publications').document(publication_name)
    # Increment the doc counter for the given publication
    pubdoc.set({'count': firestore.Increment(count)}, merge=True)
    log.debug(f"Incremented the publication counter for {publication_name}")
