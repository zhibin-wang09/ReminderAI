import chromadb

# chroma_client = chromadb.E(host="localhost", port=8000, ssl=False)
chroma_client = chromadb.EphemeralClient()

chroma_collection = chroma_client.get_or_create_collection(name="transcriptions")