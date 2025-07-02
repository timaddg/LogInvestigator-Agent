"""
Real-time monitoring module for Log Investigator.
"""

from .real_time_monitor import (
    RealTimeMonitor,
    monitor_deployment_logs,
    monitor_production_logs,
    monitor_pipeline_logs
)

__all__ = [
    'RealTimeMonitor',
    'monitor_deployment_logs',
    'monitor_production_logs',
    'monitor_pipeline_logs'
] 