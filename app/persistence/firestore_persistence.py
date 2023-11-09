from google.cloud import firestore

def get_database_client():
    return firestore.Client()

def persist(client, publication_name, collname, doc_id, document_dict):
    pass

def persist_no_op(*args, **kwargs):
    pass

def increment_publication(client, publication_name, count):
    pass