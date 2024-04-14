import os
from pprint import pprint

from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain_community.document_loaders.directory import DirectoryLoader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter
# from qdrant_client import QdrantClient
from langchain_community.document_loaders.text import TextLoader
from langchain_community.vectorstores.qdrant import Qdrant
from qdrant_client import QdrantClient

import constants

os.environ["OPENAI_API_KEY"] = constants.OPENAI_APIKEY

# loader = TextLoader("./data/data.txt")
# loader = TextLoader("./data/history_X_ch1-1_cleaned.txt")
# loader = DirectoryLoader("./history_complete_book")
# documents = loader.load()
# # text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0, separator=". ")
# text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=500, chunk_overlap=0, encoding_name="cl100k_base")
# docs = text_splitter.split_documents(documents)
# print(len(docs))
# print(docs[0])
# print(docs[1])
# print(docs)

embeddings = OpenAIEmbeddings()


def create_index(collection_name, document):
    url = constants.QDRANT_HOSTNAME
    api_key = constants.QDRANT_APIKEY

    qdrant = Qdrant.from_documents(
        document,
        embeddings,
        url=url,
        prefer_grpc=True,
        api_key=api_key,
        collection_name=collection_name,
    )


def retrieve_data(collection_name):
    client = QdrantClient(
        url=constants.QDRANT_HOSTNAME,
        api_key=constants.QDRANT_APIKEY,
    )

    doc_store = Qdrant(
        client=client, collection_name=collection_name,
        embeddings=embeddings
    )

    # print(doc_store.similarity_search("What happened in playground?"))

    chat_history = []
    chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model="gpt-3.5-turbo"),
        retriever=doc_store.as_retriever(search_kwargs={"k": 1}),
    )

    query = None
    with open('/home/akhil/PycharmProjects/customTrainGPT/data/english_book_X/output/jefp109.txt', 'r') as file:
        query = file.read()
    print(query)
    result = chain({"question": query, "chat_history": chat_history})
    print(result)
    exit()
    while True:
        if query is None:
            query = input("Prompt: ")
        pprint(doc_store.similarity_search(query))
        result = chain({"question": query, "chat_history": chat_history})
        print(result["answer"])

        chat_history.append((query, result["answer"]))
        query = None

# retrieve_data(collection_name='10th-history-complete-book')

docs = TextLoader('/home/akhil/PycharmProjects/customTrainGPT/data/test_file.txt').load()
# docs = loader.load()

create_index(collection_name="test_book", document=docs)


