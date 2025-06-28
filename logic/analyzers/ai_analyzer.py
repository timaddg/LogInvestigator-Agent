"""
AI Analyzer module for Log Investigator.
Handles Google Gemini API interactions and log analysis with token optimization.
"""

import json
import google.generativeai as genai
from typing import List, Dict, Any, Optional
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

from config.config import config
import random
from collections import Counter


class AIAnalyzer:
    """Handles AI-powered log analysis using Google Gemini API with token optimization."""
    
    def __init__(self):
        """Initialize AI analyzer with Gemini configuration."""
        genai.configure(api_key=config.gemini_api_key)
        self.model = genai.GenerativeModel(config.gemini_model)
        self.max_tokens = config.gemini_max_tokens
        self.temperature = config.gemini_temperature
        # Token limits for free tier optimization
        self.max_input_tokens = config.max_input_tokens
        self.max_log_entries = config.max_log_entries
        self.sample_size = config.sample_size
        self.enable_optimization = config.enable_log_optimization
    
    def analyze_logs(self, logs: List[Dict[str, Any]]) -> Optional[str]:
        """Analyze logs using AI with token optimization."""
        try:
            # Optimize logs for token efficiency if enabled
            if self.enable_optimization and len(logs) > self.max_log_entries:
                optimized_logs = self._optimize_logs_for_analysis(logs)
                total_original_logs = len(logs)
            else:
                optimized_logs = logs
                total_original_logs = len(logs)
            
            if not optimized_logs:
                return "❌ No valid logs to analyze after optimization."
            
            prompt = self._create_optimized_analysis_prompt(optimized_logs, total_original_logs)
            if not prompt:
                return None
            
            print(f"🤖 Sending {len(optimized_logs)} log entries to Gemini...")
            if self.enable_optimization and len(logs) > self.max_log_entries:
                print(f"📊 Original logs: {len(logs)}, Optimized: {len(optimized_logs)}")
            
            response = self._call_gemini_api(prompt)
            if not response:
                return None
            
            print("✅ AI analysis completed successfully")
            return response
        
        except Exception as e:
            print(f"❌ DEBUG: Full error details: {type(e).__name__}: {str(e)}")
            if "api_key" in str(e).lower() or "authentication" in str(e).lower():
                print("❌ Authentication error: Invalid API key")
                print("Please check your GEMINI_API_KEY in the .env file")
            elif "quota" in str(e).lower() or "rate" in str(e).lower():
                print("❌ Rate limit exceeded: Please wait before trying again")
            elif "model" in str(e).lower():
                print(f"❌ Model error: {e}")
                print(f"Please ensure the model '{config.gemini_model}' is available")
            else:
                print(f"❌ Unexpected error during AI analysis: {e}")
            return None
    
    def _optimize_logs_for_analysis(self, logs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Optimize logs to reduce token usage while preserving important information."""
        if not logs:
            return []
        
        total_logs = len(logs)
        print(f"📊 Optimizing {total_logs} log entries...")
        
        # Strategy 1: Prioritize errors and warnings
        error_logs = [log for log in logs if log.get('level') == 'ERROR']
        warning_logs = [log for log in logs if log.get('level') == 'WARN']
        info_logs = [log for log in logs if log.get('level') == 'INFO']
        
        # Strategy 2: Sample logs intelligently
        optimized_logs = []
        
        # Always include errors (up to 50% of sample)
        error_sample = min(len(error_logs), self.sample_size // 2)
        if error_logs:
            optimized_logs.extend(random.sample(error_logs, error_sample))
        
        # Include warnings (up to 30% of sample)
        warning_sample = min(len(warning_logs), self.sample_size // 3)
        if warning_logs:
            optimized_logs.extend(random.sample(warning_logs, warning_sample))
        
        # Fill remaining with info logs (up to 20% of sample)
        remaining_slots = self.sample_size - len(optimized_logs)
        if info_logs and remaining_slots > 0:
            info_sample = min(len(info_logs), remaining_slots)
            optimized_logs.extend(random.sample(info_logs, info_sample))
        
        # Strategy 3: Compress log entries
        compressed_logs = []
        for log in optimized_logs:
            compressed_log = self._compress_log_entry(log)
            if compressed_log:
                compressed_logs.append(compressed_log)
        
        print(f"✅ Optimization complete: {len(compressed_logs)} entries selected")
        return compressed_logs
    
    def _compress_log_entry(self, log: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Compress a log entry to reduce token usage."""
        try:
            # Keep only essential fields
            compressed = {
                'timestamp': log.get('timestamp', ''),
                'level': log.get('level', 'INFO'),
                'message': self._truncate_message(log.get('message', ''), 200)
            }
            
            # Add important fields if they exist
            if log.get('ip_address'):
                compressed['ip'] = log['ip_address']
            if log.get('status_code'):
                compressed['status'] = log['status_code']
            if log.get('request_method'):
                compressed['method'] = log['request_method']
            if log.get('request_path'):
                compressed['path'] = log['request_path'][:100]  # Truncate long paths
            
            return compressed
        except Exception as e:
            print(f"⚠️ Error compressing log entry: {e}")
            return None
    
    def _truncate_message(self, message: str, max_length: int) -> str:
        """Truncate message to reduce token usage."""
        if not message:
            return ""
        
        if len(message) <= max_length:
            return message
        
        # Try to truncate at a word boundary
        truncated = message[:max_length]
        last_space = truncated.rfind(' ')
        if last_space > max_length * 0.8:  # If we can find a good break point
            return truncated[:last_space] + "..."
        
        return truncated + "..."
    
    def _create_optimized_analysis_prompt(self, logs: List[Dict[str, Any]], total_original_logs: int) -> Optional[str]:
        """Create an optimized prompt for AI analysis."""
        try:
            # Generate key statistics
            total_logs = len(logs)
            error_count = sum(1 for log in logs if log.get('level') == 'ERROR')
            warning_count = sum(1 for log in logs if log.get('level') == 'WARN')
            
            # Get top IPs and status codes
            ip_counter = Counter(log.get('ip') for log in logs if log.get('ip'))
            status_counter = Counter(log.get('status') for log in logs if log.get('status'))
            
            # Create summary statistics
            stats_summary = f"""
LOG SUMMARY:
- Total entries analyzed: {total_logs} (from {total_original_logs} total)
- Errors: {error_count}
- Warnings: {warning_count}
- Top IPs: {dict(ip_counter.most_common(3))}
- Top Status Codes: {dict(status_counter.most_common(5))}
"""
            
            # Create a more compact log representation
            log_summary = self._create_log_summary(logs)
            
            prompt = f"""
You are a cybersecurity analyst. Analyze these logs and provide a CONCISE summary.

{stats_summary}

LOG SAMPLE:
{log_summary}

Provide a BRIEF analysis in this exact format:

## 🔍 QUICK OVERVIEW
[2-3 sentences summarizing the overall situation]

## 🚨 CRITICAL ISSUES
- [List only critical security/performance issues, max 3 items]

## ⚠️ WARNINGS
- [List important warnings, max 3 items]

## 📊 KEY METRICS
- [2-3 key performance metrics]

## 🎯 IMMEDIATE ACTIONS
- [2-3 specific, actionable steps]

Keep each section brief and actionable. Use bullet points. Focus on the most important findings only.
"""
            return prompt
        except Exception as e:
            print(f"❌ Error creating analysis prompt: {e}")
            return None
    
    def _create_log_summary(self, logs: List[Dict[str, Any]]) -> str:
        """Create a compact summary of logs instead of full JSON."""
        try:
            # Group logs by level
            by_level = {}
            for log in logs:
                level = log.get('level', 'INFO')
                if level not in by_level:
                    by_level[level] = []
                by_level[level].append(log)
            
            summary = []
            for level in ['ERROR', 'WARN', 'INFO']:
                if level in by_level:
                    level_logs = by_level[level]
                    summary.append(f"\n{level} LOGS ({len(level_logs)} entries):")
                    
                    # Show first 3 examples of each level
                    for i, log in enumerate(level_logs[:3]):
                        timestamp = log.get('timestamp', '')[:19]  # Truncate timestamp
                        message = log.get('message', '')[:100]    # Truncate message
                        summary.append(f"  {i+1}. [{timestamp}] {message}")
                    
                    if len(level_logs) > 3:
                        summary.append(f"  ... and {len(level_logs) - 3} more {level} entries")
            
            return '\n'.join(summary)
        except Exception as e:
            print(f"❌ Error creating log summary: {e}")
            return str(logs)[:1000] + "..."  # Fallback
    
    def _call_gemini_api(self, prompt: str) -> Optional[str]:
        """Make API call to Gemini with token monitoring."""
        try:
            # Estimate token count (rough approximation)
            estimated_tokens = len(prompt.split()) * 1.3  # Rough token estimation
            print(f"📝 Estimated tokens: ~{int(estimated_tokens)}")
            
            if estimated_tokens > self.max_input_tokens:
                print(f"⚠️ Warning: Estimated tokens ({int(estimated_tokens)}) exceed recommended limit ({self.max_input_tokens})")
            
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=self.max_tokens,
                    temperature=self.temperature
                )
            )
            
            if not response or not response.text:
                raise Exception("No response received from Gemini API")
            
            return response.text
            
        except Exception as e:
            raise Exception(f"API call failed: {e}")
    
    def analyze_specific_issue(self, logs: List[Dict[str, Any]], issue_type: str) -> Optional[str]:
        """Analyze logs for a specific type of issue with optimization."""
        try:
            # Optimize logs for specific analysis
            optimized_logs = self._optimize_logs_for_analysis(logs)
            
            if not optimized_logs:
                return f"❌ No logs available for {issue_type} analysis."
            
            prompt = f"""
You are a cybersecurity analyst. Focus on {issue_type} in these logs.

LOG SAMPLE:
{self._create_log_summary(optimized_logs)}

Provide a CONCISE analysis in this format:

## 🎯 {issue_type.upper()} ANALYSIS
[2-3 sentences about the issue]

## 🚨 SEVERITY
[Low/Medium/High] - [Brief reason]

## 🔍 ROOT CAUSE
[1-2 sentences identifying the cause]

## ✅ SOLUTION
[2-3 specific, actionable steps]

Keep it brief and actionable. Use bullet points where appropriate.
"""
            
            return self._call_gemini_api(prompt)
        
        except Exception as e:
            print(f"❌ Error in specific issue analysis: {e}")
            return None 