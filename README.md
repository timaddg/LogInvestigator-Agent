# Log Investigator 🔍

An AI-powered log analysis tool for cybersecurity and system administration that provides intelligent insights from log files using Google's Gemini AI.

## 🚀 Features

- **AI-Powered Analysis**: Uses Google Gemini AI to analyze logs and provide intelligent insights
- **Multiple Input Sources**: 
  - Upload local log files (JSON, LOG, TXT, CSV formats)
  - Download sample logs from online sources
  - Auto-download and analyze sample logs
- **Dual Interface**: 
  - Modern web interface (Next.js + TypeScript)
  - Command-line interface for automation
- **Smart Log Processing**: 
  - Automatic log validation and statistics
  - Token usage optimization for large files
  - Support for various log formats
- **Real-time Analysis**: Instant AI-powered insights with detailed breakdowns

## 🏗️ Architecture

```
log-investigator/
├── backend/                 # Python backend
│   ├── api/                # Flask API endpoints
│   ├── config/             # Configuration management
│   ├── logic/              # Core business logic
│   │   ├── analyzers/      # AI analysis engine
│   │   └── processors/     # Log processing & downloading
│   └── utils/              # Utility functions
├── frontend/               # Next.js web interface
│   ├── src/
│   │   ├── app/           # Next.js app router
│   │   ├── components/    # React components
│   │   └── types/         # TypeScript definitions
│   └── public/            # Static assets
├── data/                   # Sample data and logs
├── docs/                   # Documentation
└── scripts/               # Utility scripts
```

## 🛠️ Technology Stack

### Backend
- **Python 3.8+** - Core language
- **Flask** - Web API framework
- **Google Gemini AI** - AI analysis engine
- **Pandas** - Data processing
- **Rich** - Terminal output formatting

### Frontend
- **Next.js 14** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **React Hooks** - State management

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Node.js 18 or higher
- Google Gemini API key

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/log-investigator.git
   cd log-investigator
   ```

2. **Set up Python environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r backend/requirements.txt
   ```

3. **Set up frontend**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

4. **Configure environment variables**
   ```bash
   cp env.example .env
   # Edit .env and add your GEMINI_API_KEY
   ```

## 🔧 Configuration

Create a `.env` file with the following variables:

```env
# Required
GEMINI_API_KEY=your_gemini_api_key_here

# Optional (with defaults)
GEMINI_MODEL=gemini-2.5-pro
GEMINI_MAX_TOKENS=2048
GEMINI_TEMPERATURE=0.3
ENABLE_LOG_OPTIMIZATION=true
MAX_INPUT_TOKENS=30000
MAX_LOG_ENTRIES=1000
SAMPLE_SIZE=500
```

## 🚀 Usage

### Web Interface (Recommended)

1. **Start the backend server**
   ```bash
   python run.py web
   ```

2. **Start the frontend**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Open your browser**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

### Command Line Interface

```bash
# Run with default sample logs
python run.py cli

# Analyze specific file
python run.py cli --file path/to/logs.json

# List available online log sources
python run.py cli --list-sources

# Download and analyze from specific source
python run.py cli --download sample_json_logs

# Download, convert, and analyze
python run.py cli --convert sample_json_logs
```

### Direct Backend Usage

```bash
# Navigate to backend directory
cd backend

# Run with default behavior (downloads and analyzes sample logs)
python main.py

# Analyze specific file
python main.py --file ../data/logs/sample_logs.json

# List available sources
python main.py --list-sources

# Download from specific source
python main.py --download sample_json_logs
```

## 📊 Supported Log Sources

The tool currently works with **JSON-formatted logs** and can:

- **Upload Local JSON Files**: Analyze your own JSON log files
- **Download Sample JSON Logs**: Access pre-formatted JSON logs from online sources
- **Convert Other Formats**: Download various log formats (Nginx, Apache, Hadoop, etc.) and convert them to JSON for analysis

### Available Sample Sources:
- **Web Server Logs**: Nginx, Apache access logs (converted to JSON)
- **Big Data Logs**: Hadoop, Elasticsearch, Kafka logs (converted to JSON)
- **Infrastructure Logs**: Docker, Kubernetes logs (converted to JSON)

All logs are processed and analyzed in JSON format for consistency and optimal AI analysis.

## 🔍 AI Analysis Features

The AI analyzer provides:

- **Log Type Detection**: Automatically identifies log formats and sources
- **Anomaly Detection**: Finds unusual patterns and potential issues
- **Security Insights**: Identifies security-related events and threats
- **Performance Analysis**: Highlights performance bottlenecks
- **Summary Reports**: Concise summaries with actionable insights
- **Token Optimization**: Smart handling of large log files

## 📁 Project Structure

```
├── backend/                 # Python backend application
│   ├── api/                # Flask API endpoints
│   ├── config/             # Configuration management
│   ├── logic/              # Core business logic
│   │   ├── analyzers/      # AI analysis components
│   │   └── processors/     # Log processing & downloading
│   ├── utils/              # Utility functions
│   └── main.py             # CLI entry point
├── frontend/               # Next.js web application
│   ├── src/
│   │   ├── app/           # Next.js app router pages
│   │   ├── components/    # React components
│   │   └── types/         # TypeScript type definitions
│   └── package.json       # Frontend dependencies
├── data/                   # Sample data and logs
│   └── logs/              # Sample log files
├── docs/                   # Documentation
│   ├── api/               # API documentation
│   ├── deployment/        # Deployment guides
│   └── guides/            # User guides
├── scripts/               # Utility scripts
├── run.py                 # Main entry point
└── README.md              # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check the `docs/` directory for detailed guides
- **Issues**: Report bugs and feature requests on GitHub
- **Discussions**: Use GitHub Discussions for questions and ideas

## 🔗 Related Links

- [Google Gemini API Documentation](https://ai.google.dev/docs)
- [Next.js Documentation](https://nextjs.org/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

**Log Investigator** - Making log analysis intelligent and accessible! 🔍✨ 