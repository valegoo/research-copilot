from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from vector_store import VectorStoreManager
from dotenv import load_dotenv

load_dotenv()

class ChatEngine:
    def __init__(self, vector_store):
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.2)
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
        
        template = """You are a highly capable Research Assistant powered by a group of academic documents.
Your task is to answer user questions using ONLY the provided context from the documents.
If you cannot find the answer in the documents, state that you do not have that information.
ALWAYS provide in-text citations in APA format (e.g., Author, Year) when referring to the documents.
At the end of your answer, provide a list of sources used for this specific answer in APA Reference format.

CONTEXT:
{context}

CHAT HISTORY:
{chat_history}

QUESTION: {question}

ANSWER:"""

        self.prompt = PromptTemplate(
            input_variables=["context", "chat_history", "question"],
            template=template
        )
        
        self.retriever = vector_store.as_retriever(search_kwargs={"k": 5})
        
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.retriever,
            memory=self.memory,
            combine_docs_chain_kwargs={"prompt": self.prompt},
            return_source_documents=True,
            get_chat_history=lambda h: h,
        )

    def ask(self, question: str):
        response = self.chain({"question": question})
        return {
            "answer": response["answer"],
            "sources": [doc.metadata for doc in response["source_documents"]]
        }
