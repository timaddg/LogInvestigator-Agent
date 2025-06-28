# Gemini API Setup Guide

This guide will help you set up Google's Gemini API for your Log Investigator.

## 🎯 **Why Gemini API?**

- **Generous Free Tier**: 15 requests per minute, 1500 requests per day
- **High Quality**: Excellent for log analysis and security assessment
- **Fast**: Quick response times
- **Reliable**: Google's infrastructure
- **No Setup**: Just API key needed

## 📋 **Prerequisites**

- Google account
- Internet connection
- Python 3.7+

## 🚀 **Setup Steps**

### Step 1: Get Gemini API Key

1. **Go to Google AI Studio**: https://makersuite.google.com/app/apikey
2. **Sign in** with your Google account
3. **Click "Create API Key"**
4. **Copy the API key** (starts with `AIza...`)

### Step 2: Configure Your Environment

Create or update your `.env` file:

```env
# Gemini API Configuration
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-1.5-flash
GEMINI_MAX_TOKENS=2048
GEMINI_TEMPERATURE=0.3

# Log Configuration
LOG_FILE=log_investigator.log
LOG_LEVEL=INFO
SAMPLE_LOGS_FILE=sample_logs.json
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Test Your Setup

```bash
python main.py
```

## 🔧 **Configuration Options**

### Available Models

| Model | Speed | Quality | Best For |
|-------|-------|---------|----------|
| `gemini-1.5-flash` | Fast | Good | General use |
| `gemini-1.5-pro` | Medium | Excellent | Complex analysis |
| `gemini-1.0-pro` | Medium | Good | Balanced |

### Configuration Parameters

```env
# Model selection
GEMINI_MODEL=gemini-1.5-flash

# Response length (tokens)
GEMINI_MAX_TOKENS=2048

# Creativity (0.0 = focused, 1.0 = creative)
GEMINI_TEMPERATURE=0.3
```

## 💰 **Pricing & Limits**

### Free Tier Limits
- **Requests per minute**: 15
- **Requests per day**: 1500
- **Characters per request**: 30,000
- **Characters per response**: 30,000

### Paid Tier (if needed)
- **$0.00025** per 1K characters input
- **$0.0005** per 1K characters output
- Higher rate limits

## 🎯 **Usage Examples**

### Basic Log Analysis
```bash
python main.py
```

### Custom Configuration
```env
# For more detailed analysis
GEMINI_MODEL=gemini-1.5-pro
GEMINI_MAX_TOKENS=4096
GEMINI_TEMPERATURE=0.1
```

## 🔍 **Troubleshooting**

### Common Issues

1. **"Invalid API key"**
   - Check your API key format (should start with `AIza`)
   - Ensure no extra spaces in `.env` file

2. **"Rate limit exceeded"**
   - Wait a minute before trying again
   - Check your usage in Google AI Studio

3. **"Model not found"**
   - Use one of the supported models
   - Check model name spelling

### Error Messages

| Error | Solution |
|-------|----------|
| `GEMINI_API_KEY is required` | Add API key to `.env` file |
| `Invalid API key` | Check key format and validity |
| `Rate limit exceeded` | Wait and retry |
| `Model not found` | Use supported model name |

## 📊 **Performance Tips**

### For Better Results
- Use `gemini-1.5-flash` for speed
- Use `gemini-1.5-pro` for quality
- Set `temperature=0.1` for focused analysis
- Set `temperature=0.7` for creative insights

### For Cost Optimization
- Use shorter prompts
- Set lower `max_tokens`
- Use `gemini-1.5-flash` (cheaper)

## 🔐 **Security Best Practices**

1. **Never commit API keys** to version control
2. **Use environment variables** for configuration
3. **Rotate API keys** regularly
4. **Monitor usage** in Google AI Studio

## 📈 **Monitoring Usage**

### Check Usage in Google AI Studio
1. Go to https://makersuite.google.com/app/apikey
2. Click on your API key
3. View usage statistics

### Usage Alerts
- Set up alerts for approaching limits
- Monitor daily usage
- Track cost (if on paid tier)

## 🎉 **Benefits of Gemini API**

✅ **No Server Setup**: Just API key needed
✅ **High Quality**: Excellent for log analysis
✅ **Fast**: Quick response times
✅ **Reliable**: Google's infrastructure
✅ **Free Tier**: Generous limits
✅ **Scalable**: Easy to upgrade

## 🚀 **Next Steps**

1. **Get your API key** from Google AI Studio
2. **Configure your `.env` file**
3. **Install dependencies**
4. **Run your Log Investigator**

Your Log Investigator is now ready to use Gemini API! 🎉 