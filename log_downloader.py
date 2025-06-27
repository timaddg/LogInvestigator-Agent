"""
Log Downloader module for Log Investigator.
Downloads sample log files from various online sources.
"""

import requests
import json
import os
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse
import time
from utils import print_info, print_success, print_error, print_warning


class LogDownloader:
    """Handles downloading sample log files from various sources."""
    
    def __init__(self):
        """Initialize the log downloader."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'LogInvestigator/1.0'
        })
    
    def get_available_sources(self) -> Dict[str, str]:
        """Get list of available log file sources."""
        return {
            "github_logs": "https://raw.githubusercontent.com/logpai/loghub/master/Apache/Apache_2k.log",
            "sample_json_logs": "https://raw.githubusercontent.com/logpai/loghub/master/JSON/nginx_logs.json",
            "elasticsearch_logs": "https://raw.githubusercontent.com/elastic/examples/master/Common%20Data%20Formats/nginx_logs/nginx_logs",
            "web_server_logs": "https://raw.githubusercontent.com/logpai/loghub/master/Nginx/Nginx_2k.log",
            "hadoop_logs": "https://raw.githubusercontent.com/logpai/loghub/master/Hadoop/Hadoop_2k.log",
            "spark_logs": "https://raw.githubusercontent.com/logpai/loghub/master/Spark/Spark_2k.log",
            "zookeeper_logs": "https://raw.githubusercontent.com/logpai/loghub/master/Zookeeper/Zookeeper_2k.log",
            "hpc_logs": "https://raw.githubusercontent.com/logpai/loghub/master/HPC/HPC_2k.log"
        }
    
    def download_logs(self, source_name: str, output_file: str = None) -> Optional[str]:
        """Download logs from a specific source."""
        sources = self.get_available_sources()
        
        if source_name not in sources:
            print_error(f"Unknown source: {source_name}")
            print_info("Available sources:")
            for name in sources.keys():
                print(f"  - {name}")
            return None
        
        url = sources[source_name]
        output_file = output_file or f"{source_name}.log"
        
        try:
            print_info(f"Downloading logs from {source_name}...")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # Save the raw log file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            print_success(f"Downloaded {len(response.text)} characters to {output_file}")
            return output_file
            
        except requests.exceptions.RequestException as e:
            print_error(f"Failed to download from {source_name}: {e}")
            return None
    
    def download_and_convert_to_json(self, source_name: str, output_file: str = None) -> Optional[str]:
        """Download logs and convert to JSON format for analysis."""
        raw_file = self.download_logs(source_name)
        if not raw_file:
            return None
        
        output_file = output_file or f"{source_name}_converted.json"
        
        try:
            print_info("Converting logs to JSON format...")
            
            # Read the raw log file
            with open(raw_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Convert to JSON format (simplified conversion)
            json_logs = self._convert_to_json(content, source_name)
            
            # Save as JSON
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(json_logs, f, indent=2)
            
            print_success(f"Converted and saved to {output_file}")
            return output_file
            
        except Exception as e:
            print_error(f"Failed to convert logs: {e}")
            return None
    
    def _convert_to_json(self, content: str, source_type: str) -> List[Dict[str, Any]]:
        """Convert raw log content to JSON format."""
        lines = content.strip().split('\n')
        json_logs = []
        
        for i, line in enumerate(lines):
            if not line.strip():
                continue
                
            # Create a basic JSON log entry
            log_entry = {
                "timestamp": self._extract_timestamp(line, source_type),
                "level": self._extract_level(line, source_type),
                "service": source_type,
                "message": line.strip(),
                "line_number": i + 1,
                "source": source_type
            }
            
            # Add additional fields based on source type
            if "nginx" in source_type.lower():
                log_entry.update(self._parse_nginx_log(line))
            elif "apache" in source_type.lower():
                log_entry.update(self._parse_apache_log(line))
            elif "hadoop" in source_type.lower():
                log_entry.update(self._parse_hadoop_log(line))
            
            json_logs.append(log_entry)
        
        return json_logs
    
    def _extract_timestamp(self, line: str, source_type: str) -> str:
        """Extract timestamp from log line."""
        import re
        from datetime import datetime
        
        # Common timestamp patterns
        patterns = [
            r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})',
            r'(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2})',
            r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, line)
            if match:
                return match.group(1)
        
        # If no timestamp found, use current time
        return datetime.now().isoformat()
    
    def _extract_level(self, line: str, source_type: str) -> str:
        """Extract log level from log line."""
        line_lower = line.lower()
        
        if any(word in line_lower for word in ['error', 'err', 'failed', 'failure']):
            return 'ERROR'
        elif any(word in line_lower for word in ['warn', 'warning']):
            return 'WARN'
        elif any(word in line_lower for word in ['debug']):
            return 'DEBUG'
        else:
            return 'INFO'
    
    def _parse_nginx_log(self, line: str) -> Dict[str, Any]:
        """Parse Nginx log line."""
        import re
        
        # Nginx log format: IP - - [timestamp] "method path status size"
        pattern = r'(\S+) - - \[([^\]]+)\] "(\S+) (\S+) (\S+)" (\d+) (\d+)'
        match = re.match(pattern, line)
        
        if match:
            return {
                "ip_address": match.group(1),
                "request_method": match.group(3),
                "request_path": match.group(4),
                "http_version": match.group(5),
                "status_code": int(match.group(6)),
                "response_size": int(match.group(7))
            }
        
        return {}
    
    def _parse_apache_log(self, line: str) -> Dict[str, Any]:
        """Parse Apache log line."""
        import re
        
        # Apache log format: IP - - [timestamp] "method path status size"
        pattern = r'(\S+) - - \[([^\]]+)\] "(\S+) (\S+) (\S+)" (\d+) (\d+)'
        match = re.match(pattern, line)
        
        if match:
            return {
                "ip_address": match.group(1),
                "request_method": match.group(3),
                "request_path": match.group(4),
                "http_version": match.group(5),
                "status_code": int(match.group(6)),
                "response_size": int(match.group(7))
            }
        
        return {}
    
    def _parse_hadoop_log(self, line: str) -> Dict[str, Any]:
        """Parse Hadoop log line."""
        import re
        
        # Extract common Hadoop log patterns
        patterns = {
            "job_id": r'job_(\d+_\d+)',
            "task_id": r'task_(\d+_\d+_\d+)',
            "container_id": r'container_(\d+_\d+_\d+_\d+)',
        }
        
        result = {}
        for key, pattern in patterns.items():
            match = re.search(pattern, line)
            if match:
                result[key] = match.group(1)
        
        return result
    
    def list_sources(self) -> None:
        """List all available log sources."""
        sources = self.get_available_sources()
        print_info("Available log sources:")
        print()
        
        for name, url in sources.items():
            print(f"  📁 {name}")
            print(f"     URL: {url}")
            print()
    
    def download_multiple_sources(self, source_names: List[str], output_dir: str = "downloaded_logs") -> List[str]:
        """Download multiple log sources."""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        downloaded_files = []
        
        for source_name in source_names:
            output_file = os.path.join(output_dir, f"{source_name}.log")
            result = self.download_logs(source_name, output_file)
            if result:
                downloaded_files.append(result)
            time.sleep(1)  # Be nice to servers
        
        return downloaded_files 