import os

from langchain_community.document_loaders.directory import DirectoryLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader


class DocumentChunking:

    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 0):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        pass

    def directory_files_chunking(self, path) -> list[Document]:
        if not os.path.exists(path):
            raise Exception(f"{path} doesn't exist. Please recheck")
        loader = DirectoryLoader(path)
        documents = loader.load()
        # text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0, separator=". ")
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap,
                                                                             encoding_name="cl100k_base")
        return text_splitter.split_documents(documents)

    def single_file_chunking(self, path_to_file: str) -> list[Document]:
        if not os.path.exists(path_to_file):
            raise Exception(f"{path_to_file} doesn't exist. Please check")
        loader = TextLoader(path_to_file)
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap,
                                                                             encoding_name="cl100k_base")
        return text_splitter.split_documents(documents)

