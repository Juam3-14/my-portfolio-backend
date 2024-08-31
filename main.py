
from llama_index.llms.openai import OpenAI
from llama_index.agent.openai import OpenAIAgent

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, Settings
from llama_index.llms.ollama import Ollama

from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb, os
from chromadb.utils import embedding_functions

#model = "gpt-3.5-turbo"
#prompt="Eres un pirata."


print("Holaaa")

Settings.llm = Ollama(model="llama2", request_timeout=60.0)
#--embeddingfunction = embedding_functions.OpenAIEmbeddingFunction(model_name="text_embedding-ada-002", api_key=apiKey)
#--chroma_client=chromadb.HttpClient(host='localhost', port=8000)

documents = SimpleDirectoryReader(input_dir='./app/resources').load_data()
db = chromadb.PersistentClient(path="./chroma_db")
chroma_collection = db.get_or_create_collection("quickstart")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)

query_engine = index.as_query_engine()
response = query_engine.query("De que se trata el texto?")
