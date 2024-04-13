import os
import sys

import openai
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain_community.vectorstores.marqo import Marqo
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings


import constants
import warnings
from pinecone import Pinecone


os.environ["OPENAI_API_KEY"] = constants.OPENAI_APIKEY
pc = Pinecone(api_key=constants.PINECONE_APIKEY)


# Enable to save to disk & reuse the model (for repeated queries on the same data)
PERSIST = False

def main():
    query = None
    if len(sys.argv) > 1:
        query = sys.argv[1]

    loader = TextLoader('./data/test_file.txt')
    index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory": "persist"}).from_loaders([loader])
    # print(index.model_dump_json)

    with open("./data/test_file.txt") as f:
        data = f.read()

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_text(data)
    index_name = "langchain-qa-with-retrieval"
    ind = Marqo.from_documents(texts, index_name=index_name)

    index = VectorStoreIndexWrapper(vectorstore=ind)

    # vectorstore = pc.Index("first book index")
    # with open("./indexes/saved_index.json", '+w') as file:
    #     file.write(str(index.))

    print(index.query(query))


if __name__ == '__main__':
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        main()

'''
if PERSIST and os.path.exists("persist"):
    print("Reusing index...\n")
    vectorstore = Chroma(persist_directory="persist", embedding_function=OpenAIEmbeddings())
    index = VectorStoreIndexWrapper(vectorstore=vectorstore)
else:
    # loader = TextLoader("data/data.txt") # Use this line if you only need data.txt
    loader = DirectoryLoader("data/")
    if PERSIST:
        index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory": "persist"}).from_loaders([loader])
    else:
        index = VectorstoreIndexCreator().from_loaders([loader])

chain = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(model="gpt-3.5-turbo"),
    retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
)

chat_history = []
while True:
    if not query:
        query = input("Prompt: ")
    if query in ['quit', 'q', 'exit']:
        sys.exit()
    result = chain({"question": query, "chat_history": chat_history})
    print(result['answer'])

    chat_history.append((query, result['answer']))
    query = None
'''
