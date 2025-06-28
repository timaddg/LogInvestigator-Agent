"""
Log Loader module for Log Investigator.
Handles loading and parsing of log files in various formats.
"""

import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
import re
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

from utils.utils import print_info, print_success, print_error, print_warning


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
                content = f.read().strip()
            
            # Try to parse as regular JSON array first
            try:
                logs = json.loads(content)
                if isinstance(logs, list):
                    self._validate_logs(logs)
                    print(f"✅ Loaded {len(logs)} log entries from {self.file_path}")
                    return logs
            except json.JSONDecodeError:
                pass
            
            # If that fails, try to parse as JSON Lines (one JSON object per line)
            logs = []
            lines = content.split('\n')
            for i, line in enumerate(lines):
                line = line.strip()
                if not line:
                    continue
                try:
                    log_entry = json.loads(line)
                    logs.append(log_entry)
                except json.JSONDecodeError as e:
                    print(f"⚠️ Warning: Skipping invalid JSON at line {i+1}: {e}")
                    continue
            
            if not logs:
                raise ValueError("No valid JSON entries found in file")
            
            self._validate_logs(logs)
            print(f"✅ Loaded {len(logs)} log entries from {self.file_path} (JSON Lines format)")
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
        
        # Validate each log entry and normalize field names
        for i, log in enumerate(logs):
            if not isinstance(log, dict):
                raise ValueError(f"Log entry {i} must be a JSON object")
            
            # Normalize field names for consistency
            if 'time' in log and 'timestamp' not in log:
                log['timestamp'] = log['time']
            if 'remote_ip' in log and 'ip_address' not in log:
                log['ip_address'] = log['remote_ip']
            
            # Add missing required fields with defaults
            if 'timestamp' not in log:
                log['timestamp'] = 'unknown'
            if 'level' not in log:
                # Try to infer level from response code or other fields
                if 'response' in log:
                    response = log['response']
                    if isinstance(response, int):
                        if response >= 500:
                            log['level'] = 'ERROR'
                        elif response >= 400:
                            log['level'] = 'WARN'
                        else:
                            log['level'] = 'INFO'
                    else:
                        log['level'] = 'INFO'
                else:
                    log['level'] = 'INFO'
            if 'message' not in log:
                # Create a message from available fields
                if 'request' in log:
                    log['message'] = f"HTTP request: {log['request']}"
                elif 'remote_ip' in log:
                    log['message'] = f"Request from {log['remote_ip']}"
                else:
                    log['message'] = "Log entry"
    
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