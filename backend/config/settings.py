"""
Configuration settings for the AI Financial Coach application.
Loads environment variables and provides centralized configuration.
"""

import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # OpenRouter API Configuration
    openrouter_api_key: str
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    
    # Model Configuration
    default_model: str = "openai/gpt-4o-mini"
    backup_model: str = "openai/gpt-3.5-turbo"
    
    # MongoDB Configuration
    mongodb_uri: str
    mongodb_db_name: str = "financial_coach"
    mongodb_collection: str = "analyses"
    
    # HuggingFace Configuration
    huggingface_token: Optional[str] = None
    
    # PaddleOCR Configuration
    paddleocr_lang: str = "en"  # Language: en, ch, french, german, korean, japan
    paddleocr_use_gpu: bool = False  # Set to True if you have GPU
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True
    
    # File Upload Configuration
    max_upload_size: int = 10485760  # 10MB
    allowed_extensions: str = "pdf,csv"
    
    # Data Directories
    data_dir: str = "./data"
    demo_statements_dir: str = "./data/demo_statements"
    processed_dir: str = "./data/processed"
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "./logs/app.log"
    
    # Cost Monitoring
    enable_cost_tracking: bool = True
    cost_log_file: str = "./logs/cost_tracking.json"
    
    # Cache Configuration
    enable_cache: bool = True
    cache_expiry_hours: int = 24
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    @property
    def allowed_extensions_list(self) -> list[str]:
        """Return allowed file extensions as a list."""
        return [ext.strip() for ext in self.allowed_extensions.split(",")]
    
    def ensure_directories(self) -> None:
        """Create necessary directories if they don't exist."""
        directories = [
            self.data_dir,
            self.demo_statements_dir,
            self.processed_dir,
            os.path.dirname(self.log_file),
            os.path.dirname(self.cost_log_file),
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)


# Global settings instance
settings = Settings()

# Ensure all directories exist on import
settings.ensure_directories()
