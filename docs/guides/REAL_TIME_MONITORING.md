# Real-Time Log Monitoring Guide

This guide explains how to use Log Investigator's real-time monitoring capabilities to detect issues during deployment and production.

## 🎯 **Overview**

The real-time monitoring system allows you to:
- **Monitor log files** in real-time for critical issues
- **Track system metrics** (CPU, memory, disk usage)
- **Watch Kubernetes logs** for containerized applications
- **Receive instant alerts** when problems are detected
- **Get AI-powered analysis** of log patterns

## 🚀 **Quick Start**

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Set Up Environment

Add these variables to your `.env` file:

```env
# Real-time monitoring configuration
MONITOR_SCAN_INTERVAL=30
MONITOR_BUFFER_SIZE=100
MONITOR_ALERT_THRESHOLD=5

# Your existing Gemini configuration
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.5-pro
```

### 3. Start Monitoring

#### **Deployment Monitoring**
```bash
python logic/monitors/monitor_cli.py deployment /var/log/app.log /var/log/nginx/access.log
```

#### **Production Monitoring**
```bash
python logic/monitors/monitor_cli.py production /var/log/app.log
```

#### **Pipeline Monitoring**
```bash
python logic/monitors/monitor_cli.py pipeline
```

## 📊 **Monitoring Modes**

### **1. Deployment Monitoring**

Perfect for monitoring during application deployment:

```bash
python logic/monitors/monitor_cli.py deployment /path/to/logs
```

**Watches for:**
- Deployment failures
- Health check failures
- Service unavailability
- Connection timeouts
- Rollback events

**Features:**
- ✅ File monitoring
- ✅ System metrics
- ✅ Deployment-specific patterns
- ✅ Real-time alerts

### **2. Production Monitoring**

Comprehensive monitoring for production environments:

```bash
python logic/monitors/monitor_cli.py production /var/log/app.log
```

**Watches for:**
- Out of memory errors
- Disk space issues
- Database connection failures
- Authentication failures
- Rate limiting issues
- Service downtime

**Features:**
- ✅ File monitoring
- ✅ System metrics
- ✅ Kubernetes logs
- ✅ Production-specific patterns
- ✅ AI analysis

### **3. Pipeline Monitoring**

Monitors CI/CD pipeline logs:

```bash
python logic/monitors/monitor_cli.py pipeline
```

**Watches for:**
- Build failures
- Test failures
- Deployment failures
- Lint errors
- Security scan failures
- Dependency conflicts

**Features:**
- ✅ Pipeline log monitoring
- ✅ Pipeline-specific patterns
- ✅ Real-time alerts

### **4. Custom Monitoring**

Flexible monitoring configuration:

```bash
# Monitor only files
python logic/monitors/monitor_cli.py custom /var/log/app.log --no-system

# Monitor with Kubernetes
python logic/monitors/monitor_cli.py custom /var/log/app.log --kubernetes

# Monitor only system metrics
python logic/monitors/monitor_cli.py custom --no-files
```

## 🔧 **Configuration Options**

### **Environment Variables**

| Variable | Default | Description |
|----------|---------|-------------|
| `MONITOR_SCAN_INTERVAL` | 30 | Seconds between scans |
| `MONITOR_BUFFER_SIZE` | 100 | Number of logs to buffer |
| `MONITOR_ALERT_THRESHOLD` | 5 | Critical issues before AI analysis |

### **Critical Patterns**

The system automatically detects these patterns:

**General Issues:**
- `error`, `exception`, `failed`, `timeout`
- `connection refused`, `out of memory`
- `disk full`, `service unavailable`
- `crash`, `segmentation fault`, `oom`, `panic`, `fatal`

**Deployment Issues:**
- `deployment failed`, `rollback`, `health check failed`
- `service unavailable`, `connection refused`, `timeout`

**Production Issues:**
- `out of memory`, `disk full`, `database connection failed`
- `authentication failed`, `rate limit exceeded`, `service down`

**Pipeline Issues:**
- `build failed`, `test failed`, `deployment failed`
- `lint error`, `security scan failed`, `dependency conflict`

## 📱 **Alert System**

### **Alert Types**

1. **Immediate Alerts**: Critical issues trigger instant notifications
2. **Analysis Alerts**: AI-powered analysis of log patterns
3. **Status Updates**: Regular monitoring status

### **Alert Format**

```json
{
  "timestamp": "2024-01-15T10:30:15Z",
  "title": "🚨 CRITICAL ISSUE DETECTED",
  "content": {
    "message": "Database connection failed",
    "source": "file:/var/log/app.log",
    "level": "ERROR"
  },
  "type": "real_time_alert"
}
```

### **Custom Alert Callbacks**

You can add custom alert handlers:

```python
from logic.monitors import RealTimeMonitor

def my_alert_handler(alert):
    # Send to Slack, email, etc.
    print(f"ALERT: {alert['title']}")

monitor = RealTimeMonitor()
monitor.add_alert_callback(my_alert_handler)
```

## 🐳 **Kubernetes Integration**

### **Prerequisites**

- `kubectl` installed and configured
- Access to Kubernetes cluster

### **Usage**

```bash
# Monitor with Kubernetes logs
python logic/monitors/monitor_cli.py production /var/log/app.log

# Custom monitoring with Kubernetes
python logic/monitors/monitor_cli.py custom /var/log/app.log --kubernetes
```

