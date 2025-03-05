from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

class EmbeddingIngestor:
    def __init__(self):
        self.model = HuggingFaceEmbeddings(model_name = "all-MiniLM-L6-v2")
    
    def create_embeddings(self, text):
        with open("output.md", "w", encoding = "utf-8") as file:
            file.write(text)
        
        loader = UnstructuredMarkdownLoader("output.md")
        data = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 50)
        chunks = text_splitter.split_documents(data)
        vector_db = FAISS.from_documents(documents=chunks, embedding=self.model)
        vector_db.save_local("faiss_db")

        return vector_db