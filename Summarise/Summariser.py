import os
import time

import openai
from langchain.chains.llm import LLMChain
from langchain_community.document_loaders.text import TextLoader
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_openai.chat_models import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain
import tempfile
from logs.Logging import log


class Summariser:

    def __init__(self):
        self.llm = ChatOpenAI(temperature=0, model_name="gpt-3.5")

    def summarise(self, document: list[Document]):
        # Define prompt
        MAX_RETRY = 3
        # prompt_template = """Write a summary of the following. Make sure that no information is lost. I need every bit of information later.:
        # "{text}"
        # SUMMARY  :"""
        prompt_template = """You are a teacher, you need to explain each and every line to students. Below is  the 
        story. You need to reframe it in such a manner that every small small information should be retained. Not 
        even slight information should be lost.: 
        "{text}" 
        SUMMARY : """
        chat = ChatOpenAI(model_name="gpt-3.5-turbo")
        # print(document)
        while MAX_RETRY:
            try:
                prompt = PromptTemplate.from_template(prompt_template)
                # chain = load_summarize_chain(llm=self.llm, prompt=prompt, chain_type="stuff")
                # return Summariser.string_loader(chain.run(document))
                # print(prompt_template.format(text=document[0].page_content))
                print(chat.invoke(prompt_template.format(text=document[0].page_content)))
                exit()

            except openai.RateLimitError as rate_limit_error:
                MAX_RETRY -= 1
                log.exception("Rate limit error: Exception: " + rate_limit_error.message + f" Max_RETRY left: {MAX_RETRY}")
                time.sleep(60)
        else:
            log.exception("Rate limit Error occurred. Max retry exhausted.")

    @staticmethod
    def string_loader(document: str, path=None):
        print(document)
        fd, path = tempfile.mkstemp(suffix="assistant")
        with open(path, 'w') as file:
            file.write(document)
        loader = TextLoader(path)
        doc = loader.load()
        if path and os.path.exists(path):
            os.remove(path)
        return doc

su = Summariser()
doc = su.summarise(TextLoader('/home/akhil/PycharmProjects/customTrainGPT/data/english_book_X/output/jefp104.txt').load())
su.summarise(doc)
