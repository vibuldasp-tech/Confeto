"""AI provider interface for gap analysis."""

import os
from typing import Optional, Dict
from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)


class AIProvider(ABC):
    """Abstract base class for AI providers."""
    
    @abstractmethod
    def analyze(self, prompt: str, max_tokens: Optional[int] = None) -> str:
        """Send a prompt to the AI and get a response."""
        pass


class OpenAIProvider(AIProvider):
    """OpenAI API provider."""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """Initialize OpenAI provider."""
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("openai package not installed. Install with: pip install openai")
        
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key not provided")
        
        self.model = model or os.getenv('OPENAI_MODEL', 'gpt-4-turbo-preview')
        self.client = OpenAI(api_key=self.api_key)
    
    def analyze(self, prompt: str, max_tokens: Optional[int] = None) -> str:
        """Send a prompt to OpenAI and get a response."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a document analysis expert specializing in gap analysis."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens or 4000,
                temperature=0.3,  # Lower temperature for more consistent analysis
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise


class AnthropicProvider(AIProvider):
    """Anthropic (Claude) API provider."""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """Initialize Anthropic provider."""
        try:
            from anthropic import Anthropic
        except ImportError:
            raise ImportError("anthropic package not installed. Install with: pip install anthropic")
        
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("Anthropic API key not provided")
        
        self.model = model or os.getenv('ANTHROPIC_MODEL', 'claude-3-sonnet-20240229')
        self.client = Anthropic(api_key=self.api_key)
    
    def analyze(self, prompt: str, max_tokens: Optional[int] = None) -> str:
        """Send a prompt to Anthropic and get a response."""
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens or 4000,
                temperature=0.3,
                system="You are a document analysis expert specializing in gap analysis.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return message.content[0].text
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            raise


def get_ai_provider(provider_name: Optional[str] = None) -> AIProvider:
    """
    Factory function to get an AI provider instance.
    
    Args:
        provider_name: Name of the provider ('openai' or 'anthropic')
        
    Returns:
        AIProvider instance
    """
    provider_name = provider_name or os.getenv('AI_PROVIDER', 'openai')
    
    if provider_name.lower() == 'openai':
        return OpenAIProvider()
    elif provider_name.lower() == 'anthropic':
        return AnthropicProvider()
    else:
        raise ValueError(f"Unknown AI provider: {provider_name}")
