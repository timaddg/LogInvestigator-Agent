# Online Logs Guide

This guide explains how to download and analyze logs from various online sources using Log Investigator.

## Available Log Sources

Log Investigator supports downloading logs from several online repositories:

### Web Server Logs
- **nginx_logs**: Nginx access logs from various web servers
- **apache_logs**: Apache access logs with different formats
- **iis_logs**: Internet Information Services logs

### Big Data Logs
- **hadoop_logs**: Hadoop distributed file system logs
- **spark_logs**: Apache Spark application logs
- **kafka_logs**: Apache Kafka streaming logs

### Infrastructure Logs
- **docker_logs**: Docker container logs
- **kubernetes_logs**: Kubernetes cluster logs
- **elasticsearch_logs**: Elasticsearch search engine logs

## Downloading Logs

### Using the CLI

```bash
# Download a specific log source
python run.py cli --download nginx_logs

# Download and analyze in one command
python run.py cli --convert nginx_logs

# Download multiple sources
python run.py cli --download nginx_logs,hadoop_logs,spark_logs
```

### Using the Web Interface

1. Open the web interface at `http://localhost:4000`
2. Click on "Download Sample Logs"
3. Select the log source you want to download
4. Click "Download and Analyze"

### Using the Download Script

```bash
# Download a specific source
python scripts/download_logs.py --download nginx_logs

# Download with custom output file
python scripts/download_logs.py --download nginx_logs --output my_nginx.json

# Download multiple sources
python scripts/download_logs.py --download nginx_logs,hadoop_logs,spark_logs
```

## Analyzing Downloaded Logs

### CLI Analysis

```bash
# Analyze a downloaded file
python run.py cli --file downloaded_logs/nginx_logs.json

# Analyze with specific options
python run.py cli --file downloaded_logs/nginx_logs.json --optimize
```

### Web Interface Analysis

1. Upload the downloaded JSON file through the web interface
2. The system will automatically analyze the logs
3. View the results in the analysis panel

## Project Structure

After downloading logs, your project structure will look like:

```
log-investigator/
├── downloaded_logs/
│   ├── nginx_logs.json
│   ├── hadoop_logs.json
│   └── spark_logs.json
├── data/
│   └── logs/
└── ...
```

## Log Formats

The downloaded logs come in various formats:

- **JSON**: Structured log data (preferred)
- **Raw logs**: `{source_name}.json`

## Advanced Usage

### Programmatic Download

```python
from logic.processors.log_downloader import LogDownloader

# Initialize downloader
downloader = LogDownloader()

# Download logs
downloader.download_logs("nginx_logs", "my_nginx.json")

# Download and analyze
from backend.main import LogInvestigator
investigator = LogInvestigator("my_nginx.json")
investigator.analyze()
```

### Batch Download

```python
# Download multiple sources
sources = ["nginx_logs", "hadoop_logs", "spark_logs"]
downloader.download_multiple_sources(sources)
```

## Troubleshooting

### Download Issues

If downloads fail, check:

1. **Internet Connection**: Ensure you have a stable internet connection
2. **Source Availability**: Some sources may be temporarily unavailable
3. **File Permissions**: Ensure you have write permissions in the output directory

### File Size Issues

Large log files may cause memory issues. Use optimization:

```bash
# Enable optimization for large files
ENABLE_LOG_OPTIMIZATION=true python run.py cli --file large_log.json
```

### Source Verification

You can verify source URLs before downloading:

```bash
# Check if a source is available
curl -I https://raw.githubusercontent.com/logpai/loghub/master/Nginx/Nginx_2k.log
```

## Examples

### Basic Analysis

```bash
# Download and analyze nginx logs
python run.py cli --convert nginx_logs
```

### Custom Analysis

```bash
# Download logs to custom location
python scripts/download_logs.py --download nginx_logs --output /tmp/nginx.json

# Analyze with custom settings
MAX_INPUT_TOKENS=20000 python run.py cli --file /tmp/nginx.json
```

### Batch Processing

```bash
# Download multiple sources
python scripts/download_logs.py --download nginx_logs,hadoop_logs,spark_logs

# List downloaded files
ls -la downloaded_logs/
```

## Contributing

To add new log sources:

1. Add the source to the `sources` dictionary in `log_downloader.py`
2. Test the download functionality
3. Update this documentation
4. Submit a pull request

## Support

For issues with specific log sources or download problems:

1. Check the troubleshooting section
2. Verify the source URL is still accessible
3. Open an issue on GitHub with details about the problem 