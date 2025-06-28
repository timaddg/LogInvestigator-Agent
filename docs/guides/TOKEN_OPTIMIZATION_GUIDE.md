# Token Optimization Guide for Log Investigator

This guide helps you optimize log files to stay within the free Google Gemini API token limits while maintaining analysis quality.

## 🎯 Token Limits Overview

### Free Gemini API Limits
- **Input Tokens**: ~30,000 tokens per request
- **Output Tokens**: ~2,000 tokens per response
- **Rate Limits**: 15 requests per minute

### What Consumes Tokens
- **Log Data**: Each log entry consumes tokens
- **Analysis Instructions**: ~200 tokens
- **JSON Formatting**: Adds overhead
- **Long Messages**: More tokens per entry

## 🚀 Optimization Strategies

### 1. Automatic Optimization (Recommended)

The Log Investigator automatically optimizes large log files:

```bash
# Enable optimization (default: true)
ENABLE_LOG_OPTIMIZATION=true

# Control sample size (default: 500)
SAMPLE_SIZE=300

# Set maximum log entries (default: 1000)
MAX_LOG_ENTRIES=800

# Set token limit (default: 30000)
MAX_INPUT_TOKENS=25000
```

### 2. Intelligent Sampling

The system prioritizes important logs:
- **Errors**: 50% of sample (most critical)
- **Warnings**: 30% of sample (important)
- **Info**: 20% of sample (context)

### 3. Log Compression

Each log entry is compressed to essential fields:
```json
{
  "timestamp": "2024-01-01 12:00:00",
  "level": "ERROR",
  "message": "Connection failed...",
  "ip": "192.168.1.1",
  "status": "500",
  "method": "POST",
  "path": "/api/endpoint"
}
```

## 📊 Token Usage Estimation

### Before Analysis
The system estimates token usage and provides recommendations:

```
📊 TOKEN USAGE ESTIMATE:
==================================================
Total Log Entries: 5,000
Estimated Tokens: 45,000
  ├─ Base Prompt: 200
  └─ Log Data: 44,800

💡 RECOMMENDATIONS:
  ⚠️ High token usage detected
  💡 Consider enabling log optimization
  💡 Reduce sample size or truncate messages

🚨 OPTIMIZATION RECOMMENDED:
  • Enable log optimization in .env file
  • Reduce SAMPLE_SIZE setting
  • Use smaller log files for analysis
==================================================
```

### Token Calculation
- **Base Prompt**: ~200 tokens
- **Log Data**: ~1.3 tokens per word
- **JSON Overhead**: ~20% additional tokens

## ⚙️ Configuration Options

### Environment Variables

Add these to your `.env` file:

```env
# Enable/disable optimization
ENABLE_LOG_OPTIMIZATION=true

# Maximum tokens for input
MAX_INPUT_TOKENS=30000

# Maximum log entries to process
MAX_LOG_ENTRIES=1000

# Sample size for large files
SAMPLE_SIZE=500

# Gemini API settings
GEMINI_MODEL=gemini-1.5-flash
GEMINI_MAX_TOKENS=2048
GEMINI_TEMPERATURE=0.3
```

### Optimization Levels

#### Conservative (Safe for Free Tier)
```env
SAMPLE_SIZE=300
MAX_INPUT_TOKENS=25000
MAX_LOG_ENTRIES=800
```

#### Balanced (Good Performance)
```env
SAMPLE_SIZE=500
MAX_INPUT_TOKENS=30000
MAX_LOG_ENTRIES=1000
```

#### Aggressive (Maximum Data)
```env
SAMPLE_SIZE=800
MAX_INPUT_TOKENS=35000
MAX_LOG_ENTRIES=1500
```

## 📁 Log File Preparation

### 1. Filter Before Upload
```bash
# Remove unnecessary fields
grep -v "DEBUG" large_log.log > filtered_log.log

# Keep only recent entries
tail -n 1000 large_log.log > recent_log.log

# Extract only errors and warnings
grep -E "(ERROR|WARN)" large_log.log > important_log.log
```

