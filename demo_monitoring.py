#!/usr/bin/env python3
"""
Demo script for real-time log monitoring.
Shows practical examples of monitoring different scenarios.
"""

import os
import time
import threading
import tempfile
from datetime import datetime

# Add backend to path for imports
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.logic.monitors.real_time_monitor import (
    RealTimeMonitor,
    monitor_deployment_logs,
    monitor_production_logs,
    monitor_pipeline_logs
)


def demo_alert_callback(alert):
    """Demo alert callback that formats alerts nicely."""
    print(f"\n{'🚨' if 'CRITICAL' in alert['title'] else '📊'} {alert['title']}")
    print(f"⏰ {alert['timestamp']}")
    
    if isinstance(alert['content'], dict):
        print(f"📝 {alert['content'].get('message', 'No message')}")
        print(f"📍 Source: {alert['content'].get('source', 'Unknown')}")
    else:
        print(f"📝 {alert['content']}")
    
    print("─" * 60)


def demo_deployment_monitoring():
    """Demo deployment monitoring scenario."""
    print("\n🚀 DEMO: Deployment Monitoring")
    print("=" * 50)
    
    # Create temporary log file
    log_file = tempfile.NamedTemporaryFile(mode='w+', suffix='.log', delete=False)
    log_file.close()
    
    try:
        # Start deployment monitoring
        monitor = monitor_deployment_logs([log_file.name])
        monitor.add_alert_callback(demo_alert_callback)
        
        print("✅ Deployment monitoring started")
        print("📁 Monitoring log file:", log_file.name)
        print("🔍 Watching for deployment-specific issues")
        
        # Simulate deployment process
        print("\n📦 Simulating deployment process...")
        
        deployment_logs = [
            "2024-01-15T10:00:00 [INFO] Starting deployment of v2.1.0",
            "2024-01-15T10:00:05 [INFO] Building Docker image...",
            "2024-01-15T10:00:10 [INFO] Image built successfully",
            "2024-01-15T10:00:15 [INFO] Pushing to registry...",
            "2024-01-15T10:00:20 [INFO] Image pushed successfully",
            "2024-01-15T10:00:25 [INFO] Updating Kubernetes deployment...",
            "2024-01-15T10:00:30 [ERROR] deployment failed: ImagePullBackOff",
            "2024-01-15T10:00:35 [ERROR] Health check failed: 503 Service Unavailable",
            "2024-01-15T10:00:40 [ERROR] Rolling back to previous version",
            "2024-01-15T10:00:45 [INFO] Rollback completed successfully"
        ]
        
        for i, log in enumerate(deployment_logs):
            with open(log_file.name, 'a') as f:
                f.write(log + '\n')
            print(f"   📝 Added deployment log {i+1}/{len(deployment_logs)}")
            time.sleep(2)
        
        # Wait for analysis
        print("\n⏳ Waiting for AI analysis...")
        time.sleep(10)
        
        # Stop monitoring
        monitor.stop_monitoring()
        print("✅ Deployment monitoring demo completed")
        
    finally:
        # Cleanup
        if os.path.exists(log_file.name):
            os.unlink(log_file.name)


def demo_production_monitoring():
    """Demo production monitoring scenario."""
    print("\n🚀 DEMO: Production Monitoring")
    print("=" * 50)
    
    # Create temporary log file
    log_file = tempfile.NamedTemporaryFile(mode='w+', suffix='.log', delete=False)
    log_file.close()
    
    try:
        # Start production monitoring
        monitor = monitor_production_logs([log_file.name])
        monitor.add_alert_callback(demo_alert_callback)
        
        print("✅ Production monitoring started")
        print("📁 Monitoring log file:", log_file.name)
        print("💻 Monitoring system metrics")
        print("☸️ Monitoring Kubernetes logs (if available)")
        
        # Simulate production issues
        print("\n🏭 Simulating production issues...")
        
        production_logs = [
            "2024-01-15T11:00:00 [INFO] Application started successfully",
            "2024-01-15T11:00:05 [INFO] Database connection established",
            "2024-01-15T11:00:10 [WARN] High memory usage: 85%",
            "2024-01-15T11:00:15 [INFO] Processing user requests",
            "2024-01-15T11:00:20 [ERROR] Database connection failed",
            "2024-01-15T11:00:25 [ERROR] Out of memory error detected",
            "2024-01-15T11:00:30 [ERROR] Authentication failed for user admin",
            "2024-01-15T11:00:35 [ERROR] Rate limit exceeded",
            "2024-01-15T11:00:40 [ERROR] Service unavailable",
            "2024-01-15T11:00:45 [ERROR] Disk space critical: 95% full"
        ]
        
        for i, log in enumerate(production_logs):
            with open(log_file.name, 'a') as f:
                f.write(log + '\n')
            print(f"   📝 Added production log {i+1}/{len(production_logs)}")
            time.sleep(2)
        
        # Wait for analysis
        print("\n⏳ Waiting for AI analysis...")
        time.sleep(10)
        
        # Stop monitoring
        monitor.stop_monitoring()
        print("✅ Production monitoring demo completed")
        
    finally:
        # Cleanup
        if os.path.exists(log_file.name):
            os.unlink(log_file.name)


