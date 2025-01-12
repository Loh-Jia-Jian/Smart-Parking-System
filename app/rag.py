import os
import time
from threading import Thread
from langchain.vectorstores import FAISS
from langchain.schema import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI


class RAG:
    def __init__(self, data_directory, openai_api_key):
        self.data_directory = data_directory
        self.openai_api_key = openai_api_key
        self.vector_store = None
        self.qa_system = None
        self.last_update_time = 0
        self.load_vector_store()

    def load_documents(self):
        from langchain.document_loaders import TextLoader, PyPDFLoader
        from langchain.text_splitter import RecursiveCharacterTextSplitter

        documents = []
        for filename in os.listdir(self.data_directory):
            file_path = os.path.join(self.data_directory, filename)
            if os.path.getsize(file_path) == 0:
                print(f"Skipping empty file: {filename}")
                continue

            if filename.endswith(".md"):
                loader = TextLoader(file_path)
                docs = loader.load()
                documents.extend(docs)
            elif filename.endswith(".pdf"):
                loader = PyPDFLoader(file_path)
                docs = loader.load()
                documents.extend(docs)

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=100,
            separators=["\n## ", "\n### ", "\n"],
        )

        split_docs = []
        for doc in documents:
            raw_text = doc.page_content
            chunks = text_splitter.split_text(raw_text)
            split_docs.extend([
                Document(page_content=chunk, metadata=doc.metadata) for chunk in chunks
            ])

        return split_docs

    def create_vector_store(self, documents):
        embeddings = OpenAIEmbeddings(openai_api_key=self.openai_api_key)
        texts = [doc.page_content for doc in documents]
        metadata = [doc.metadata for doc in documents]
        self.vector_store = FAISS.from_texts(texts=texts, embedding=embeddings, metadatas=metadata)
        self.vector_store.save_local("faiss_index")

    def load_vector_store(self):
        if os.path.exists("faiss_index"):
            embeddings = OpenAIEmbeddings(openai_api_key=self.openai_api_key)
            self.vector_store = FAISS.load_local(
                "faiss_index", embeddings, allow_dangerous_deserialization=True
            )
            self.create_qa_system()
        else:
            print("No vector store found. Initializing...")
            documents = self.load_documents()
            self.create_vector_store(documents)
            self.create_qa_system()


    def create_qa_system(self):
        llm = ChatOpenAI(model="gpt-4o", openai_api_key=self.openai_api_key)
        prompt_template = PromptTemplate(
            template="""
            You are an assistant specialized in answering questions about car parking information based on the documentation. Always provide clear and concise answers.
            If unsure, state so clearly. Here's the user's question:

            Question: {question}
            Context: {context}
            """,
            input_variables=["question", "context"]
        )
        self.qa_system = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=self.vector_store.as_retriever(),
            chain_type_kwargs={"prompt": prompt_template}
        )

    def monitor_database(self):
        print("Starting database monitoring...")
        while True:
            try:
                # Check the last modification time of the data directory
                latest_update = max(
                    os.path.getmtime(os.path.join(self.data_directory, f))
                    for f in os.listdir(self.data_directory)
                )
                if latest_update > self.last_update_time:
                    print("Detected database update. Reloading documents...")
                    self.last_update_time = latest_update
                    documents = self.load_documents()
                    self.create_vector_store(documents)
                    print("Documents and vector store updated.")
                else:
                    print("No updates detected.")
            except Exception as e:
                print(f"Error in database monitoring: {e}")
            time.sleep(10)  # Check every 10 seconds


    def start_listener(self):
        listener_thread = Thread(target=self.monitor_database, daemon=True)
        listener_thread.start()