### 2. Split Large Files
```bash
# Split into smaller chunks
split -l 1000 large_log.log chunk_

# Analyze each chunk separately
for file in chunk_*; do
    python main.py --file "$file"
done
```

### 3. Compress Log Messages
```python
# Example: Truncate long messages
import json

def compress_log(log_entry):
    return {
        'timestamp': log_entry['timestamp'][:19],
        'level': log_entry['level'],
        'message': log_entry['message'][:200] + '...' if len(log_entry['message']) > 200 else log_entry['message']
    }
```

## 🔧 Manual Optimization Techniques

### 1. Pre-filter Logs
```bash
# Keep only last 24 hours
grep "$(date -d '1 day ago' +%Y-%m-%d)" access.log > recent_access.log

# Keep only specific services
grep "nginx" combined.log > nginx_only.log

# Remove verbose debug logs
grep -v "DEBUG" application.log > production.log
```

### 2. Extract Key Information
```bash
# Extract only error patterns
grep -o "ERROR.*" application.log > errors_only.log

# Extract HTTP status codes
grep -o "HTTP/[0-9.]*\" [0-9]*" access.log > status_codes.log

# Extract IP addresses and requests
grep -o "^[0-9.]*.*\"[A-Z]* [^ ]*" access.log > requests.log
```

### 3. Use Log Rotation
```bash
# Analyze only today's logs
python main.py --file /var/log/nginx/access.log.$(date +%Y%m%d)

# Analyze specific time ranges
sed -n '/2024-01-01 10:00:00/,/2024-01-01 11:00:00/p' large_log.log > hourly_sample.log
```

## 📈 Performance Monitoring

### Check Token Usage
```bash
# Run with verbose output
python main.py --file your_log.log

# Look for token estimates in output
# Estimated tokens: ~15,000
```

### Monitor API Quotas
- Check Google AI Studio dashboard
- Monitor rate limit errors
- Track daily usage

### Optimization Results
```
📊 Original logs: 10,000, Optimized: 500
🤖 Sending 500 log entries to Gemini...
📝 Estimated tokens: ~12,500
✅ AI analysis completed successfully
```

## 🚨 Troubleshooting

### Common Issues

#### "Rate limit exceeded"
- Wait 1 minute between requests
- Reduce log file size
- Use smaller sample sizes

#### "Token limit exceeded"
- Enable optimization
- Reduce SAMPLE_SIZE
- Split large files

#### "No response from API"
- Check API key validity
- Verify internet connection
- Check Gemini service status

### Error Recovery
```bash
# Retry with smaller sample
SAMPLE_SIZE=200 python main.py --file large_log.log

# Use conservative settings
MAX_INPUT_TOKENS=20000 SAMPLE_SIZE=300 python main.py --file large_log.log
```

## 💡 Best Practices

### 1. Start Small
- Begin with small log files
- Gradually increase size
- Monitor token usage

### 2. Focus on Quality
- Prioritize errors and warnings
- Remove noise and debug logs
- Keep relevant context

### 3. Use Sampling
- Sample representative data
- Include all error types
- Maintain time distribution

### 4. Monitor Usage
- Track token consumption
- Set up alerts for limits
- Optimize based on patterns

## 📚 Example Configurations

### Web Server Logs
```env
SAMPLE_SIZE=400
MAX_LOG_ENTRIES=800
ENABLE_LOG_OPTIMIZATION=true
```

### Application Logs
```env
SAMPLE_SIZE=300
MAX_LOG_ENTRIES=600
ENABLE_LOG_OPTIMIZATION=true
```

### Security Logs
```env
SAMPLE_SIZE=500
MAX_LOG_ENTRIES=1000
ENABLE_LOG_OPTIMIZATION=true
```

## 🎯 Summary

1. **Enable automatic optimization** (default: enabled)
2. **Adjust sample sizes** based on log type
3. **Pre-filter logs** before analysis
4. **Monitor token usage** with estimates
5. **Use conservative settings** for free tier
6. **Split large files** when necessary

Following these guidelines will help you stay within free Gemini API limits while getting meaningful log analysis results. 