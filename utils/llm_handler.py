"""
LLM Handler Module
This module manages interactions with the Ollama AI models
"""

from langchain_community.llms import Ollama
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate

class LLMHandler:
    """
    Handles all AI model operations
    """
    
    def __init__(self, model_name="llama3.2:3b", temperature=0.7):
        """
        Initialize the LLM handler
        
        Args:
            model_name: Name of the Ollama model to use
            temperature: Controls randomness (0.0 = deterministic, 1.0 = creative)
        """
        print(f"Initializing LLM with model: {model_name}")
        
        self.llm = Ollama(
            model=model_name,
            temperature=temperature
        )
        
        print("LLM initialized successfully!")
    
    def create_qa_chain(self, vectorstore):
        """
        Create a Question-Answering chain with document retrieval
        
        Args:
            vectorstore: Vector store containing documents
            
        Returns:
            QA chain object
        """
        # Define the prompt template
        template = """You are a helpful academic assistant. Use the following context from documents to answer the question.
        If you don't know the answer based on the context, say "I don't have enough information in the provided documents to answer this question."
        
        Context from documents:
        {context}
        
        Question: {question}
        
        Provide a clear and detailed answer:"""
        
        PROMPT = PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
        
        # Create the QA chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
            chain_type_kwargs={"prompt": PROMPT},
            return_source_documents=True
        )
        
        return qa_chain
    
    def ask_question(self, qa_chain, question):
        """
        Ask a question using the QA chain
        
        Args:
            qa_chain: The QA chain object
            question: Question string
            
        Returns:
            Answer string
        """
        try:
            result = qa_chain({"query": question})
            return result['result']
        except Exception as e:
            return f"Error: {str(e)}"
    
    def summarize_text(self, text, max_words=200):
        """
        Summarize the given text
        
        Args:
            text: Text to summarize
            max_words: Target length of summary
            
        Returns:
            Summary string
        """
        prompt = f"""Summarize the following text in approximately {max_words} words.
        Focus on the main points and key ideas.
        
        Text to summarize:
        {text}
        
        Summary:"""
        
        try:
            summary = self.llm(prompt)
            return summary
        except Exception as e:
            return f"Error generating summary: {str(e)}"
    
    def explain_concept(self, concept):
        """
        Provide a detailed explanation of a concept
        
        Args:
            concept: The concept to explain
            
        Returns:
            Explanation string
        """
        prompt = f"""Explain the concept of "{concept}" in a clear and educational way.
        
        Your explanation should include:
        1. A simple definition
        2. Why it's important or relevant
        3. A practical example
        4. Any common misconceptions (if applicable)
        
        Make it easy to understand for students.
        
        Explanation:"""
        
        try:
            explanation = self.llm(prompt)
            return explanation
        except Exception as e:
            return f"Error generating explanation: {str(e)}"
    
    def simple_chat(self, message):
        """
        Simple chat without document context
        
        Args:
            message: User message
            
        Returns:
            AI response
        """
        try:
            response = self.llm(message)
            return response
        except Exception as e:
            return f"Error: {str(e)}"
        