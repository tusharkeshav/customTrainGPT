import time

import openai

import constants

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.qdrant import Qdrant
from qdrant_client import QdrantClient
from logs.Logging import log
from langchain_core.documents import Document
from Summarise.Summariser import Summariser


class Index:

    def __init__(self, collection_name, API=None, host_name=None, ):
        self.API = API or constants.PINECONE_APIKEY
        self.API: str = constants.QDRANT_APIKEY
        self.host_name: str = constants.QDRANT_HOSTNAME
        self.collection_name: str = collection_name
        self.embeddings = OpenAIEmbeddings()

    def create_index(self, document: list[Document], summarise=False):
        max_retries = 5
        if summarise:
            # print(len(document))
            document = Summariser().summarise_using_openai(document)
        while max_retries:
            try:
                qdrant = Qdrant.from_documents(
                    document,
                    self.embeddings,
                    url=self.host_name,
                    prefer_grpc=True,
                    api_key=self.API,
                    collection_name=self.collection_name,
                )
            except openai.RateLimitError as rate_limit_error:
                max_retries -= 1
                if max_retries == 0:
                    raise IndexException('Unable to index. Rate limit error occurred. Retries exhausted')
                log.exception('Rate limit error while converting text to embeddings : %s. Exception: %s', rate_limit_error)
                time.sleep(60 * abs(3-max_retries))  # openai.RateLimitError on embedding is 20 seconds

            except IndexException as e:
                log.exception('IndexException occurred while creating index: %s', e)
                raise IndexException('Error occurred while creating index: %s', e)

    def __create_retriever(self):

        client = QdrantClient(
            url=constants.QDRANT_HOSTNAME,
            api_key=constants.QDRANT_APIKEY,
        )

        doc_store = Qdrant(
            client=client, collection_name=self.collection_name,
            embeddings=self.embeddings
        )
        return doc_store

    def get_retriever(self):
        return self.__create_retriever()


class IndexException(Exception):
    pass

