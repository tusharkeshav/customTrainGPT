from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI
from index.Index import Index


class QueryModel:

    @staticmethod
    def query(query, index: Index):
        chat_history = []
        chain = ConversationalRetrievalChain.from_llm(
            llm=ChatOpenAI(model="gpt-3.5-turbo"),
            retriever=index.get_retriever().as_retriever(search_kwargs={"k": 1}),
        )

        query = None

        while True:
            if query is None:
                query = input("Prompt: ")
            result = chain({"question": query, "chat_history": chat_history})
            print(result["answer"])

            chat_history.append((query, result["answer"]))
            query = None