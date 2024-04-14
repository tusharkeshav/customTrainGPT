import os
import time

import openai
from langchain_community.document_loaders.text import TextLoader
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_openai.chat_models import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain
import tempfile
from logs.Logging import log


class Summariser:

    def __init__(self):
        self.llm = ChatOpenAI(temperature=0, model_name="gpt-3.5")
        self.client = openai.OpenAI()

    def summarise_using_langchain(self, document: list[Document]):
        # Define prompt
        MAX_RETRY = 3
        prompt_template = """You are a teacher, you need to explain each and every line to students. Below is  the 
        story. You need to reframe it in such a manner that every small small information should be retained. Not 
        even slight information should be lost.: 
        "{text}" 
        SUMMARY : """
        while MAX_RETRY:
            try:
                prompt = PromptTemplate.from_template(prompt_template)
                chain = load_summarize_chain(llm=self.llm, prompt=prompt, chain_type="stuff")
                return Summariser.string_loader(chain.run(document))

            except openai.RateLimitError as rate_limit_error:
                MAX_RETRY -= 1
                log.exception(
                    "Rate limit error: Exception: " + rate_limit_error.message + f" Max_RETRY left: {MAX_RETRY}")
                time.sleep(60)
        else:
            log.exception("Rate limit Error occurred. Max retry exhausted.")

    def summarise_using_openai(self, document: list[Document]):
        MAX_RETRIES = 3
        prompt = """
You are a teacher, you need to explain each and every line to students. Below is  the story. You need to reframe it in such a manner that every small small information should be retained. Not even slight information should be lost. 
Focus on each details. Its alright if output is enlarged or huge. Talk about every single detail about the people and events involved in story.

Below is the story.
{query}

Summary: 
"""
        message = prompt.format(query=document[0].page_content)
        while MAX_RETRIES:
            try:
                stream = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    # messages=[{"role": "system", "content": "count from 1 to 10 with no comma or anything inbetween"}],
                    messages=[{"role": "system", "content": message}],
                    stream=True,
                )
                # print(stream)
                output = ""
                for chunk in stream:
                    if chunk.choices[0].delta.content is not None:
                        output += chunk.choices[0].delta.content
                        # print(x)
                log.debug(f"Question: {message} and answered by chatGPT: {output}")
                return Summariser.string_loader(output)
            except openai.RateLimitError as rate_limit_error:
                MAX_RETRIES -= 1
                if MAX_RETRIES == 0:
                    raise SummariserError(f'Exception occurred while summarizing documents: {document} Exception: ' + str(rate_limit_error))
                log.exception(
                    "Rate limit error: Exception: " + rate_limit_error.message + f" Max_RETRY left: {MAX_RETRIES}")
                time.sleep(60)

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


class SummariserError(Exception):
    pass

# su = Summariser()
# # doc = su.summarise(TextLoader('/home/akhil/PycharmProjects/customTrainGPT/data/english_book_X/output/jefp104.txt').load())
# su.summarise_using_openai(TextLoader('/home/akhil/PycharmProjects/customTrainGPT/data/english_book_X/output/jefp104.txt').load())
