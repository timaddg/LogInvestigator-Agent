# Log Investigator

An AI-powered log analysis tool for cybersecurity and system administration. Upload your log files or download sample logs from online sources for instant AI-powered insights.

## Features

- 🤖 **AI-Powered Analysis**: Uses Google Gemini API for intelligent log analysis
- 📁 **File Upload**: Drag & drop interface for uploading log files
- 🌐 **Online Sources**: Download and analyze logs from various online repositories
- 📊 **Rich Statistics**: Detailed metrics and visualizations
- 🎨 **Modern UI**: Beautiful React/Next.js frontend with dark theme
- 🔧 **Modular Design**: Clean, maintainable codebase

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 18+
- Google Gemini API key

### 1. Backend Setup (Flask)

```bash
# Clone the repository
git clone <your-repo-url>
cd log-investigator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Start the Flask backend
python app.py
```

The Flask backend will run on `http://localhost:8000`

### 2. Frontend Setup (Next.js)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create environment file
echo "FLASK_BACKEND_URL=http://localhost:8000" > .env.local

# Start the development server
npm run dev
```

The frontend will run on `http://localhost:4000`

### 3. Usage

1. Open `http://localhost:4000` in your browser
2. **Upload Logs**: Drag & drop your log files (JSON, LOG, TXT, CSV)
3. **Download Samples**: Choose from available online log sources
4. **View Analysis**: Get AI-powered insights and statistics

## Architecture

```
log-investigator/
├── app.py                 # Flask backend server
├── config.py             # Configuration management
├── log_loader.py         # Log file loading and parsing
├── ai_analyzer.py        # AI analysis with Gemini
├── log_downloader.py     # Online log source management
├── utils.py              # Utility functions
├── requirements.txt      # Python dependencies
├── frontend/             # Next.js frontend
│   ├── src/
│   │   ├── app/         # Next.js App Router
│   │   │   └── types/       # TypeScript definitions
│   │   └── package.json     # Node.js dependencies
│   └── README.md            # This file
```

## Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Required: Google Gemini API Key
GEMINI_API_KEY=your_gemini_api_key_here

# Optional: Gemini Configuration
GEMINI_MODEL=gemini-2.5-pro
GEMINI_MAX_TOKENS=2048
GEMINI_TEMPERATURE=0.3

# Optional: Flask Configuration
SECRET_KEY=your-secret-key-here
```

### Frontend Configuration

Create a `.env.local` file in the `frontend/` directory:

```env
FLASK_BACKEND_URL=http://localhost:8000
```

## API Endpoints

### Flask Backend (`http://localhost:8000`)

- `POST /upload` - Upload and analyze log files
- `GET /sources` - Get available log sources
- `POST /download/<source>` - Download and analyze sample logs
- `GET /health` - Health check

### Next.js Frontend (`http://localhost:4000`)

- `/` - Main application interface
- `/api/upload` - Proxy to Flask upload endpoint
- `/api/sources` - Proxy to Flask sources endpoint
- `/api/download/[source]` - Proxy to Flask download endpoint

## Supported Log Formats

- **JSON**: Structured log data
- **LOG**: Standard log files
- **TXT**: Plain text logs
- **CSV**: Comma-separated values

## Available Log Sources

- **Web Server Logs**: Nginx, Apache access logs
- **Big Data Logs**: Hadoop, Elasticsearch, Kafka
- **Infrastructure Logs**: Docker, Kubernetes

## Development

### Backend Development

```bash
# Activate virtual environment
source venv/bin/activate

# Run with auto-reload
python app.py

# Run tests (if available)
python -m pytest
```

### Frontend Development

```bash
cd frontend

# Start development server
npm run dev

# Build for production
npm run build

# Run linting
npm run lint
```

## Deployment

### Backend Deployment

The Flask app can be deployed to:
- Heroku
- Railway
- DigitalOcean App Platform
- AWS Elastic Beanstalk
- Google Cloud Run

### Frontend Deployment

The Next.js app can be deployed to:
- Vercel (recommended)
- Netlify
- Railway
- DigitalOcean App Platform

## Troubleshooting

### Common Issues

1. **GEMINI_API_KEY not found**
   - Ensure your `.env` file exists and contains the API key
   - Verify the key is valid and has proper permissions

2. **Frontend can't connect to backend**
   - Check that Flask backend is running on port 8000
   - Verify `FLASK_BACKEND_URL` in frontend `.env.local`

3. **File upload fails**
   - Check file size (max 50MB)
   - Verify file format is supported
   - Ensure upload directory has write permissions

4. **CORS errors**
   - Backend has CORS enabled by default
   - Check that frontend URL is allowed

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:
- Check the troubleshooting section
- Review the configuration
- Open an issue on GitHub




