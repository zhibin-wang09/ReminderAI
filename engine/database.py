from config import index
from llama_index.core import Document

def save_transcribed_recording(transcription: str) -> None:
    """given the transacription it will store this in to chroma db
    """
    # Add a temporary document to the index
   
    index.insert(Document(text=transcription))

    


def retrieve_transacribed_recording_by_id(recording_id: str) -> str:
    """given the recording id it will retrieve the transcription from chroma db
    """
    pass


def retrieve_all_transcriptions() -> list[dict]:
    """retrieve all transcriptions from chroma db
    """
    pass


