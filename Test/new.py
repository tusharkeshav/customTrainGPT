import os
from datetime import datetime

from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores.inmemory import InMemoryVectorStore
from langchain_pinecone import PineconeVectorStore
from langchain_community.vectorstores.faiss import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
import pickle
from langchain_pinecone import PineconeVectorStore, Pinecone

import constants

os.environ["OPENAI_API_KEY"] = constants.OPENAI_APIKEY
os.environ["PINECONE_API_KEY"] = constants.PINECONE_APIKEY
os.environ["PINECONE_INDEX_NAME"] = "first-book-index"


loader = TextLoader("./data/test_file.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
# print(embeddings)
# vectorstore = FAISS.from_documents(documents=docs, embedding=embeddings)
start_time = datetime.now()
# vectorstore = FAISS.load_local("./indexes", embeddings=embeddings, allow_dangerous_deserialization=True)
# # vectorstore = InMemoryVectorStore.from_documents(documents=docs, embedding=embeddings)
vectorstore = PineconeVectorStore.from_existing_index(index_name="first-book-index", embedding=embeddings,
                                                      index_host=constants.PINECONE_HOST)

end_time = datetime.now()
embedding_file = "embeddings.pkl"

print(vectorstore.similarity_search(query="what happened in playground"))
vectorstore.as_retriever()
final_time = datetime.now()
print(f"diff in loading of data {end_time-start_time}")
print(f"diff in finding the similar searc {final_time - end_time}")

# vectorstore.save_local("./indexes")
# with open(embedding_file, "wb") as f:
#     pickle.dump(vectorstore.embeddings, f)

exit()
index_name = "first-book-index"
pinecone = Pinecone(api_key=constants.PINECONE_APIKEY)


index = pinecone.index(index_name)

print(vectorstore.similarity_search("what happened in playground"))

# docsearch = PineconeVectorStore.from_documents(docs, embeddings, index_name=index_name)

# query = "what happened in playground?"
# docs = docsearch.similarity_search(query)
# print(docs)
# print(docs[0].page_content)