### **Kubernetes Monitoring Features**

- ✅ Real-time pod logs
- ✅ Container-level monitoring
- ✅ Service health checks
- ✅ Resource usage tracking

## 🔍 **AI Analysis**

The system uses Gemini 2.5 Pro to analyze log patterns:

### **Analysis Triggers**

- When critical issue threshold is reached
- Periodic analysis of log buffer
- Pattern detection in real-time

### **Analysis Output**

```
📊 LOG ANALYSIS UPDATE

## CRITICAL SEVERITY
- Database connection failures increasing
- Memory usage approaching limits

## HIGH SEVERITY  
- Multiple authentication failures
- Service response times degrading

## MEDIUM SEVERITY
- Cache miss rates elevated
- Disk I/O performance issues

## OVERVIEW
System showing signs of resource exhaustion and connectivity issues.

## KEY METRICS
- Error rate: 15% (increased from 5%)
- Response time: 2.5s (increased from 0.8s)

## RECOMMENDED ACTIONS
- Scale database connections
- Increase memory allocation
- Investigate authentication service
```

## 🚨 **Troubleshooting**

### **Common Issues**

#### **"kubectl not found"**
```bash
# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/
```

#### **"Permission denied" for log files**
```bash
# Check file permissions
ls -la /var/log/app.log

# Add read permissions
sudo chmod 644 /var/log/app.log
```

#### **"No logs found"**
```bash
# Check if log files exist
ls -la /var/log/

# Test with sample log
echo "2024-01-15 10:30:15 [INFO] Test log entry" >> /var/log/app.log
```

### **Performance Tuning**

#### **High CPU Usage**
```env
# Increase scan interval
MONITOR_SCAN_INTERVAL=60

# Reduce buffer size
MONITOR_BUFFER_SIZE=50
```

#### **Memory Usage**
```env
# Reduce buffer size
MONITOR_BUFFER_SIZE=50

# Increase alert threshold
MONITOR_ALERT_THRESHOLD=10
```

## 📈 **Integration Examples**

### **Docker Compose**

```yaml
version: '3.8'
services:
  log-monitor:
    build: .
    volumes:
      - /var/log:/var/log:ro
      - ./logs:/app/logs
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - MONITOR_SCAN_INTERVAL=30
    command: python logic/monitors/monitor_cli.py production /var/log/app.log
```

### **Kubernetes Deployment**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: log-monitor
spec:
  replicas: 1
  selector:
    matchLabels:
      app: log-monitor
  template:
    metadata:
      labels:
        app: log-monitor
    spec:
      containers:
      - name: log-monitor
        image: log-investigator:latest
        env:
        - name: GEMINI_API_KEY
          valueFrom:
            secretKeyRef:
              name: gemini-secret
              key: api-key
        - name: MONITOR_SCAN_INTERVAL
          value: "30"
        volumeMounts:
        - name: app-logs
          mountPath: /var/log
        command: ["python", "logic/monitors/monitor_cli.py", "production", "/var/log/app.log"]
      volumes:
      - name: app-logs
        hostPath:
          path: /var/log
```

### **CI/CD Pipeline Integration**

```yaml
# GitHub Actions
- name: Monitor Deployment
  run: |
    python logic/monitors/monitor_cli.py deployment /tmp/deploy.log &
    MONITOR_PID=$!
    
    # Run deployment
    ./deploy.sh > /tmp/deploy.log 2>&1
    
    # Stop monitoring
    kill $MONITOR_PID
```

## 🎯 **Best Practices**

### **1. Start Small**
- Begin with file monitoring only
- Add system metrics gradually
- Enable Kubernetes monitoring last

### **2. Configure Alerts**
- Set appropriate thresholds
- Use custom alert callbacks
- Monitor alert frequency

### **3. Resource Management**
- Monitor system resources
- Adjust buffer sizes
- Tune scan intervals

### **4. Security**
- Use read-only log access
- Secure API keys
- Monitor access logs

### **5. Maintenance**
- Rotate log files
- Clean up old alerts
- Update patterns regularly

## 📚 **Advanced Usage**

### **Custom Pattern Detection**

```python
from logic.monitors import RealTimeMonitor

monitor = RealTimeMonitor()

# Add custom patterns
monitor.critical_patterns.extend([
    "custom error pattern",
    "specific failure message"
])

monitor.start_monitoring(["/var/log/app.log"])
```

### **Integration with External Systems**

```python
import requests

def slack_alert(alert):
    webhook_url = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
    payload = {
        "text": f"🚨 {alert['title']}\n{alert['content']}"
    }
    requests.post(webhook_url, json=payload)

monitor = RealTimeMonitor()
monitor.add_alert_callback(slack_alert)
```

## 🎉 **Summary**

The real-time monitoring system transforms your Log Investigator from a static analysis tool into a dynamic, proactive monitoring solution that can:

- ✅ **Detect issues instantly** during deployment and production
- ✅ **Provide AI-powered analysis** of log patterns
- ✅ **Monitor multiple sources** (files, system, Kubernetes)
- ✅ **Send real-time alerts** for critical issues
- ✅ **Scale with your infrastructure** needs

Start monitoring today and catch issues before they become problems! 🚀 