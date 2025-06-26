# Online Log Files Guide

Download and analyze real-world log files from various sources using your Log Investigator.

## 🎯 **Why Use Online Log Files?**

- **Real Data**: Analyze actual production logs
- **Variety**: Different systems and formats
- **Learning**: Practice with diverse scenarios
- **Testing**: Validate your analysis skills
- **No Setup**: No need to generate your own logs

## 📋 **Available Log Sources**

### **Web Servers**
- `github_logs` - Apache web server logs
- `web_server_logs` - Nginx web server logs
- `sample_json_logs` - JSON format nginx logs

### **Big Data & Cloud**
- `hadoop_logs` - Hadoop distributed computing
- `spark_logs` - Apache Spark processing

### **Infrastructure**
- `zookeeper_logs` - Apache ZooKeeper
- `hpc_logs` - High Performance Computing
- `elasticsearch_logs` - Elasticsearch search engine

## 🚀 **Quick Start**

### **1. List Available Sources**
```bash
python main.py --list-sources
```

### **2. Download and Analyze**
```bash
# Download nginx logs and analyze
python main.py --download nginx_logs

# Download, convert to JSON, and analyze
python main.py --convert nginx_logs
```

### **3. Use Downloaded Files**
```bash
# Analyze a specific downloaded file
python main.py --file downloaded_logs/nginx_logs.log
```

## 🔧 **Download Options**

### **Download Single Source**
```bash
python download_logs.py --download nginx_logs
```

### **Download All Sources**
```bash
python download_logs.py --download-all
```

### **Download and Convert to JSON**
```bash
python download_logs.py --convert nginx_logs
```

### **Custom Output**
```bash
python download_logs.py --download nginx_logs --output my_nginx.log
```

## 📊 **Log Format Support**

### **Raw Log Formats**
- **Nginx/Apache**: Standard web server logs
- **Hadoop/Spark**: Big data processing logs
- **System Logs**: OS-level logs
- **Application Logs**: Various application formats

### **JSON Conversion**
All logs are automatically converted to JSON format with:
- **timestamp**: Extracted from log entries
- **level**: ERROR, WARN, INFO, DEBUG
- **service**: Source system identifier
- **message**: Original log message
- **additional_fields**: Parsed specific data

## 🎯 **Usage Examples**

### **Analyze Web Server Logs**
```bash
# Download and analyze nginx logs
python main.py --convert nginx_logs
```

### **Analyze Big Data Logs**
```bash
# Download and analyze Hadoop logs
python main.py --convert hadoop_logs
```

### **Analyze System Logs**
```bash
# Download and analyze Windows logs
python main.py --convert windows_logs
```

### **Batch Analysis**
```bash
# Download all sources
python download_logs.py --download-all

# Analyze each downloaded file
python main.py --file downloaded_logs/nginx_logs.log
python main.py --file downloaded_logs/hadoop_logs.log
python main.py --file downloaded_logs/windows_logs.log
```

## 📁 **File Organization**

### **Downloaded Files Structure**
```
log-investigator/
├── downloaded_logs/
│   ├── nginx_logs.log
│   ├── hadoop_logs.log
│   ├── windows_logs.log
│   └── ...
├── nginx_logs_converted.json
├── hadoop_logs_converted.json
└── ...
```

### **File Naming Convention**
- **Raw logs**: `{source_name}.log`
- **JSON converted**: `{source_name}_converted.json`
- **Custom names**: Use `--output` parameter

## 🔍 **Analysis Examples**

### **Web Server Analysis**
```bash
python main.py --convert nginx_logs
```
**What to look for:**
- HTTP status codes (4xx, 5xx errors)
- Request patterns and traffic
- Security issues (failed logins, suspicious IPs)
- Performance bottlenecks

### **Big Data Analysis**
```bash
python main.py --convert hadoop_logs
```
**What to look for:**
- Job failures and errors
- Resource utilization
- Task completion times
- Cluster health issues

### **System Logs Analysis**
```bash
python main.py --convert windows_logs
```
**What to look for:**
- System errors and warnings
- Security events
- Application crashes
- Performance issues

## 🛠️ **Advanced Usage**

### **Custom Analysis Script**
```python
from log_downloader import LogDownloader
from log_investigator import LogInvestigator

# Download specific logs
downloader = LogDownloader()
downloader.download_logs("nginx_logs", "my_nginx.log")

# Analyze with custom settings
investigator = LogInvestigator("my_nginx.log")
investigator.run()
```

### **Batch Processing**
```bash
#!/bin/bash
# Download and analyze multiple sources
sources=("nginx_logs" "hadoop_logs" "windows_logs")

for source in "${sources[@]}"; do
    echo "Analyzing $source..."
    python main.py --convert "$source"
    echo "---"
done
```

## 🔧 **Troubleshooting**

### **Download Issues**
```bash
# Check internet connection
curl -I https://raw.githubusercontent.com/logpai/loghub/master/Nginx/Nginx_2k.log

# Try different source
python main.py --download apache_logs
```

### **Conversion Issues**
```bash
# Check file format
file downloaded_logs/nginx_logs.log

# Manual conversion
python download_logs.py --convert nginx_logs --output custom.json
```

### **Analysis Issues**
```bash
# Check file permissions
ls -la downloaded_logs/

# Verify JSON format
python -m json.tool nginx_logs_converted.json | head -10
```

## 📈 **Performance Tips**

### **For Large Log Files**
- Use `--convert` for JSON format (faster processing)
- Consider splitting large files
- Use specific time ranges when possible

### **For Multiple Sources**
- Download in batches
- Use `--download-all` for bulk operations
- Store in organized directory structure

## 🎉 **Benefits**

✅ **Real Data**: Analyze actual production logs
✅ **Diverse Sources**: Multiple systems and formats
✅ **Easy Setup**: One command to download and analyze
✅ **Learning**: Practice with real scenarios
✅ **No Cost**: All sources are free and open

## 🚀 **Next Steps**

1. **Explore Sources**: `python main.py --list-sources`
2. **Download One**: `python main.py --convert nginx_logs`
3. **Analyze Results**: Review the AI analysis
4. **Try Different Sources**: Experiment with various log types
5. **Compare Results**: Analyze multiple sources side by side

Your Log Investigator now has access to a vast collection of real-world log data! 🎉 