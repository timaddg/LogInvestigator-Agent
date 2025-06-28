"""
Configuration management for Log Investigator.
Handles environment variables and application settings.
"""

import os
from dotenv import load_dotenv
from typing import Optional


class Config:
    """Configuration class for Log Investigator."""
    
    def __init__(self):
        """Initialize configuration with environment variables."""
        load_dotenv()
        self._validate_required_vars()
    
    def _validate_required_vars(self) -> None:
        """Validate that required environment variables are present."""
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is required in environment variables")
    
    @property
    def gemini_api_key(self) -> str:
        """Get Google Gemini API key from environment."""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY environment variable is required. "
                "Please set it in your .env file or environment."
            )
        return api_key
    
    @property
    def gemini_model(self) -> str:
        """Get Gemini model name from environment."""
        return os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    
    @property
    def gemini_max_tokens(self) -> int:
        """Get maximum tokens for Gemini API."""
        return int(os.getenv("GEMINI_MAX_TOKENS", "2048"))
    
    @property
    def gemini_temperature(self) -> float:
        """Get temperature setting for Gemini API."""
        return float(os.getenv("GEMINI_TEMPERATURE", "0.3"))
    
    @property
    def log_file(self) -> str:
        """Get log file path from environment."""
        return os.getenv("LOG_FILE", "log_investigator.log")
    
    @property
    def log_level(self) -> str:
        """Get log level from environment or use default."""
        return os.getenv("LOG_LEVEL", "INFO")
    
    @property
    def sample_logs_file(self) -> str:
        """Get sample logs file path from environment."""
        return os.getenv("SAMPLE_LOGS_FILE", "data/logs/sample_logs.json")
    
    @property
    def enable_log_optimization(self) -> bool:
        """Check if log optimization is enabled."""
        return os.getenv("ENABLE_LOG_OPTIMIZATION", "true").lower() == "true"
    
    @property
    def max_input_tokens(self) -> int:
        """Get maximum input tokens for optimization."""
        return int(os.getenv("MAX_INPUT_TOKENS", "30000"))
    
    @property
    def max_log_entries(self) -> int:
        """Get maximum log entries for optimization."""
        return int(os.getenv("MAX_LOG_ENTRIES", "1000"))
    
    @property
    def sample_size(self) -> int:
        """Get sample size for log optimization."""
        return int(os.getenv("SAMPLE_SIZE", "500"))
    
    @property
    def secret_key(self) -> str:
        """Get Flask secret key from environment."""
        return os.getenv("SECRET_KEY", "your-secret-key-change-this")


# Global configuration instance
config = Config() 