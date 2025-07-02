"""
Real-time Log Monitor for Log Investigator.
Monitors logs in real-time during deployment and production to detect issues.
"""

import os
import time
import json
import threading
import subprocess
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Callable
from pathlib import Path
import queue
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import psutil
import requests

# Add backend to path for imports
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from config.config import config
from logic.analyzers.ai_analyzer import AIAnalyzer


class RealTimeMonitor:
    """Real-time log monitoring system for deployment and production."""
    
    def __init__(self):
        """Initialize the real-time monitor."""
        self.ai_analyzer = AIAnalyzer()
        self.log_buffer = queue.Queue(maxsize=1000)
        self.alert_callbacks: List[Callable] = []
        self.monitoring = False
        self.observer = Observer()
        
        # Monitoring configuration
        self.scan_interval = int(os.getenv("MONITOR_SCAN_INTERVAL", "30"))  # seconds
        self.buffer_size = int(os.getenv("MONITOR_BUFFER_SIZE", "100"))
        self.alert_threshold = int(os.getenv("MONITOR_ALERT_THRESHOLD", "5"))
        
        # Issue tracking
        self.issue_count = 0
        self.last_analysis = None
        self.critical_patterns = [
            "error", "exception", "failed", "timeout", "connection refused",
            "out of memory", "disk full", "service unavailable", "crash",
            "segmentation fault", "oom", "panic", "fatal"
        ]
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def start_monitoring(self, log_paths: List[str] = None, 
                        watch_files: bool = True,
                        watch_system: bool = True,
                        watch_kubernetes: bool = False) -> None:
        """Start real-time monitoring."""
        if self.monitoring:
            self.logger.warning("Monitoring already active")
            return
        
        self.monitoring = True
        self.logger.info("🚀 Starting real-time log monitoring...")
        
        # Start monitoring threads
        threads = []
        
        if watch_files and log_paths:
            for log_path in log_paths:
                if os.path.exists(log_path):
                    thread = threading.Thread(
                        target=self._monitor_log_file,
                        args=(log_path,),
                        daemon=True
                    )
                    thread.start()
                    threads.append(thread)
                    self.logger.info(f"📁 Monitoring log file: {log_path}")
        
        if watch_system:
            thread = threading.Thread(
                target=self._monitor_system_metrics,
                daemon=True
            )
            thread.start()
            threads.append(thread)
            self.logger.info("💻 Monitoring system metrics")
        
        if watch_kubernetes:
            thread = threading.Thread(
                target=self._monitor_kubernetes_logs,
                daemon=True
            )
            thread.start()
            threads.append(thread)
            self.logger.info("☸️ Monitoring Kubernetes logs")
        
        # Start analysis thread
        analysis_thread = threading.Thread(
            target=self._continuous_analysis,
            daemon=True
        )
        analysis_thread.start()
        
        self.logger.info(f"✅ Real-time monitoring active with {len(threads)} monitors")
    
    def stop_monitoring(self) -> None:
        """Stop real-time monitoring."""
        self.monitoring = False
        self.observer.stop()
        self.observer.join()
        self.logger.info("🛑 Real-time monitoring stopped")
    
    def add_alert_callback(self, callback: Callable) -> None:
        """Add a callback function for alerts."""
        self.alert_callbacks.append(callback)
    
    def _monitor_log_file(self, log_path: str) -> None:
        """Monitor a specific log file for changes."""
        try:
            # Use tail to follow log file
            process = subprocess.Popen(
                ['tail', '-f', log_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            while self.monitoring:
                line = process.stdout.readline()
                if line:
                    self._process_log_line(line.strip(), source=f"file:{log_path}")
                time.sleep(0.1)
                
        except Exception as e:
            self.logger.error(f"Error monitoring log file {log_path}: {e}")
    
    def _monitor_system_metrics(self) -> None:
        """Monitor system metrics for issues."""
        while self.monitoring:
            try:
                # CPU usage
                cpu_percent = psutil.cpu_percent(interval=1)
                if cpu_percent > 90:
                    self._process_log_line(
                        f"CRITICAL: High CPU usage detected: {cpu_percent}%",
                        source="system:metrics"
                    )
                
                # Memory usage
                memory = psutil.virtual_memory()
                if memory.percent > 90:
                    self._process_log_line(
                        f"CRITICAL: High memory usage detected: {memory.percent}%",
                        source="system:metrics"
                    )
                
                # Disk usage
                disk = psutil.disk_usage('/')
                if disk.percent > 90:
                    self._process_log_line(
                        f"CRITICAL: High disk usage detected: {disk.percent}%",
                        source="system:metrics"
                    )
                
                time.sleep(self.scan_interval)
                
            except Exception as e:
                self.logger.error(f"Error monitoring system metrics: {e}")
                time.sleep(self.scan_interval)
    
    def _monitor_kubernetes_logs(self) -> None:
        """Monitor Kubernetes logs using kubectl."""
        while self.monitoring:
            try:
                # Get logs from all pods
                result = subprocess.run(
                    ['kubectl', 'logs', '--tail=10', '--all-containers=true'],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    for line in result.stdout.split('\n'):
                        if line.strip():
                            self._process_log_line(line.strip(), source="kubernetes")
                
                time.sleep(self.scan_interval)
                
            except subprocess.TimeoutExpired:
                self.logger.warning("Kubernetes log fetch timed out")
            except FileNotFoundError:
                self.logger.warning("kubectl not found, skipping Kubernetes monitoring")
                break
            except Exception as e:
                self.logger.error(f"Error monitoring Kubernetes logs: {e}")
                time.sleep(self.scan_interval)
    
    def _process_log_line(self, line: str, source: str) -> None:
        """Process a single log line and check for issues."""
        try:
            # Check for critical patterns
            line_lower = line.lower()
            critical_found = any(pattern in line_lower for pattern in self.critical_patterns)
            
            # Create log entry
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "level": "ERROR" if critical_found else "INFO",
                "message": line,
                "source": source,
                "critical": critical_found
            }
            
            # Add to buffer
            try:
                self.log_buffer.put_nowait(log_entry)
            except queue.Full:
                # Remove oldest entry
                try:
                    self.log_buffer.get_nowait()
                    self.log_buffer.put_nowait(log_entry)
                except queue.Empty:
                    pass
            
            # Immediate alert for critical issues
            if critical_found:
                self._send_alert(f"🚨 CRITICAL ISSUE DETECTED: {line[:100]}...", log_entry)
                
        except Exception as e:
            self.logger.error(f"Error processing log line: {e}")
    
    def _continuous_analysis(self) -> None:
        """Continuously analyze log buffer for patterns."""
        while self.monitoring:
            try:
                # Collect logs from buffer
                logs = []
                while not self.log_buffer.empty() and len(logs) < self.buffer_size:
                    try:
                        log = self.log_buffer.get_nowait()
                        logs.append(log)
                    except queue.Empty:
                        break
                
                if logs:
                    # Analyze logs
                    analysis = self._analyze_logs(logs)
                    if analysis:
                        self._send_alert("📊 LOG ANALYSIS UPDATE", analysis)
                
                time.sleep(self.scan_interval)
                
            except Exception as e:
                self.logger.error(f"Error in continuous analysis: {e}")
                time.sleep(self.scan_interval)
    
    def _analyze_logs(self, logs: List[Dict[str, Any]]) -> Optional[str]:
        """Analyze a batch of logs using AI."""
        try:
            if not logs:
                return None
            
            # Check if we have enough critical issues to warrant analysis
            critical_count = sum(1 for log in logs if log.get('critical', False))
            if critical_count < self.alert_threshold:
                return None
            
            # Prepare logs for AI analysis
            formatted_logs = []
            for log in logs:
                formatted_log = {
                    "timestamp": log.get("timestamp"),
                    "level": log.get("level"),
                    "message": log.get("message"),
                    "source": log.get("source")
                }
                formatted_logs.append(formatted_log)
            
            # Use AI analyzer
            analysis = self.ai_analyzer.analyze_logs(formatted_logs)
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing logs: {e}")
            return None
    
    def _send_alert(self, title: str, content: Any) -> None:
        """Send alert to all registered callbacks."""
        alert = {
            "timestamp": datetime.now().isoformat(),
            "title": title,
            "content": content,
            "type": "real_time_alert"
        }
        
        # Log alert
        self.logger.warning(f"ALERT: {title}")
        
        # Send to callbacks
        for callback in self.alert_callbacks:
            try:
                callback(alert)
            except Exception as e:
                self.logger.error(f"Error in alert callback: {e}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current monitoring status."""
        return {
            "monitoring": self.monitoring,
            "buffer_size": self.log_buffer.qsize(),
            "issue_count": self.issue_count,
            "last_analysis": self.last_analysis,
            "alert_callbacks": len(self.alert_callbacks)
        }


class LogFileWatcher(FileSystemEventHandler):
    """Watchdog handler for log file changes."""
    
    def __init__(self, monitor: RealTimeMonitor):
        self.monitor = monitor
        self.logger = logging.getLogger(__name__)
    
    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(('.log', '.txt')):
            self.logger.info(f"Log file modified: {event.src_path}")
            # The monitor will handle the file reading


# Utility functions for different monitoring scenarios
def monitor_deployment_logs(log_paths: List[str]) -> RealTimeMonitor:
    """Monitor logs during deployment."""
    monitor = RealTimeMonitor()
    
    # Add deployment-specific patterns
    deployment_patterns = [
        "deployment failed", "rollback", "health check failed",
        "service unavailable", "connection refused", "timeout"
    ]
    monitor.critical_patterns.extend(deployment_patterns)
    
    monitor.start_monitoring(log_paths, watch_files=True, watch_system=True)
    return monitor


def monitor_production_logs(log_paths: List[str]) -> RealTimeMonitor:
    """Monitor logs in production environment."""
    monitor = RealTimeMonitor()
    
    # Add production-specific patterns
    production_patterns = [
        "out of memory", "disk full", "database connection failed",
        "authentication failed", "rate limit exceeded", "service down"
    ]
    monitor.critical_patterns.extend(production_patterns)
    
    monitor.start_monitoring(log_paths, watch_files=True, watch_system=True, watch_kubernetes=True)
    return monitor


def monitor_pipeline_logs() -> RealTimeMonitor:
    """Monitor CI/CD pipeline logs."""
    monitor = RealTimeMonitor()
    
    # Add pipeline-specific patterns
    pipeline_patterns = [
        "build failed", "test failed", "deployment failed",
        "lint error", "security scan failed", "dependency conflict"
    ]
    monitor.critical_patterns.extend(pipeline_patterns)
    
    # Monitor common pipeline log locations
    pipeline_logs = [
        "/var/log/ci-cd/pipeline.log",
        "/tmp/pipeline.log",
        "pipeline.log"
    ]
    
    monitor.start_monitoring(pipeline_logs, watch_files=True, watch_system=False)
    return monitor 