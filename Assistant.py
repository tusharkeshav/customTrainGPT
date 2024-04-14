import os
from concurrent.futures import wait
from langchain_core.documents import Document
from ThreadManager import executor
from document_generators.DocumentChunking import DocumentChunking

import constants
from QueryModel import QueryModel
from index.Index import Index
from logs.Logging import log
from pdf_extract.ExtractPdf import ExtractPdf

os.environ["OPENAI_API_KEY"] = constants.OPENAI_APIKEY


def assistant(collection_name):
    index = Index(collection_name=collection_name)
    # query = " What is Spinning Jenny? Explain. Why were many workers opposed to the use of the Spinning Jenny?
    # Discuss"
    query = "The two boys in London were surprised and fascinated. Why?"

    query_model = QueryModel()
    result = query_model.query(query=query, index=index)


def create_index_single_file(document: list[Document], collection_name):
    try:
        log.info("Starting to create index: %s", document)

        index = Index(collection_name=collection_name)
        index.create_index(document=document, summarise=False)

        log.info("Index creation successful for document: %s", document[0].metadata)
    except Exception as E:
        log.exception("Index creation failed for document: %s. Skipping it. Exception: %s", document[0].metadata, E)


def __process_chunk_and_index(path, collection_name, split_text):
    document = DocumentChunking().single_file_chunking(path_to_file=path,
                                                       split_text=True)
    log.info(f"Started to create index file: {path.split('/')[-1]}")
    create_index_single_file(document=document, collection_name=collection_name)


def create_index_on_directory(dir_path: str, collection_name: str):
    list_files = os.listdir(dir_path)
    thread_queue = []
    # thread_executor = ThreadManager(workers=3).get_executor()
    for file in list_files:
        absolute_file_path = os.path.join(dir_path, file)
        # thread = executor.submit(__process_chunk_and_index, path=absolute_file_path, collection_name=collection_name, split_text=True)
        # thread = thread_executor.submit(__process_chunk_and_index, path=absolute_file_path, collection_name=collection_name, split_text=True)
        __process_chunk_and_index(path=absolute_file_path, collection_name=collection_name, split_text=True)
        # thread_queue.append(thread)
    # wait(thread_queue)
        # document = DocumentChunking().single_file_chunking(path_to_file=absolute_file_path,
        #                                                    split_text=True)
        # log.info(f"Started to create index file: {file}")
        # create_index_single_file(document=document, collection_name=collection_name)
    # loader = DirectoryLoader(path=dir_path)
    # doc = loader.load()
    # parse_books(document=doc)


# loader = TextLoader(dir_path='/home/akhil/PycharmProjects/customTrainGPT/data/english_book_X/output/jefp101.txt')
# book = loader.load()
# parse_books(book)

# extract_pdf = ExtractPdf().extract_data_from_directory(
#     dir_path='/home/akhil/PycharmProjects/customTrainGPT/data/english_book_X/pdf',
#     save_path='/home/akhil/PycharmProjects/customTrainGPT/data/english_book_X/output')

# create_index_file(dir_path='/home/akhil/PycharmProjects/customTrainGPT/data/english_book_X/output',
#                   collection_name='first_chapter')
#
# assistant(collection_name='first_chapter')

# document = DocumentChunking().single_file_chunking(
#     path_to_file='/home/akhil/PycharmProjects/customTrainGPT/data/XI-biology-book/kebo102.txt')
# create_index_single_file(document, collection_name='first_chapter')
# assistant(collection_name='first_chapter')

def extract_and_index(input_dir, output_dir, collection_name):
    # try:
    #     executor.submit(ExtractPdf().extract_data_from_directory(input_dir=input_dir, output_dir=output_dir))
    # except Exception as e:
    #     log.error('Error occurred while extracting. Halted further execution. Exception: %s', e)
    #     exit(1)
    create_index_on_directory(dir_path=output_dir, collection_name=collection_name)


if __name__ == '__main__':
    extract_and_index(input_dir='/home/akhil/PycharmProjects/customTrainGPT/data/XI-biology-book/in',
                      output_dir='/home/akhil/PycharmProjects/customTrainGPT/data/XI-biology-book/out',
                      collection_name='XI-biology-book')
    assistant(collection_name='XI-biology-book')
