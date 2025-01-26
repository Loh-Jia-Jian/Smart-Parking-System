import os
import time
from threading import Thread
from firebase_admin import firestore, initialize_app, credentials
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

        # Initialize Firebase Admin SDK
        cred = credentials.Certificate("app/firebase-adminsdk.json")
        initialize_app(cred)

        self.load_vector_store()

    def fetch_transaction_data(self):
        """Fetch transaction data from Firestore."""
        db = firestore.client()
        transactions_ref = db.collection_group('transactions')  # Query all user transactions
        docs = transactions_ref.stream()

        transaction_texts = []
        for doc in docs:
            data = doc.to_dict()
            transaction_text = (
                f"Transaction ID: {data.get('transactionID', 'N/A')}\n"
                f"Area: {data.get('area', 'N/A')}\n"
                f"Slot Number: {data.get('slotNumber', 'N/A')}\n"
                f"Car Plate: {data.get('carPlate', 'N/A')}\n"
                f"Date: {data.get('date', 'N/A')}\n"
                f"Duration: {data.get('duration', 'N/A')} hours\n"
                f"Total: ${data.get('total', 0):.2f}\n"
                "----------------------------------"
            )
            transaction_texts.append(transaction_text)

        return transaction_texts

    def load_documents(self):
        """Load documents from the data directory and Firestore."""
        documents = []

        # Load local documents
        if os.path.exists(self.data_directory):
            for filename in os.listdir(self.data_directory):
                file_path = os.path.join(self.data_directory, filename)
                if os.path.getsize(file_path) > 0:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                        documents.append(Document(page_content=content))

        # Fetch transaction data
        transaction_texts = self.fetch_transaction_data()
        transaction_documents = [Document(page_content=text) for text in transaction_texts]

        return documents + transaction_documents

    def create_vector_store(self, documents):
        embeddings = OpenAIEmbeddings(openai_api_key=self.openai_api_key)
        texts = [doc.page_content for doc in documents]
        self.vector_store = FAISS.from_texts(texts=texts, embedding=embeddings)
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
        llm = ChatOpenAI(model="gpt-4", openai_api_key=self.openai_api_key)
        prompt_template = PromptTemplate(
            template="""
            You are an assistant specialized in answering questions about car parking information based on the documentation and user transactions. Always provide clear and concise answers.
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
        """Extend monitoring to fetch updates from Firestore."""
        print("Starting database monitoring...")
        while True:
            try:
                print("Fetching Firestore transactions...")
                # Fetch transaction data from Firestore
                transaction_texts = self.fetch_transaction_data()
                transaction_documents = [Document(page_content=text) for text in transaction_texts]

                # Update the vector store with transaction documents
                self.create_vector_store(transaction_documents)
                print("Transactions and vector store updated.")
            except Exception as e:
                print(f"Error in Firestore monitoring: {e}")
            time.sleep(10)  # Check every 10 seconds


    def start_listener(self):
        listener_thread = Thread(target=self.monitor_database, daemon=True)
        listener_thread.start()
