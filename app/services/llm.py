"""
Large Language Model service using Hugging Face
"""
from huggingface_hub import InferenceClient
import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class LLMService:
    """Service for LLM interactions via Hugging Face Inference API"""
    
    def __init__(self):
        self.api_token = os.getenv("HF_TOKEN")
        if not self.api_token:
            raise ValueError("HF_TOKEN environment variable not set")
        
        self.client = InferenceClient(api_key=self.api_token)
        self.model = "Qwen/Qwen2-7B-Instruct"
    
    def generate_text(self, prompt: str, max_tokens: int = 512) -> Optional[str]:
        """
        Generate text using Hugging Face Inference API
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text or None if error
        """
        try:
            response = self.client.text_generation(
                prompt,
                model=self.model,
                max_new_tokens=max_tokens,
                temperature=0.7,
            )
            return response
        except Exception as e:
            logger.error(f"Error generating text: {e}")
            return None
    
    def analyze_resume(self, resume_text: str) -> Optional[dict]:
        """
        Analyze resume using LLM
        
        Args:
            resume_text: Resume content
            
        Returns:
            Analysis results or None if error
        """
        prompt = f"""
        Analyze the following resume and provide:
        1. Overall score (0-100)
        2. Key strengths
        3. Areas for improvement
        4. Recommended skills to add
        
        Resume:
        {resume_text}
        """
        
        try:
            analysis = self.generate_text(prompt)
            return {"analysis": analysis}
        except Exception as e:
            logger.error(f"Error analyzing resume: {e}")
            return None
