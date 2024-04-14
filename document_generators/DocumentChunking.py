import os

from langchain_community.document_loaders.directory import DirectoryLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader

from logs.Logging import log


class DocumentChunking:

    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 0):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        pass

    def directory_files_chunking(self, dir_path: str, split_text: bool = False) -> list[Document]:
        log.info("Processing directory for chunking: %s" % dir_path)
        if not os.path.exists(dir_path):
            raise Exception(f"{dir_path} doesn't exist. Please recheck")
        loader = DirectoryLoader(dir_path)
        documents = loader.load()
        if not split_text:
            return documents
        # text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0, separator=". ")
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap,
                                                                             encoding_name="cl100k_base")
        return text_splitter.split_documents(documents)

    def single_file_chunking(self, path_to_file: str, split_text: bool = False) -> list[Document]:
        log.info("Processing document for chunking: %s" % path_to_file)
        if not os.path.exists(path_to_file):
            raise Exception(f"{path_to_file} doesn't exist. Please check")
        loader = TextLoader(path_to_file)
        documents = loader.load()
        if not split_text:
            return documents
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap,
                                                                             encoding_name="cl100k_base")
        return text_splitter.split_documents(documents)

