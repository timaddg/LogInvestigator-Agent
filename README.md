# Log Investigator

A Python-based log analysis and investigation tool designed to help developers and system administrators analyze, filter, and investigate log files efficiently.

## Features

- 📊 **Log Analysis**: Parse and analyze structured JSON log files
- 🔍 **Advanced Filtering**: Filter logs by level, service, user, IP address, and more
- 📈 **Performance Metrics**: Track request durations and performance patterns
- 🚨 **Error Detection**: Identify and categorize errors and warnings
- 🔐 **Security Monitoring**: Detect suspicious activities like failed login attempts
- 📝 **Comprehensive Logging**: Built-in logging with configurable levels

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/timaddg/LogInvestigator-Agent.git
   cd LogInvestigator-Agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env file with your configuration
   ```

## Usage

### Basic Usage

Run the main application:
```bash
python main.py
```

### Environment Variables

Create a `.env` file with the following variables:

```env
# Log file path
LOG_FILE=log_investigator.log

# Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL=INFO

# Path to sample logs
SAMPLE_LOGS_FILE=sample_logs.json

# OpenAI API Key (optional, for AI-powered analysis)
OPENAI_API_KEY=your_openai_api_key_here
```

## Sample Data

The project includes `sample_logs.json` with realistic log data including:
- Web server logs
- Database connection issues
- User authentication events
- Security warnings
- Performance metrics
- Error tracking

## Project Structure

```
log-investigator/
├── main.py              # Main application entry point
├── sample_logs.json     # Sample log data for testing
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (not tracked by git)
├── env.example          # Environment variables template
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Dependencies

- **python-dotenv**: Environment variable management
- **pandas**: Data analysis and manipulation
- **rich**: Enhanced terminal output




