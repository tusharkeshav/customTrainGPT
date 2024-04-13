import os

from langchain_community.document_loaders.text import TextLoader
from langchain_community.document_loaders.directory import DirectoryLoader
from langchain_core.documents import Document

import constants
from QueryModel import QueryModel
from index.Index import Index
from pdf_extract.ExtractPdf import ExtractPdf

# collection_name = '10th-history-complete-book'
collection_name = 'X-english-book'

os.environ["OPENAI_API_KEY"] = constants.OPENAI_APIKEY


def assistant():
    index = Index(collection_name=collection_name)
    query = " What is Spinning Jenny? Explain. Why were many workers opposed to the use of the Spinning Jenny? Discuss"
    query = "Why Mrs. Pumphrey was worried?"

    query_model = QueryModel()
    result = query_model.query(query=query, index=index)


def parse_books(document: list[Document], collection_name):
    index = Index(collection_name=collection_name)
    index.create_index(document=document, summarise=True)


def create_index_file(file_path):
    list_files = os.listdir(file_path)
    for file in list_files:
        loader = TextLoader(file_path=os.path.join(file_path, file))
        doc = loader.load()
        print(f"Started to create index file: {file}")
        parse_books(document=doc, collection_name='X-english-book')
    # loader = DirectoryLoader(path=file_path)
    # doc = loader.load()
    # parse_books(document=doc)

# loader = TextLoader(file_path='/home/akhil/PycharmProjects/customTrainGPT/data/english_book_X/output/jefp101.txt')
# book = loader.load()
# parse_books(book)

# extract_pdf = ExtractPdf().extract_data_from_directory(
#     dir_path='/home/akhil/PycharmProjects/customTrainGPT/data/english_book_X/pdf',
#     save_path='/home/akhil/PycharmProjects/customTrainGPT/data/english_book_X/output')

create_index_file(file_path='/home/akhil/PycharmProjects/customTrainGPT/data/english_book_X/output')

