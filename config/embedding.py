from config.database import chroma_collection
from llama_index.core import PromptTemplate, Settings, StorageContext, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.chroma import ChromaVectorStore

# create embedding model and update the global settings of llama index
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
Settings.embed_model = embed_model
Settings.llm = Ollama(model="llama2", system_prompt="You are a helpful assistant.")

# create a our own swappable vector store component
vector_store = ChromaVectorStore(chroma_collection = chroma_collection, mode="append")
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# creating an index
index = VectorStoreIndex.index = VectorStoreIndex.from_vector_store(
    vector_store, 
    storage_context=storage_context
)
Settings.index = index

# create a query engine using the index
template = ("Your name is Raisa, imagine you are a helpful assistant and "
    "you answer your boss's questions about things they told you to remember."
    "things to remember related to the query:: \n"
    "-----------------------------------------\n"
    "{context_str}\n"
    "-----------------------------------------\n"
    "Please respond to the following inquiry:\n\n"
    "Question: {query_str}\n\n"
    "Answer succinctly and ensure your response is helpful and accurate. If you do not know the answer, simply state that you do not have that information."
    "When you answer question don't add emoji.")

qa_template = PromptTemplate(template)

query_engine = index.as_query_engine(text_qa_template=qa_template, streaming=True)
