import chromadb
from chromadb.config import Settings

chroma_client = chromadb.HttpClient(host='localhost', port=1234, ssl=False, settings=Settings(allow_reset=True))

transcription_collection = chroma_client.get_or_create_collection(name="transcriptions")