# Log Investigator Frontend

A modern React/Next.js frontend for the Log Investigator AI-powered log analysis tool.

## Features

- 🎨 Modern, responsive UI with dark theme
- 📁 Drag & drop file upload
- 🌐 Download sample logs from online sources
- 🤖 AI-powered log analysis with Google Gemini
- 📊 Interactive statistics and insights
- ⚡ Real-time analysis results

## Tech Stack

- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **File Upload**: React Dropzone
- **Backend**: Flask API (separate service)

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn
- Python backend running (see main README)

### Installation

1. Install dependencies:
```bash
npm install
```

2. Set up environment variables:
```bash
cp .env.example .env.local
```

Edit `.env.local`:
```env
FLASK_BACKEND_URL=http://localhost:8000
```

3. Start the development server:
```bash
npm run dev
```

4. Open [http://localhost:4000](http://localhost:4000) in your browser.

## Usage

### File Upload
1. Drag and drop a log file onto the upload area
2. Supported formats: JSON, LOG, TXT, CSV
3. Maximum file size: 50MB
4. The AI will automatically analyze your logs

### Sample Logs
1. Browse available log sources in the right panel
2. Click "Download & Analyze" on any source
3. The system will download and analyze the logs automatically

### Analysis Results
- **AI Analysis**: View AI-generated insights about your logs
- **Statistics**: See detailed metrics and patterns
- **HTTP Status Codes**: Color-coded status code distribution
- **Top Endpoints**: Most accessed endpoints
- **Time Range**: Log entry time span

## Development

### Project Structure
```
src/
├── app/                 # Next.js App Router
│   ├── api/            # API routes (proxies to Flask)
│   └── page.tsx        # Main page
├── components/         # React components
│   ├── FileUpload.tsx  # File upload with drag & drop
│   ├── LogSources.tsx  # Sample log sources
│   └── AnalysisResults.tsx # Results display
└── types/              # TypeScript type definitions
```

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

## API Integration

The frontend communicates with the Flask backend through API routes:

- `POST /api/upload` - Upload and analyze log files
- `GET /api/sources` - Get available log sources
- `POST /api/download/[source]` - Download and analyze sample logs

## Deployment

### Vercel (Recommended)
1. Push your code to GitHub
2. Connect your repository to Vercel
3. Set environment variables in Vercel dashboard
4. Deploy

### Other Platforms
The app can be deployed to any platform that supports Next.js:
- Netlify
- Railway
- DigitalOcean App Platform
- AWS Amplify

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_BACKEND_URL` | URL of the Flask backend | `http://localhost:8000` |

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see main repository for details.
