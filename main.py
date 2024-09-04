from llama_index.llms.openai import OpenAI
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader


import os

from getpass import getpass

apikey = os.environ["OPENAI_API_KEY"]

documents = SimpleDirectoryReader('app/resources').load_data()

index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()


response = query_engine.query("de qué se trata el cuento?")
print(response)