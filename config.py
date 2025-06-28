"""
Configuration module for Log Investigator.
Handles environment variables and application settings.
"""

import os
from dotenv import load_dotenv
from typing import Optional


class Config:
    """Configuration class to manage application settings."""
    
    def __init__(self):
        """Initialize configuration by loading environment variables."""
        load_dotenv()
        self._validate_required_vars()
    
    def _validate_required_vars(self) -> None:
        """Validate that required environment variables are present."""
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is required in environment variables")
    
    @property
    def gemini_api_key(self) -> Optional[str]:
        """Get Gemini API key from environment."""
        return os.getenv("GEMINI_API_KEY")
    
    @property
    def gemini_model(self) -> str:
        """Get Gemini model name from environment or use default."""
        return os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    
    @property
    def gemini_max_tokens(self) -> int:
        """Get Gemini max tokens from environment or use default."""
        return int(os.getenv("GEMINI_MAX_TOKENS", "2048"))
    
    @property
    def gemini_temperature(self) -> float:
        """Get Gemini temperature from environment or use default."""
        return float(os.getenv("GEMINI_TEMPERATURE", "0.3"))
    
    @property
    def log_file_path(self) -> str:
        """Get log file path from environment or use default."""
        return os.getenv("LOG_FILE", "log_investigator.log")
    
    @property
    def log_level(self) -> str:
        """Get log level from environment or use default."""
        return os.getenv("LOG_LEVEL", "INFO")
    
    @property
    def sample_logs_file(self) -> str:
        """Get sample logs file path from environment or use default."""
        return os.getenv("SAMPLE_LOGS_FILE", "downloaded_logs/web_server_logs.log")
    
    @property
    def max_input_tokens(self) -> int:
        """Get maximum input tokens for AI analysis."""
        return int(os.getenv("MAX_INPUT_TOKENS", "30000"))
    
    @property
    def max_log_entries(self) -> int:
        """Get maximum log entries to send to AI."""
        return int(os.getenv("MAX_LOG_ENTRIES", "1000"))
    
    @property
    def sample_size(self) -> int:
        """Get sample size for large log files."""
        return int(os.getenv("SAMPLE_SIZE", "500"))
    
    @property
    def enable_log_optimization(self) -> bool:
        """Get whether to enable log optimization."""
        return os.getenv("ENABLE_LOG_OPTIMIZATION", "true").lower() == "true"


# Global configuration instance
config = Config() 