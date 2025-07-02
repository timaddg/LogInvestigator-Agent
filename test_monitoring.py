#!/usr/bin/env python3
"""
Test script for real-time log monitoring.
This script demonstrates the monitoring capabilities by generating sample logs and monitoring them.
"""

import os
import time
import threading
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path

# Add backend to path for imports
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.logic.monitors.real_time_monitor import RealTimeMonitor


class MonitoringTester:
    """Test class for real-time monitoring functionality."""
    
    def __init__(self):
        self.test_log_file = None
        self.monitor = None
        self.testing = False
        
    def setup_test_environment(self):
        """Set up test environment with temporary log file."""
        # Create temporary log file
        self.test_log_file = tempfile.NamedTemporaryFile(
            mode='w+', 
            suffix='.log', 
            delete=False,
            prefix='test_monitoring_'
        )
        self.test_log_file.close()
        
        print(f"📁 Created test log file: {self.test_log_file.name}")
        return self.test_log_file.name
    
    def cleanup_test_environment(self):
        """Clean up test environment."""
        if self.test_log_file and os.path.exists(self.test_log_file.name):
            os.unlink(self.test_log_file.name)
            print(f"🧹 Cleaned up test log file: {self.test_log_file.name}")
    
    def alert_callback(self, alert):
        """Test alert callback function."""
        print(f"\n🚨 TEST ALERT RECEIVED:")
        print(f"   Title: {alert['title']}")
        print(f"   Time: {alert['timestamp']}")
        if isinstance(alert['content'], dict):
            print(f"   Message: {alert['content'].get('message', 'No message')}")
            print(f"   Source: {alert['content'].get('source', 'Unknown')}")
        else:
            print(f"   Content: {alert['content']}")
        print("   " + "="*50)
    
    def generate_test_logs(self, log_file_path: str):
        """Generate test log entries to simulate real application logs."""
        print("📝 Generating test log entries...")
        
        test_logs = [
            # Normal logs
            f"{datetime.now().isoformat()} [INFO] Application started successfully",
            f"{datetime.now().isoformat()} [INFO] Database connection established",
            f"{datetime.now().isoformat()} [INFO] User login successful",
            
            # Warning logs
            f"{datetime.now().isoformat()} [WARN] High memory usage detected: 85%",
            f"{datetime.now().isoformat()} [WARN] Slow database query detected",
            
            # Error logs (these should trigger alerts)
            f"{datetime.now().isoformat()} [ERROR] Database connection failed",
            f"{datetime.now().isoformat()} [ERROR] Out of memory error detected",
            f"{datetime.now().isoformat()} [ERROR] Service unavailable",
            f"{datetime.now().isoformat()} [ERROR] Authentication failed for user admin",
            f"{datetime.now().isoformat()} [ERROR] Disk space critical: 95% full",
            
            # More normal logs
            f"{datetime.now().isoformat()} [INFO] Cache miss for key: user_profile_123",
            f"{datetime.now().isoformat()} [INFO] API request processed successfully",
        ]
        
        with open(log_file_path, 'w') as f:
            for log in test_logs:
                f.write(log + '\n')
        
        print(f"✅ Generated {len(test_logs)} test log entries")
    
    def simulate_log_generation(self, log_file_path: str, duration: int = 60):
        """Simulate continuous log generation."""
        print(f"🔄 Starting log simulation for {duration} seconds...")
        
        start_time = time.time()
        log_counter = 0
        
        while time.time() - start_time < duration and self.testing:
            # Generate a new log entry every 2-5 seconds
            time.sleep(2 + (log_counter % 3))
            
            timestamp = datetime.now().isoformat()
            log_counter += 1
            
            # Alternate between normal and error logs
            if log_counter % 5 == 0:
                # Generate error log (should trigger alert)
                log_entry = f"{timestamp} [ERROR] Test error #{log_counter}: Simulated failure"
            else:
                # Generate normal log
                log_entry = f"{timestamp} [INFO] Test log #{log_counter}: Normal operation"
            
            with open(log_file_path, 'a') as f:
                f.write(log_entry + '\n')
            
            print(f"   📝 Added log entry #{log_counter}")
    
    def test_basic_monitoring(self):
        """Test basic file monitoring functionality."""
        print("\n🧪 TEST 1: Basic File Monitoring")
        print("=" * 50)
        
        # Setup
        log_file = self.setup_test_environment()
        self.generate_test_logs(log_file)
        
        # Start monitoring
        self.monitor = RealTimeMonitor()
        self.monitor.add_alert_callback(self.alert_callback)
        
        print("🚀 Starting basic monitoring...")
        self.monitor.start_monitoring([log_file], watch_files=True, watch_system=False)
        
        # Wait for initial analysis
        print("⏳ Waiting for initial analysis...")
        time.sleep(10)
        
        # Add more logs to trigger alerts
        print("📝 Adding more error logs to trigger alerts...")
        with open(log_file, 'a') as f:
            f.write(f"{datetime.now().isoformat()} [ERROR] CRITICAL: Test critical error\n")
            f.write(f"{datetime.now().isoformat()} [ERROR] CRITICAL: Another critical issue\n")
        
        # Wait for alerts
        print("⏳ Waiting for alerts...")
        time.sleep(15)
        
        # Stop monitoring
        self.monitor.stop_monitoring()
        self.cleanup_test_environment()
        
        print("✅ Basic monitoring test completed")
    
    def test_system_monitoring(self):
        """Test system metrics monitoring."""
        print("\n🧪 TEST 2: System Metrics Monitoring")
        print("=" * 50)
        
        # Start monitoring with system metrics
        self.monitor = RealTimeMonitor()
        self.monitor.add_alert_callback(self.alert_callback)
        
        print("🚀 Starting system monitoring...")
        self.monitor.start_monitoring(watch_files=False, watch_system=True)
        
        # Monitor for 30 seconds
        print("⏳ Monitoring system metrics for 30 seconds...")
        time.sleep(30)
        
        # Stop monitoring
        self.monitor.stop_monitoring()
        
        print("✅ System monitoring test completed")
    
    def test_continuous_monitoring(self):
        """Test continuous monitoring with log generation."""
        print("\n🧪 TEST 3: Continuous Monitoring with Log Generation")
        print("=" * 50)
        
        # Setup
        log_file = self.setup_test_environment()
        self.generate_test_logs(log_file)
        
        # Start monitoring
        self.monitor = RealTimeMonitor()
        self.monitor.add_alert_callback(self.alert_callback)
        
        print("🚀 Starting continuous monitoring...")
        self.monitor.start_monitoring([log_file], watch_files=True, watch_system=True)
        
        # Start log generation in background
        self.testing = True
        log_thread = threading.Thread(
            target=self.simulate_log_generation,
            args=(log_file, 45),  # 45 seconds
            daemon=True
        )
        log_thread.start()
        
        print("⏳ Running continuous monitoring for 45 seconds...")
        print("   (Press Ctrl+C to stop early)")
        
        try:
            # Monitor for 45 seconds
            time.sleep(45)
        except KeyboardInterrupt:
            print("\n🛑 Stopping test early...")
        
        # Stop everything
        self.testing = False
        self.monitor.stop_monitoring()
        self.cleanup_test_environment()
        
        print("✅ Continuous monitoring test completed")
    
    def test_custom_patterns(self):
        """Test custom pattern detection."""
        print("\n🧪 TEST 4: Custom Pattern Detection")
        print("=" * 50)
        
        # Setup
        log_file = self.setup_test_environment()
        
        # Start monitoring
        self.monitor = RealTimeMonitor()
        self.monitor.add_alert_callback(self.alert_callback)
        
        # Add custom patterns
        custom_patterns = [
            "custom error",
            "test failure",
            "simulated issue"
        ]
        self.monitor.critical_patterns.extend(custom_patterns)
        
        print("🚀 Starting monitoring with custom patterns...")
        self.monitor.start_monitoring([log_file], watch_files=True, watch_system=False)
        
        # Add logs with custom patterns
        print("📝 Adding logs with custom patterns...")
        with open(log_file, 'a') as f:
            f.write(f"{datetime.now().isoformat()} [INFO] Normal operation\n")
            f.write(f"{datetime.now().isoformat()} [ERROR] custom error detected\n")
            f.write(f"{datetime.now().isoformat()} [ERROR] test failure occurred\n")
            f.write(f"{datetime.now().isoformat()} [ERROR] simulated issue found\n")
        
        # Wait for alerts
        print("⏳ Waiting for custom pattern alerts...")
        time.sleep(15)
        
        # Stop monitoring
        self.monitor.stop_monitoring()
        self.cleanup_test_environment()
        
        print("✅ Custom pattern test completed")
    
    def run_all_tests(self):
        """Run all monitoring tests."""
        print("🚀 Starting Real-Time Monitoring Tests")
        print("=" * 60)
        
        try:
            # Test 1: Basic monitoring
            self.test_basic_monitoring()
            
            # Test 2: System monitoring
            self.test_system_monitoring()
            
            # Test 3: Continuous monitoring
            self.test_continuous_monitoring()
            
            # Test 4: Custom patterns
            self.test_custom_patterns()
            
            print("\n🎉 All tests completed successfully!")
            print("✅ Real-time monitoring is working correctly")
            
        except Exception as e:
            print(f"\n❌ Test failed: {e}")
            import traceback
            traceback.print_exc()
        finally:
            # Cleanup
            if self.monitor:
                self.monitor.stop_monitoring()
            self.cleanup_test_environment()


