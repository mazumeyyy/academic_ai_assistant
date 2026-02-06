"""
Vector Store Handler Module
This module manages the vector database for semantic search
"""

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import os

class VectorStoreHandler:
    """
    Manages vector database operations for document search
    """
    
    def __init__(self, persist_directory="./data/vectorstore"):
        """
        Initialize the vector store handler
        
        Args:
            persist_directory: Directory where vector store will be saved
        """
        self.persist_directory = persist_directory
        
        # Initialize embeddings model
        # This converts text into numerical vectors
        print("Loading embedding model...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        print("Embedding model loaded!")
        
        self.vectorstore = None
    
    def create_vectorstore(self, documents):
        """
        Create a new vector store from documents
        
        Args:
            documents: List of document chunks to store
            
        Returns:
            Created vector store object
        """
        print(f"Creating vector store with {len(documents)} documents...")
        
        self.vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        
        print("Vector store created successfully!")
        return self.vectorstore
    
    def load_vectorstore(self):
        """
        Load an existing vector store from disk
        
        Returns:
            Loaded vector store object or None if doesn't exist
        """
        if os.path.exists(self.persist_directory):
            print("Loading existing vector store...")
            self.vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
            print("Vector store loaded!")
            return self.vectorstore
        else:
            print("No existing vector store found.")
            return None
    
    def similarity_search(self, query, k=4):
        """
        Search for documents similar to the query
        
        Args:
            query: Search query string
            k: Number of results to return
            
        Returns:
            List of similar documents
        """
        if self.vectorstore:
            results = self.vectorstore.similarity_search(query, k=k)
            return results
        else:
            print("No vector store available. Please create or load one first.")
            return []
    
    def delete_vectorstore(self):
        """
        Delete the vector store
        """
        if os.path.exists(self.persist_directory):
            import shutil
            shutil.rmtree(self.persist_directory)
            print("Vector store deleted!")
            self.vectorstore = None
            