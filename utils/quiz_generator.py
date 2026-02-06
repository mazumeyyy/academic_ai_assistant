"""
Quiz Generator Module
This module generates multiple choice quizzes from content
"""

import json
import re
from langchain_community.llms import Ollama

class QuizGenerator:
    """
    Generates quizzes from educational content
    """
    
    def __init__(self, model_name="llama3.2:3b"):
        """
        Initialize the quiz generator
        
        Args:
            model_name: Name of the Ollama model to use
        """
        print(f"Initializing Quiz Generator with model: {model_name}")
        self.llm = Ollama(model=model_name, temperature=0.8)
        print("Quiz Generator ready!")
    
    def generate_quiz(self, content, num_questions=5):
        """
        Generate multiple choice questions from content
        
        Args:
            content: Text content to create questions from
            num_questions: Number of questions to generate
            
        Returns:
            List of question dictionaries
        """
        # Truncate content if too long
        if len(content) > 3000:
            content = content[:3000] + "..."
        
        prompt = f"""Based on the following educational content, generate {num_questions} multiple choice questions.

Content:
{content}

Generate questions in this EXACT format for each question:

QUESTION 1: [Write the question here]
A) [First option]
B) [Second option]
C) [Third option]
D) [Fourth option]
CORRECT: [Letter of correct answer]
EXPLANATION: [Brief explanation]

QUESTION 2: [Write the question here]
...and so on.

Make sure questions test understanding, not just memorization.
Generate the questions now:"""
        
        try:
            print("Generating quiz questions...")
            response = self.llm(prompt)
            questions = self._parse_quiz_response(response)
            print(f"Generated {len(questions)} questions successfully!")
            return questions
        except Exception as e:
            print(f"Error generating quiz: {str(e)}")
            return []
    
    def _parse_quiz_response(self, response):
        """
        Parse the LLM response into structured quiz format
        
        Args:
            response: Raw response from LLM
            
        Returns:
            List of structured question dictionaries
        """
        questions = []
        
        # Split by QUESTION keyword
        question_blocks = re.split(r'QUESTION \d+:', response)[1:]
        
        for block in question_blocks:
            try:
                # Extract question text
                question_match = re.search(r'^(.*?)(?=A\))', block, re.DOTALL)
                if not question_match:
                    continue
                question_text = question_match.group(1).strip()
                
                # Extract options
                options = []
                for letter in ['A', 'B', 'C', 'D']:
                    pattern = f'{letter}\\)(.*?)(?=[B-D]\\)|CORRECT:|$)'
                    option_match = re.search(pattern, block, re.DOTALL)
                    if option_match:
                        option_text = option_match.group(1).strip()
                        options.append(f"{letter}) {option_text}")
                
                # Extract correct answer
                correct_match = re.search(r'CORRECT:\s*([A-D])', block)
                correct_answer = correct_match.group(1) if correct_match else 'A'
                
                # Extract explanation
                explanation_match = re.search(r'EXPLANATION:\s*(.*?)(?=QUESTION|\Z)', block, re.DOTALL)
                explanation = explanation_match.group(1).strip() if explanation_match else "No explanation provided."
                
                # Only add if we have all components
                if question_text and len(options) == 4:
                    questions.append({
                        'question': question_text,
                        'options': options,
                        'correct_answer': correct_answer,
                        'explanation': explanation
                    })
            
            except Exception as e:
                print(f"Error parsing question block: {str(e)}")
                continue
        
        return questions
    
    def generate_true_false(self, content, num_questions=5):
        """
        Generate true/false questions
        
        Args:
            content: Text content to create questions from
            num_questions: Number of questions to generate
            
        Returns:
            List of true/false question dictionaries
        """
        if len(content) > 3000:
            content = content[:3000] + "..."
        
        prompt = f"""Based on the following content, generate {num_questions} TRUE or FALSE questions.

Content:
{content}

Format each question like this:

STATEMENT 1: [Write a statement that is either true or false]
ANSWER: [TRUE or FALSE]
EXPLANATION: [Explain why]

Generate the questions now:"""
        
        try:
            response = self.llm(prompt)
            questions = self._parse_true_false(response)
            return questions
        except Exception as e:
            print(f"Error generating true/false questions: {str(e)}")
            return []
    
    def _parse_true_false(self, response):
        """Parse true/false questions"""
        questions = []
        
        statement_blocks = re.split(r'STATEMENT \d+:', response)[1:]
        
        for block in statement_blocks:
            try:
                statement_match = re.search(r'^(.*?)(?=ANSWER:)', block, re.DOTALL)
                if not statement_match:
                    continue
                statement = statement_match.group(1).strip()
                
                answer_match = re.search(r'ANSWER:\s*(TRUE|FALSE)', block, re.IGNORECASE)
                answer = answer_match.group(1).upper() if answer_match else 'TRUE'
                
                explanation_match = re.search(r'EXPLANATION:\s*(.*?)(?=STATEMENT|\Z)', block, re.DOTALL)
                explanation = explanation_match.group(1).strip() if explanation_match else "No explanation."
                
                if statement:
                    questions.append({
                        'statement': statement,
                        'answer': answer,
                        'explanation': explanation
                    })
            
            except Exception as e:
                continue
        
        return questions
    