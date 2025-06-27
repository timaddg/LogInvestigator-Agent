"""
Log loader module for Log Investigator.
Handles loading and validating log files.
"""

import json
import os
from typing import List, Dict, Any, Optional
from config import config


class LogLoader:
    """Handles loading and validation of log files."""
    
    def __init__(self, file_path: Optional[str] = None):
        """Initialize log loader with file path."""
        self.file_path = file_path or config.sample_logs_file
    
    def load_logs(self) -> Optional[List[Dict[str, Any]]]:
        """Load and validate log data from JSON file."""
        try:
            if not os.path.exists(self.file_path):
                raise FileNotFoundError(f"Log file '{self.file_path}' not found")
            
            with open(self.file_path, 'r') as f:
                logs = json.load(f)
            
            self._validate_logs(logs)
            print(f"✅ Loaded {len(logs)} log entries from {self.file_path}")
            return logs
        
        except FileNotFoundError as e:
            print(f"❌ File error: {e}")
            print(f"Please ensure {self.file_path} exists in the project directory")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing error: {e}")
            print("Please check that the log file contains valid JSON")
            return None
        except Exception as e:
            print(f"❌ Unexpected error loading logs: {e}")
            return None
    
    def _validate_logs(self, logs: Any) -> None:
        """Validate log data structure."""
        if not isinstance(logs, list):
            raise ValueError("Log file must contain a JSON array")
        
        if not logs:
            raise ValueError("Log file is empty")
        
        # Validate each log entry has required fields
        required_fields = ['timestamp', 'level', 'message']
        for i, log in enumerate(logs):
            if not isinstance(log, dict):
                raise ValueError(f"Log entry {i} must be a JSON object")
            
            for field in required_fields:
                if field not in log:
                    raise ValueError(f"Log entry {i} missing required field: {field}")
    
    def get_log_statistics(self, logs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate statistics from log data."""
        if not logs:
            return {}
        
        stats = {
            'total_entries': len(logs),
            'levels': {},
            'services': {},
            'error_count': 0,
            'warning_count': 0,
            'time_range': {
                'earliest': None,
                'latest': None
            }
        }
        
        for log in logs:
            # Count log levels
            level = log.get('level', 'UNKNOWN')
            stats['levels'][level] = stats['levels'].get(level, 0) + 1
            
            # Count services
            service = log.get('service', 'UNKNOWN')
            stats['services'][service] = stats['services'].get(service, 0) + 1
            
            # Count errors and warnings
            if level == 'ERROR':
                stats['error_count'] += 1
            elif level == 'WARN':
                stats['warning_count'] += 1
            
            # Track time range
            timestamp = log.get('timestamp')
            if timestamp:
                if not stats['time_range']['earliest'] or timestamp < stats['time_range']['earliest']:
                    stats['time_range']['earliest'] = timestamp
                if not stats['time_range']['latest'] or timestamp > stats['time_range']['latest']:
                    stats['time_range']['latest'] = timestamp
        
        return stats 