def demo_pipeline_monitoring():
    """Demo CI/CD pipeline monitoring scenario."""
    print("\n🚀 DEMO: Pipeline Monitoring")
    print("=" * 50)
    
    # Create temporary log file
    log_file = tempfile.NamedTemporaryFile(mode='w+', suffix='.log', delete=False)
    log_file.close()
    
    try:
        # Start pipeline monitoring
        monitor = monitor_pipeline_logs()
        monitor.add_alert_callback(demo_alert_callback)
        
        print("✅ Pipeline monitoring started")
        print("📁 Monitoring pipeline log files")
        print("🔍 Watching for pipeline-specific issues")
        
        # Simulate CI/CD pipeline
        print("\n🔧 Simulating CI/CD pipeline...")
        
        pipeline_logs = [
            "2024-01-15T12:00:00 [INFO] Starting CI/CD pipeline",
            "2024-01-15T12:00:05 [INFO] Running linting checks...",
            "2024-01-15T12:00:10 [ERROR] lint error: Unused import detected",
            "2024-01-15T12:00:15 [INFO] Running unit tests...",
            "2024-01-15T12:00:20 [ERROR] test failed: UserServiceTest.testAuthentication",
            "2024-01-15T12:00:25 [INFO] Running security scan...",
            "2024-01-15T12:00:30 [ERROR] security scan failed: High severity vulnerability found",
            "2024-01-15T12:00:35 [INFO] Building application...",
            "2024-01-15T12:00:40 [ERROR] build failed: Dependency conflict detected",
            "2024-01-15T12:00:45 [ERROR] deployment failed: Pipeline aborted"
        ]
        
        for i, log in enumerate(pipeline_logs):
            with open(log_file.name, 'a') as f:
                f.write(log + '\n')
            print(f"   📝 Added pipeline log {i+1}/{len(pipeline_logs)}")
            time.sleep(2)
        
        # Wait for analysis
        print("\n⏳ Waiting for AI analysis...")
        time.sleep(10)
        
        # Stop monitoring
        monitor.stop_monitoring()
        print("✅ Pipeline monitoring demo completed")
        
    finally:
        # Cleanup
        if os.path.exists(log_file.name):
            os.unlink(log_file.name)


def demo_custom_monitoring():
    """Demo custom monitoring configuration."""
    print("\n🚀 DEMO: Custom Monitoring")
    print("=" * 50)
    
    # Create temporary log file
    log_file = tempfile.NamedTemporaryFile(mode='w+', suffix='.log', delete=False)
    log_file.close()
    
    try:
        # Create custom monitor
        monitor = RealTimeMonitor()
        monitor.add_alert_callback(demo_alert_callback)
        
        # Add custom patterns
        custom_patterns = [
            "custom error",
            "business logic failure",
            "data validation error",
            "external service timeout"
        ]
        monitor.critical_patterns.extend(custom_patterns)
        
        # Start custom monitoring
        monitor.start_monitoring(
            log_paths=[log_file.name],
            watch_files=True,
            watch_system=True,
            watch_kubernetes=False
        )
        
        print("✅ Custom monitoring started")
        print("📁 Monitoring log file:", log_file.name)
        print("💻 Monitoring system metrics")
        print("🔍 Custom patterns:", custom_patterns)
        
        # Simulate custom application
        print("\n🎯 Simulating custom application...")
        
        custom_logs = [
            "2024-01-15T13:00:00 [INFO] Custom application started",
            "2024-01-15T13:00:05 [INFO] Loading configuration...",
            "2024-01-15T13:00:10 [INFO] Connecting to external services...",
            "2024-01-15T13:00:15 [ERROR] custom error: Invalid configuration format",
            "2024-01-15T13:00:20 [INFO] Processing business logic...",
            "2024-01-15T13:00:25 [ERROR] business logic failure: Insufficient funds",
            "2024-01-15T13:00:30 [INFO] Validating user data...",
            "2024-01-15T13:00:35 [ERROR] data validation error: Invalid email format",
            "2024-01-15T13:00:40 [INFO] Calling external API...",
            "2024-01-15T13:00:45 [ERROR] external service timeout: Payment gateway unreachable"
        ]
        
        for i, log in enumerate(custom_logs):
            with open(log_file.name, 'a') as f:
                f.write(log + '\n')
            print(f"   📝 Added custom log {i+1}/{len(custom_logs)}")
            time.sleep(2)
        
        # Wait for analysis
        print("\n⏳ Waiting for AI analysis...")
        time.sleep(10)
        
        # Stop monitoring
        monitor.stop_monitoring()
        print("✅ Custom monitoring demo completed")
        
    finally:
        # Cleanup
        if os.path.exists(log_file.name):
            os.unlink(log_file.name)


def main():
    """Main demo function."""
    print("🎬 Real-Time Monitoring Demo Suite")
    print("=" * 50)
    
    # Check dependencies
    try:
        import psutil
        import watchdog
        print("✅ Required dependencies found")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install required packages:")
        print("pip install watchdog psutil")
        return
    
    # Check Gemini API key
    if not os.getenv("GEMINI_API_KEY"):
        print("⚠️  GEMINI_API_KEY not found in environment")
        print("   Monitoring will work but AI analysis will be limited")
    
    # Show demo options
    print("\nChoose demo to run:")
    print("1. Deployment Monitoring")
    print("2. Production Monitoring")
    print("3. Pipeline Monitoring")
    print("4. Custom Monitoring")
    print("5. Run all demos")
    
    try:
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            demo_deployment_monitoring()
        elif choice == "2":
            demo_production_monitoring()
        elif choice == "3":
            demo_pipeline_monitoring()
        elif choice == "4":
            demo_custom_monitoring()
        elif choice == "5":
            print("\n🎬 Running all demos...")
            demo_deployment_monitoring()
            demo_production_monitoring()
            demo_pipeline_monitoring()
            demo_custom_monitoring()
        else:
            print("Invalid choice. Running all demos...")
            demo_deployment_monitoring()
            demo_production_monitoring()
            demo_pipeline_monitoring()
            demo_custom_monitoring()
        
        print("\n🎉 All demos completed!")
        print("✅ Real-time monitoring is ready for your use cases")
        
    except KeyboardInterrupt:
        print("\n🛑 Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")


if __name__ == "__main__":
    main() 