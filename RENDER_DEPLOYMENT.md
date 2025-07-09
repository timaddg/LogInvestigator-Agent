# Deploying Log Investigator on Render

This guide will help you deploy the Log Investigator application on Render.

## Prerequisites

1. A Render account (free tier available)
2. A Google Gemini API key
3. Your code pushed to a Git repository (GitHub, GitLab, etc.)

## Deployment Steps

### Option 1: Using render.yaml (Recommended)

1. **Push your code to Git**
   ```bash
   git add .
   git commit -m "Add Render deployment configuration"
   git push origin main
   ```

2. **Connect to Render**
   - Go to [render.com](https://render.com)
   - Sign up/Login with your Git provider
   - Click "New +" → "Blueprint"
   - Connect your repository
   - Render will automatically detect the `render.yaml` file

3. **Configure Environment Variables**
   - In the Render dashboard, go to your service
   - Navigate to "Environment" tab
   - Add your `GEMINI_API_KEY`:
     - Key: `GEMINI_API_KEY`
     - Value: Your actual API key
     - Mark as "Secret"

4. **Deploy**
   - Render will automatically build and deploy your application
   - The build process will:
     - Install Python dependencies
     - Build the Next.js frontend
     - Start the Flask backend

### Option 2: Manual Deployment

1. **Create a new Web Service**
   - Go to Render dashboard
   - Click "New +" → "Web Service"
   - Connect your Git repository

2. **Configure the Service**
   - **Name**: `log-investigator`
   - **Environment**: `Python 3`
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt && cd frontend && npm install && npm run build
     ```
   - **Start Command**: 
     ```bash
     chmod +x render-start.sh && ./render-start.sh
     ```

3. **Set Environment Variables**
   - `GEMINI_API_KEY`: Your Google Gemini API key
   - `NODE_ENV`: `production`
   - `PYTHONPATH`: `/opt/render/project/src/backend`
   - `FLASK_ENV`: `production`

4. **Deploy**
   - Click "Create Web Service"
   - Render will build and deploy your application

## Configuration

### Environment Variables

The following environment variables are automatically set by Render:

- `PORT`: Automatically set by Render (usually 10000)
- `NODE_ENV`: Set to `production`
- `PYTHONPATH`: Set to `/opt/render/project/src/backend`

You need to manually set:

- `GEMINI_API_KEY`: Your Google Gemini API key (required)

### Optional Environment Variables

You can also set these for customization:

- `GEMINI_MODEL`: AI model to use (default: `gemini-2.5-pro`)
- `GEMINI_MAX_TOKENS`: Maximum tokens (default: `2048`)
- `GEMINI_TEMPERATURE`: AI temperature (default: `0.3`)
- `SECRET_KEY`: Flask secret key (default: auto-generated)

## Architecture

On Render, the application runs as a single service that:

1. **Builds the frontend** during deployment
2. **Serves static files** from the Flask backend
3. **Handles API requests** through Flask routes
4. **Uses Render's built-in SSL** and load balancing

## Monitoring

### Health Checks
- Render automatically checks `/health` endpoint
- Service will restart if health checks fail

### Logs
- View logs in the Render dashboard
- Logs are automatically rotated

### Metrics
- Render provides basic metrics in the dashboard
- Monitor CPU, memory, and request counts

## Troubleshooting

### Common Issues

1. **Build Fails**
   - Check that all dependencies are in `requirements.txt`
   - Ensure Node.js dependencies are properly installed
   - Verify the build command syntax

2. **Runtime Errors**
   - Check the logs in Render dashboard
   - Verify environment variables are set correctly
   - Ensure the `GEMINI_API_KEY` is valid

3. **Frontend Not Loading**
   - Check that the frontend build completed successfully
   - Verify the static file serving routes in Flask
   - Check that `frontend/out` directory exists

4. **API Calls Failing**
   - Verify CORS settings
   - Check that the backend is running on the correct port
   - Ensure environment variables are accessible

### Debugging

1. **View Logs**
   ```bash
   # In Render dashboard
   Services → Your Service → Logs
   ```

2. **Check Environment**
   - Verify all environment variables are set
   - Check that secrets are properly configured

3. **Test Health Endpoint**
   - Visit `https://your-app.onrender.com/health`
   - Should return `{"status": "healthy"}`

