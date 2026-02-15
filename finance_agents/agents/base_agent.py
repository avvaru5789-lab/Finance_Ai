"""
Base agent class for all financial analysis agents.
Provides common functionality for LLM interaction with structured output.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Type
from openai import OpenAI
from pydantic import BaseModel
from loguru import logger


class BaseAgent(ABC):
    """
    Base class for all financial agents.
    
    Uses OpenRouter for LLM access and enforces structured output
    via Pydantic schemas.
    """
    
    def __init__(
        self,
        openrouter_api_key: str,
        model: str = "openai/gpt-4o",
        temperature: float = 0.1
    ):
        """
        Initialize the agent.
        
        Args:
            openrouter_api_key: OpenRouter API key
            model: Model to use (default: gpt-4o)
            temperature: Temperature for generation (low for determinism)
        """
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=openrouter_api_key
        )
        self.model = model
        self.temperature = temperature
        
        logger.info(f"Initialized {self.__class__.__name__} with model {model}")
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """
        Return the system prompt for this agent.
        
        This defines the agent's role and expertise.
        """
        pass
    
    @abstractmethod
    def get_output_schema(self) -> Type[BaseModel]:
        """
        Return the Pydantic schema for this agent's output.
        
        This enforces structured output validation.
        """
        pass
    
    @abstractmethod
    def extract_data(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract relevant data from FinancialState for this agent.
        
        Args:
            state: Complete FinancialState
            
        Returns:
            Dictionary with only data needed by this agent
        """
        pass
    
    @abstractmethod
    def create_prompt(self, data: Dict[str, Any]) -> str:
        """
        Create the user prompt from extracted data.
        
        Args:
            data: Extracted data from extract_data()
            
        Returns:
            Formatted prompt string
        """
        pass
    
    def analyze(self, state: Dict[str, Any]) -> BaseModel:
        """
        Main analysis method - processes state and returns structured output.
        
        Args:
            state: FinancialState dictionary
            
        Returns:
            Pydantic model instance (schema from get_output_schema())
        """
        try:
            # 1. Extract relevant data
            logger.info(f"{self.__class__.__name__}: Extracting data from state")
            data = self.extract_data(state)
            
            # 2. Create user prompt
            logger.info(f"{self.__class__.__name__}: Creating prompt")
            user_prompt = self.create_prompt(data)
            
            # 3. Call LLM with structured output
            logger.info(f"{self.__class__.__name__}: Calling LLM")
            response = self.client.beta.chat.completions.parse(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.get_system_prompt()},
                    {"role": "user", "content": user_prompt}
                ],
                response_format=self.get_output_schema(),
                temperature=self.temperature
            )
            
            # 4. Extract and validate parsed output
            result = response.choices[0].message.parsed
            
            logger.info(f"{self.__class__.__name__}: Analysis complete")
            return result
            
        except Exception as e:
            logger.error(f"{self.__class__.__name__}: Analysis failed - {e}")
            raise
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(model={self.model})"
