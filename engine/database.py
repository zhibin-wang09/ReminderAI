from config import index
from llama_index.core import Document


def save_transcribed_recording(doc_id: str, transcription: str) -> None:
    """given the transacription it will store this in to chroma db"""
    # Add a temporary document to the index

    index.insert(
        Document(doc_id=doc_id, text=transcription, metadata={"status": "active"})
    )


def retrieve_transacribed_recording_by_id(recording_id: str) -> str:
    """given the recording id it will retrieve the transcription from chroma db"""
    pass

def delete_transcribed_recording_by_id(doc_id: str) -> None:
    """given the document id it will delete the transcription from chroma db"""
    index.delete(doc_ids=[doc_id])