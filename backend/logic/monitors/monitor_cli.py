"""
CLI interface for real-time log monitoring.
"""

import argparse
import signal
import sys
import time
from typing import List
from pathlib import Path

# Add backend to path for imports
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from logic.monitors.real_time_monitor import (
    RealTimeMonitor, 
    monitor_deployment_logs, 
    monitor_production_logs, 
    monitor_pipeline_logs
)


class MonitorCLI:
    """Command-line interface for real-time monitoring."""
    
    def __init__(self):
        self.monitor = None
        self.running = False
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        print("\n🛑 Shutting down monitoring...")
        if self.monitor:
            self.monitor.stop_monitoring()
        self.running = False
        sys.exit(0)
    
    def _alert_callback(self, alert):
        """Default alert callback that prints to console."""
        print(f"\n🚨 ALERT: {alert['title']}")
        print(f"⏰ Time: {alert['timestamp']}")
        if isinstance(alert['content'], dict):
            print(f"📝 Message: {alert['content'].get('message', 'No message')}")
        else:
            print(f"📝 Content: {alert['content']}")
        print("-" * 50)
    
    def start_deployment_monitoring(self, log_paths: List[str]):
        """Start monitoring for deployment scenarios."""
        print("🚀 Starting deployment monitoring...")
        
        self.monitor = monitor_deployment_logs(log_paths)
        self.monitor.add_alert_callback(self._alert_callback)
        
        print("✅ Deployment monitoring active")
        print("📁 Monitoring log files:", log_paths)
        print("💻 Monitoring system metrics")
        print("🔍 Watching for deployment-specific issues")
        print("\nPress Ctrl+C to stop monitoring")
        
        self._run_monitoring()
    
    def start_production_monitoring(self, log_paths: List[str]):
        """Start monitoring for production scenarios."""
        print("🚀 Starting production monitoring...")
        
        self.monitor = monitor_production_logs(log_paths)
        self.monitor.add_alert_callback(self._alert_callback)
        
        print("✅ Production monitoring active")
        print("📁 Monitoring log files:", log_paths)
        print("💻 Monitoring system metrics")
        print("☸️ Monitoring Kubernetes logs")
        print("🔍 Watching for production-specific issues")
        print("\nPress Ctrl+C to stop monitoring")
        
        self._run_monitoring()
    
    def start_pipeline_monitoring(self):
        """Start monitoring for CI/CD pipeline scenarios."""
        print("🚀 Starting pipeline monitoring...")
        
        self.monitor = monitor_pipeline_logs()
        self.monitor.add_alert_callback(self._alert_callback)
        
        print("✅ Pipeline monitoring active")
        print("📁 Monitoring pipeline log files")
        print("🔍 Watching for pipeline-specific issues")
        print("\nPress Ctrl+C to stop monitoring")
        
        self._run_monitoring()
    
    def start_custom_monitoring(self, log_paths: List[str], 
                              watch_files: bool = True,
                              watch_system: bool = True,
                              watch_kubernetes: bool = False):
        """Start custom monitoring configuration."""
        print("🚀 Starting custom monitoring...")
        
        self.monitor = RealTimeMonitor()
        self.monitor.add_alert_callback(self._alert_callback)
        
        self.monitor.start_monitoring(
            log_paths=log_paths,
            watch_files=watch_files,
            watch_system=watch_system,
            watch_kubernetes=watch_kubernetes
        )
        
        print("✅ Custom monitoring active")
        if log_paths:
            print("📁 Monitoring log files:", log_paths)
        if watch_system:
            print("💻 Monitoring system metrics")
        if watch_kubernetes:
            print("☸️ Monitoring Kubernetes logs")
        print("\nPress Ctrl+C to stop monitoring")
        
        self._run_monitoring()
    
    def _run_monitoring(self):
        """Run the monitoring loop."""
        self.running = True
        
        try:
            while self.running:
                # Print status every 30 seconds
                if self.monitor:
                    status = self.monitor.get_status()
                    print(f"\r📊 Status: Buffer={status['buffer_size']}, "
                          f"Issues={status['issue_count']}, "
                          f"Monitoring={'✅' if status['monitoring'] else '❌'}", end="")
                
                time.sleep(30)
                
        except KeyboardInterrupt:
            print("\n🛑 Shutting down monitoring...")
            if self.monitor:
                self.monitor.stop_monitoring()
        except Exception as e:
            print(f"\n❌ Error during monitoring: {e}")
            if self.monitor:
                self.monitor.stop_monitoring()


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Real-time Log Monitoring for Deployment and Production",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Monitor deployment logs
  python monitor_cli.py deployment /var/log/app.log /var/log/nginx/access.log
  
  # Monitor production environment
  python monitor_cli.py production /var/log/app.log
  
  # Monitor CI/CD pipeline
  python monitor_cli.py pipeline
  
  # Custom monitoring
  python monitor_cli.py custom /var/log/app.log --no-system --kubernetes
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Monitoring mode')
    
    # Deployment monitoring
    deploy_parser = subparsers.add_parser('deployment', help='Monitor deployment logs')
    deploy_parser.add_argument('log_paths', nargs='+', help='Log file paths to monitor')
    
    # Production monitoring
    prod_parser = subparsers.add_parser('production', help='Monitor production logs')
    prod_parser.add_argument('log_paths', nargs='+', help='Log file paths to monitor')
    
    # Pipeline monitoring
    subparsers.add_parser('pipeline', help='Monitor CI/CD pipeline logs')
    
    # Custom monitoring
    custom_parser = subparsers.add_parser('custom', help='Custom monitoring configuration')
    custom_parser.add_argument('log_paths', nargs='*', help='Log file paths to monitor')
    custom_parser.add_argument('--no-files', action='store_true', help='Disable file monitoring')
    custom_parser.add_argument('--no-system', action='store_true', help='Disable system monitoring')
    custom_parser.add_argument('--kubernetes', action='store_true', help='Enable Kubernetes monitoring')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    cli = MonitorCLI()
    
    try:
        if args.command == 'deployment':
            cli.start_deployment_monitoring(args.log_paths)
        elif args.command == 'production':
            cli.start_production_monitoring(args.log_paths)
        elif args.command == 'pipeline':
            cli.start_pipeline_monitoring()
        elif args.command == 'custom':
            cli.start_custom_monitoring(
                log_paths=args.log_paths,
                watch_files=not args.no_files,
                watch_system=not args.no_system,
                watch_kubernetes=args.kubernetes
            )
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 