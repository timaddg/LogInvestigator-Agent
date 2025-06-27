# Log Investigator

A Python-based log analysis and investigation tool designed to help developers and system administrators analyze, filter, and investigate log files efficiently.

## Features

- 📊 **Real Log Analysis**: Download and analyze real-world logs from various sources
- 🔍 **AI-Powered Analysis**: Use Google Gemini AI for intelligent log analysis
- 📈 **Performance Metrics**: Track request durations and performance patterns
- 🚨 **Error Detection**: Identify and categorize errors and warnings
- 🔐 **Security Monitoring**: Detect suspicious activities and security threats
- 📝 **Comprehensive Logging**: Built-in logging with configurable levels
- 🌐 **Internet Sources**: Access to 8+ real-world log sources

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/timaddg/LogInvestigator-Agent.git
   cd LogInvestigator-Agent
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env file with your Gemini API key
   ```

## Usage

### Basic Usage

Run the application to automatically download and analyze web server logs:
```bash
python main.py
```

### Advanced Usage

**List available log sources:**
```bash
python main.py --list-sources
```

**Download and analyze specific logs:**
```bash
# Analyze Hadoop logs
python main.py --source hadoop_logs

# Analyze Spark logs
python main.py --source spark_logs

# Analyze Elasticsearch logs
python main.py --source elasticsearch_logs
```

**Download and convert to JSON:**
```bash
python main.py --convert web_server_logs
```

**Analyze a specific file:**
```bash
python main.py --file downloaded_logs/hadoop_logs.log
```

## Environment Variables

Create a `.env` file with the following variables:

```env
# Log file path
LOG_FILE=log_investigator.log

# Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL=INFO
SAMPLE_LOGS_FILE=downloaded_logs/web_server_logs.log
```

## Available Log Sources

### Web Servers
- `web_server_logs` - Nginx web server logs
- `github_logs` - Apache web server logs
- `sample_json_logs` - JSON format nginx logs

### Big Data & Cloud
- `hadoop_logs` - Hadoop distributed computing
- `spark_logs` - Apache Spark processing

### Infrastructure
- `zookeeper_logs` - Apache ZooKeeper
- `hpc_logs` - High Performance Computing
- `elasticsearch_logs` - Elasticsearch search engine

## Project Structure

```
log-investigator/
├── main.py              # Main application entry point
├── config.py            # Configuration management
├── log_loader.py        # Log file loading and validation
├── log_downloader.py    # Download logs from internet sources
├── ai_analyzer.py       # AI-powered log analysis
├── utils.py             # Utilities and display formatting
├── download_logs.py     # CLI for downloading logs
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (not tracked by git)
├── .env.example         # Environment variables template
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Dependencies

- **python-dotenv**: Environment variable management
- **pandas**: Data analysis and manipulation
- **rich**: Enhanced terminal output
- **google-generativeai**: Google Gemini AI integration
- **requests**: HTTP requests for downloading logs

## Getting Started

1. **Get Gemini API Key**: Visit https://makersuite.google.com/app/apikey
2. **Configure Environment**: Add your API key to `.env` file
3. **Run Analysis**: `python main.py`
4. **Explore Sources**: `python main.py --list-sources`

## AI Analysis Features

The AI analysis provides:
- 🔍 **Quick Overview**: Summary of log analysis
- 🚨 **Critical Issues**: Security and performance problems
- ⚠️ **Warnings**: Important alerts and notifications
- 📊 **Key Metrics**: Performance and usage statistics
- 🎯 **Immediate Actions**: Specific recommendations

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

**Note**: This tool downloads real-world logs from open source repositories for educational and analysis purposes. All logs are anonymized and free to use.




