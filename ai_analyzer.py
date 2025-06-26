"""
AI Analyzer module for Log Investigator.
Handles Google Gemini API interactions and log analysis.
"""

import json
import google.generativeai as genai
from typing import List, Dict, Any, Optional
from config import config


class AIAnalyzer:
    """Handles AI-powered log analysis using Google Gemini API."""
    
    def __init__(self):
        """Initialize AI analyzer with Gemini configuration."""
        genai.configure(api_key=config.gemini_api_key)
        self.model = genai.GenerativeModel(config.gemini_model)
        self.max_tokens = config.gemini_max_tokens
        self.temperature = config.gemini_temperature
    
    def analyze_logs(self, logs: List[Dict[str, Any]]) -> Optional[str]:
        """Analyze logs using AI and return analysis results."""
        try:
            prompt = self._create_analysis_prompt(logs)
            if not prompt:
                return None
            
            print("🤖 Sending logs to Gemini for analysis...")
            
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
    
    def _call_gemini_api(self, prompt: str) -> Optional[str]:
        """Make API call to Gemini."""
        try:
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
    
    def _create_analysis_prompt(self, logs: List[Dict[str, Any]]) -> Optional[str]:
        """Create a comprehensive prompt for AI analysis."""
        try:
            # Generate basic statistics
            total_logs = len(logs)
            error_count = sum(1 for log in logs if log.get('level') == 'ERROR')
            warning_count = sum(1 for log in logs if log.get('level') == 'WARN')
            
            # Get unique services
            services = list(set(log.get('service', 'UNKNOWN') for log in logs))
            
            prompt = f"""
You are a cybersecurity analyst. Analyze these logs and provide a CONCISE summary.

LOG SUMMARY:
- Total entries: {total_logs}
- Errors: {error_count}
- Warnings: {warning_count}
- Services: {', '.join(services)}

LOG DATA:
{json.dumps(logs, indent=2)}

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
    
    def analyze_specific_issue(self, logs: List[Dict[str, Any]], issue_type: str) -> Optional[str]:
        """Analyze logs for a specific type of issue."""
        try:
            prompt = f"""
You are a cybersecurity analyst. Focus on {issue_type} in these logs.

LOG DATA:
{json.dumps(logs, indent=2)}

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