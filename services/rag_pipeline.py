import os
import pickle
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()

class RAGPipeline:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.vectorstore = None
        self.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.1-8b-instant",
            temperature=0
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

    def load_documents_from_texts(self, texts: list[str]):
        """Load documents from a list of text strings"""
        docs = [Document(page_content=t) for t in texts]
        split_docs = self.text_splitter.split_documents(docs)
        self.vectorstore = FAISS.from_documents(split_docs, self.embeddings)

    def load_documents_from_files(self, file_paths: list[str]):
        """Load documents from text files"""
        all_texts = []
        for file_path in file_paths:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    all_texts.append(content)
        if all_texts:
            self.load_documents_from_texts(all_texts)

    def save_vectorstore(self, path: str = "vectorstore.pkl"):
        """Save the vectorstore to disk"""
        if self.vectorstore:
            with open(path, 'wb') as f:
                pickle.dump(self.vectorstore, f)

    def load_vectorstore(self, path: str = "vectorstore.pkl"):
        """Load the vectorstore from disk"""
        if os.path.exists(path):
            with open(path, 'rb') as f:
                self.vectorstore = pickle.load(f)

    def query(self, question: str):
        """Query the RAG system"""
        if not self.vectorstore:
            return "No documents loaded yet. Please load documents first."

        # Create the RAG chain using LCEL
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})

        template = """Use the following pieces of context to answer the question at the end.
        If you don't know the answer, just say that you don't know, don't try to make up an answer.

        Context: {context}

        Question: {question}

        Answer:"""
        prompt = PromptTemplate.from_template(template)

        chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )

        return chain.invoke(question)

    def get_relevant_documents(self, question: str, k: int = 3):
        """Get relevant documents for a question without generating answer"""
        if not self.vectorstore:
            return []
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": k})
        docs = retriever.get_relevant_documents(question)
        return [doc.page_content for doc in docs]

rag_pipeline = RAGPipeline()
