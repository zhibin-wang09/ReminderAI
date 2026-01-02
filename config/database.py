import chromadb

chroma_client = chromadb.HttpClient(host='localhost', port=1234, ssl=False)
chroma_client.heartbeat()

chroma_collection = chroma_client.get_or_create_collection(name="transcriptions")