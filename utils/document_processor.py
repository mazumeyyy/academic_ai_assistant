"""
Document Processor Module:--this module handles loading and splittingdocuments into chunks...
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader
import os

class DocumentProcessor:
    """
    Handles document loading and text splitting
    """
    
    def __init__(self, chunk_size=1000, chunk_overlap=200):
        """
        Initialize the document processor
        
        Args:
            chunk_size: Size of each text chunk (in characters)
            chunk_overlap: Number of overlapping characters between chunks
        """
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def load_pdf(self, file_path):
        """
        Load and split PDF documents
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            List of document chunks
        """
        try:
            loader = PyPDFLoader(file_path)
            documents = loader.load()
            chunks = self.text_splitter.split_documents(documents)
            return chunks
        except Exception as e:
            print(f"Error loading PDF {file_path}: {str(e)}")
            return []
    
    def load_text(self, file_path):
        """
        Load and split text documents
        
        Args:
            file_path: Path to the text file
            
        Returns:
            List of document chunks
        """
        try:
            loader = TextLoader(file_path, encoding='utf-8')
            documents = loader.load()
            chunks = self.text_splitter.split_documents(documents)
            return chunks
        except Exception as e:
            print(f"Error loading text file {file_path}: {str(e)}")
            return []
    
    def process_multiple_files(self, file_paths):
        """
        Process multiple documents at once
        
        Args:
            file_paths: List of file paths
            
        Returns:
            Combined list of all document chunks
        """
        all_docs = []
        
        for path in file_paths:
            print(f"Processing: {path}")
            
            if path.endswith('.pdf'):
                all_docs.extend(self.load_pdf(path))
            elif path.endswith('.txt'):
                all_docs.extend(self.load_text(path))
            else:
                print(f"Unsupported file type: {path}")
        
        print(f"Total chunks created: {len(all_docs)}")
        return all_docs
    