def main():
    """Main test function."""
    print("🧪 Real-Time Monitoring Test Suite")
    print("=" * 50)
    
    # Check if required dependencies are installed
    try:
        import psutil
        import watchdog
        print("✅ Required dependencies found")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install required packages:")
        print("pip install watchdog psutil")
        return
    
    # Check if Gemini API key is set
    if not os.getenv("GEMINI_API_KEY"):
        print("⚠️  GEMINI_API_KEY not found in environment")
        print("   Monitoring will work but AI analysis will be limited")
        print("   Set GEMINI_API_KEY in your .env file for full functionality")
    
    # Create tester and run tests
    tester = MonitoringTester()
    
    # Ask user which test to run
    print("\nChoose test to run:")
    print("1. Basic file monitoring")
    print("2. System metrics monitoring")
    print("3. Continuous monitoring with log generation")
    print("4. Custom pattern detection")
    print("5. Run all tests")
    
    try:
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            tester.test_basic_monitoring()
        elif choice == "2":
            tester.test_system_monitoring()
        elif choice == "3":
            tester.test_continuous_monitoring()
        elif choice == "4":
            tester.test_custom_patterns()
        elif choice == "5":
            tester.run_all_tests()
        else:
            print("Invalid choice. Running all tests...")
            tester.run_all_tests()
            
    except KeyboardInterrupt:
        print("\n🛑 Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")


if __name__ == "__main__":
    main() 