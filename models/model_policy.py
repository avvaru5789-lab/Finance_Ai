"""
Model routing policy for cost-efficient LLM usage.
Defines which model to use for different tasks.
"""

from enum import Enum
from typing import Dict, Optional
from loguru import logger

from backend.config.settings import settings


class TaskType(Enum):
    """Types of tasks that require LLM usage."""
    
    # Parsing tasks (cheap models)
    TEXT_EXTRACTION = "text_extraction"
    DATA_NORMALIZATION = "data_normalization"
    
    # Reasoning tasks (GPT-4o-mini)
    DEBT_ANALYSIS = "debt_analysis"
    SAVINGS_STRATEGY = "savings_strategy"
    BUDGET_OPTIMIZATION = "budget_optimization"
    RISK_SCORING = "risk_scoring"
    SCENARIO_SIMULATION = "scenario_simulation"
    ORCHESTRATION = "orchestration"
    
    # Summarization
    EXECUTIVE_SUMMARY = "executive_summary"


class ModelPolicy:
    """Defines routing logic for LLM selection based on task type."""
    
    # Model configuration mapping
    TASK_MODEL_MAP: Dict[TaskType, str] = {
        # Use GPT-4o-mini for all financial reasoning
        TaskType.DEBT_ANALYSIS: settings.default_model,
        TaskType.SAVINGS_STRATEGY: settings.default_model,
        TaskType.BUDGET_OPTIMIZATION: settings.default_model,
        TaskType.RISK_SCORING: settings.default_model,
        TaskType.SCENARIO_SIMULATION: settings.default_model,
        TaskType.ORCHESTRATION: settings.default_model,
        TaskType.EXECUTIVE_SUMMARY: settings.default_model,
        
        # Cheaper models for simple tasks (if needed)
        TaskType.TEXT_EXTRACTION: settings.backup_model,
        TaskType.DATA_NORMALIZATION: settings.backup_model,
    }
    
    # Token limits per task type
    TOKEN_LIMITS: Dict[TaskType, int] = {
        TaskType.DEBT_ANALYSIS: 2000,
        TaskType.SAVINGS_STRATEGY: 2000,
        TaskType.BUDGET_OPTIMIZATION: 2000,
        TaskType.RISK_SCORING: 1500,
        TaskType.SCENARIO_SIMULATION: 2500,
        TaskType.ORCHESTRATION: 3000,
        TaskType.EXECUTIVE_SUMMARY: 1000,
        TaskType.TEXT_EXTRACTION: 500,
        TaskType.DATA_NORMALIZATION: 500,
    }
    
    # Temperature settings per task type
    TEMPERATURE_SETTINGS: Dict[TaskType, float] = {
        TaskType.DEBT_ANALYSIS: 0.3,  # More deterministic
        TaskType.SAVINGS_STRATEGY: 0.3,
        TaskType.BUDGET_OPTIMIZATION: 0.4,
        TaskType.RISK_SCORING: 0.2,  # Very deterministic
        TaskType.SCENARIO_SIMULATION: 0.5,
        TaskType.ORCHESTRATION: 0.2,
        TaskType.EXECUTIVE_SUMMARY: 0.4,
        TaskType.TEXT_EXTRACTION: 0.0,
        TaskType.DATA_NORMALIZATION: 0.0,
    }
    
    @classmethod
    def get_model_for_task(cls, task_type: TaskType) -> str:
        """
        Get the appropriate model for a given task.
        
        Args:
            task_type: Type of task to perform
            
        Returns:
            Model identifier (e.g., "openai/gpt-4o-mini")
        """
        model = cls.TASK_MODEL_MAP.get(task_type, settings.default_model)
        logger.debug(f"Selected model {model} for task {task_type.value}")
        return model
    
    @classmethod
    def get_token_limit(cls, task_type: TaskType) -> int:
        """Get max tokens for a task type."""
        return cls.TOKEN_LIMITS.get(task_type, 2000)
    
    @classmethod
    def get_temperature(cls, task_type: TaskType) -> float:
        """Get temperature setting for a task type."""
        return cls.TEMPERATURE_SETTINGS.get(task_type, 0.3)
    
    @classmethod
    def get_model_config(cls, task_type: TaskType) -> Dict[str, any]:
        """
        Get complete model configuration for a task.
        
        Args:
            task_type: Type of task to perform
            
        Returns:
            Dictionary with model, max_tokens, and temperature
        """
        return {
            "model": cls.get_model_for_task(task_type),
            "max_tokens": cls.get_token_limit(task_type),
            "temperature": cls.get_temperature(task_type),
        }


# Convenience function for easy access
def get_model_config(task_type: TaskType) -> Dict[str, any]:
    """Get model configuration for a specific task type."""
    return ModelPolicy.get_model_config(task_type)
