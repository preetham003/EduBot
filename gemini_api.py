import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image
import io
import base64
from typing import Optional, Tuple

# Load environment variables
load_dotenv()

class GeminiAPI:
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=self.api_key)
        
        # Initialize models
        self.text_model = genai.GenerativeModel('gemini-pro-latest')
        self.vision_model = genai.GenerativeModel('gemini-pro-latest')
        
        # Educational context prompt
        self.system_prompt = """
        You are EduBot, an intelligent educational assistant designed to help students and faculty with academic queries. 
        Your role is to:
        
        1. Provide clear, accurate, and educational responses
        2. Break down complex concepts into understandable parts
        3. Encourage learning and critical thinking
        4. Provide examples and practical applications when relevant
        5. Be supportive and encouraging
        6. If you're unsure about something, acknowledge it and suggest reliable sources
        7. For image-based queries, analyze the content and provide educational insights
        
        Always maintain a helpful, professional, and educational tone. Focus on being informative while keeping responses concise and engaging.
        """
    
    def get_text_model_name(self) -> str:
        return self.text_model.model_name

    def get_vision_model_name(self) -> str:
        return self.vision_model.model_name
    
    def generate_text_response(self, user_query: str, context: str = "") -> Tuple[str, bool]:
        """
        Generate response for text-based queries
        Returns: (response_text, success_status)
        """
        try:
            full_prompt = f"{self.system_prompt}\n\nContext: {context}\n\nStudent/Faculty Query: {user_query}\n\nResponse:"
            
            response = self.text_model.generate_content(full_prompt)
            
            if response.text:
                return response.text.strip(), True
            else:
                return "I apologize, but I couldn't generate a response. Please try rephrasing your question.", False
                
        except Exception as e:
            error_msg = f"Error generating response: {str(e)}"
            return f"I'm experiencing technical difficulties. Please try again later. ({error_msg})", False
    
    def generate_image_response(self, image_data, user_query: str = "") -> Tuple[str, bool]:
        """
        Generate response for image-based queries
        Returns: (response_text, success_status)
        """
        try:
            # Prepare the prompt for image analysis
            if user_query:
                prompt = f"{self.system_prompt}\n\nPlease analyze this image and respond to the following query: {user_query}"
            else:
                prompt = f"{self.system_prompt}\n\nPlease analyze this image and provide educational insights about what you see. Explain any concepts, formulas, diagrams, or educational content visible in the image."
            
            # Generate response with image
            response = self.vision_model.generate_content([prompt, image_data])
            
            if response.text:
                return response.text.strip(), True
            else:
                return "I couldn't analyze this image. Please ensure it's clear and try again.", False
                
        except Exception as e:
            error_msg = f"Error analyzing image: {str(e)}"
            return f"I'm having trouble analyzing this image. Please try again later. ({error_msg})", False
    
    def process_uploaded_image(self, uploaded_file) -> Optional[Image.Image]:
        """
        Process uploaded image file and return PIL Image
        """
        try:
            # Read the uploaded file
            image_data = uploaded_file.read()
            
            # Convert to PIL Image
            image = Image.open(io.BytesIO(image_data))
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            return image
            
        except Exception as e:
            print(f"Error processing image: {e}")
            return None
    
    def get_chat_suggestions(self, user_role: str) -> list:
        """
        Get suggested questions based on user role
        """
        if user_role == 'student':
            return [
                "Explain this mathematical concept",
                "Help me understand this diagram",
                "What is the solution to this problem?",
                "Can you break down this complex topic?",
                "Provide examples for this concept"
            ]
        else:  # faculty
            return [
                "Analyze this educational content",
                "Suggest teaching methods for this topic",
                "Create assessment questions",
                "Explain pedagogical approaches",
                "Review this academic material"
            ]
    
    def validate_educational_content(self, query: str) -> bool:
        """
        Basic validation to ensure content is educational
        """
        # Simple keyword-based validation
        educational_keywords = [
            'explain', 'how', 'what', 'why', 'solve', 'calculate', 'analyze',
            'describe', 'compare', 'define', 'summarize', 'teach', 'learn',
            'study', 'homework', 'assignment', 'concept', 'theory', 'formula'
        ]
        
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in educational_keywords) or len(query.split()) > 3