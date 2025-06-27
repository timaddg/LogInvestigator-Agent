# Log Investigator

A Python-based log analysis and investigation tool designed to help developers and system administrators analyze, filter, and investigate log files efficiently using AI-powered analysis.

## Features

- 📊 **Real Log Analysis**: Download and analyze real-world JSON logs from Elastic examples
- 🔍 **AI-Powered Analysis**: Use Google Gemini AI for intelligent log analysis
- 📈 **Smart Field Mapping**: Automatically normalize and validate log fields
- 🚨 **Error Detection**: Identify and categorize errors and warnings
- 🔐 **Security Monitoring**: Detect suspicious activities and security threats
- 📝 **JSON Lines Support**: Handle both JSON arrays and JSON Lines format
- 🌐 **Internet Sources**: Access to real-world log sources from Elastic examples

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
   cp .env.example .env
   # Edit .env file with your Gemini API key
   ```

## Usage

### Basic Usage

Run the application to automatically download and analyze sample JSON logs:
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
# Analyze sample JSON logs
python main.py --source sample_json_logs

# Download and convert to JSON format
python main.py --convert sample_json_logs
```

**Analyze a specific file:**
```bash
python main.py --file sample_json_logs.log
```

## Environment Variables

Create a `.env` file with the following variables:

```env
# Gemini API Configuration
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-flash
GEMINI_MAX_TOKENS=2048
GEMINI_TEMPERATURE=0.3

# Log Configuration
LOG_FILE=log_investigator.log
LOG_LEVEL=INFO
SAMPLE_LOGS_FILE=sample_json_logs.log
```

## Available Log Sources

### Current Sources
- `sample_json_logs` - Real Nginx JSON logs from Elastic examples repository

The system downloads real-world logs from the Elastic examples repository, which contains anonymized web server logs in JSON format.

## Project Structure

```
log-investigator/
├── main.py              # Main application entry point
├── config.py            # Configuration management
├── log_loader.py        # Log file loading and validation (supports JSON Lines)
├── log_downloader.py    # Download logs from internet sources
├── ai_analyzer.py       # AI-powered log analysis using Gemini
├── utils.py             # Utilities and display formatting
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
3. **Activate Virtual Environment**: `source venv/bin/activate`
4. **Run Analysis**: `python main.py`
5. **Explore Sources**: `python main.py --list-sources`

## AI Analysis Features

The AI analysis provides:
- 🔍 **Quick Overview**: Summary of log analysis
- 🚨 **Critical Issues**: Security and performance problems
- ⚠️ **Warnings**: Important alerts and notifications
- 📊 **Key Metrics**: Performance and usage statistics
- 🎯 **Immediate Actions**: Specific recommendations

## Log Format Support

The system supports multiple log formats:
- **JSON Arrays**: Traditional JSON array format
- **JSON Lines**: One JSON object per line (JSONL format)
- **Field Normalization**: Automatically maps common field names
- **Smart Validation**: Adds missing required fields with intelligent defaults

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError: No module named 'google'**
   ```bash
   pip install google-generativeai
   ```

2. **GEMINI_API_KEY is required**
   - Ensure you have a valid Gemini API key in your `.env` file
   - Get your API key from https://makersuite.google.com/app/apikey

3. **Virtual environment not activated**
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

**Note**: This tool downloads real-world logs from the Elastic examples repository for educational and analysis purposes. All logs are anonymized and free to use.




