#!/usr/bin/env python3
"""
Log Investigator - Main Entry Point

A modular, AI-powered log analysis tool for cybersecurity and system administration.
"""

import sys
import argparse
from typing import Optional

# Import our modules
import os
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from config.config import config
from logic.processors.log_loader import LogLoader
from logic.analyzers.ai_analyzer import AIAnalyzer
from logic.processors.log_downloader import LogDownloader
from utils.utils import (
    print_header, print_success, print_error, print_info,
    display_log_statistics, display_analysis_results,
    estimate_token_usage, display_token_estimate,
    exit_with_error, exit_success
)


class LogInvestigator:
    """Main application class for log investigation."""
    
    def __init__(self, log_file: str = None):
        """Initialize the log investigator with all components."""
        self.log_loader = LogLoader(log_file or config.sample_logs_file)
        self.ai_analyzer = AIAnalyzer()
        self.downloader = LogDownloader()
    
    def run(self) -> None:
        """Main execution flow."""
        try:
            print_header("Log Investigator - AI-Powered Log Analysis")
            
            # Step 1: Load and validate logs
            logs = self._load_logs()
            if not logs:
                exit_with_error("Failed to load logs")
            
            # Step 2: Generate and display statistics
            self._display_statistics(logs)
            
            # Step 3: Estimate token usage
            self._estimate_token_usage(logs)
            
            # Step 4: Perform AI analysis
            analysis_result = self._analyze_logs(logs)
            if not analysis_result:
                exit_with_error("Failed to complete AI analysis")
            
            # Step 5: Display results
            self._display_results(analysis_result)
            
            # Success
            exit_success()
            
        except KeyboardInterrupt:
            print_error("Analysis interrupted by user")
            sys.exit(0)
        except Exception as e:
            exit_with_error(f"Unexpected error: {e}")
    
    def _load_logs(self) -> Optional[list]:
        """Load logs with error handling."""
        print_info("Loading log data...")
        logs = self.log_loader.load_logs()
        
        if not logs:
            return None
        
        print_success(f"Successfully loaded {len(logs)} log entries")
        return logs
    
    def _display_statistics(self, logs: list) -> None:
        """Display log statistics."""
        print_info("Generating log statistics...")
        stats = self.log_loader.get_log_statistics(logs)
        display_log_statistics(stats)
    
    def _estimate_token_usage(self, logs: list) -> None:
        """Estimate and display token usage for AI analysis."""
        print_info("Estimating token usage for AI analysis...")
        estimate = estimate_token_usage(logs, include_full_json=False)
        display_token_estimate(estimate)
        
        # Ask user if they want to continue if optimization is needed
        if estimate.get('optimization_needed', False):
            print_info("Large log file detected. Optimization will be applied automatically.")
    
    def _analyze_logs(self, logs: list) -> Optional[str]:
        """Perform AI analysis on logs."""
        print_info("Starting AI-powered analysis...")
        return self.ai_analyzer.analyze_logs(logs)
    
    def _display_results(self, analysis_result: str) -> None:
        """Display analysis results."""
        print_info("Displaying analysis results...")
        display_analysis_results(analysis_result)
    
    def list_sources(self) -> None:
        """List available log sources."""
        self.downloader.list_sources()
    
    def download_logs(self, source_name: str, output_file: str = None) -> Optional[str]:
        """Download logs from a specific source."""
        return self.downloader.download_logs(source_name, output_file)
    
    def download_and_convert(self, source_name: str, output_file: str = None) -> Optional[str]:
        """Download and convert logs to JSON format."""
        return self.downloader.download_and_convert_to_json(source_name, output_file)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Log Investigator - AI-Powered Log Analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                                    # Download and analyze sample JSON logs
  python main.py --file sample_json_logs.log       # Analyze specific file
  python main.py --list-sources                     # List available log sources
  python main.py --download sample_json_logs        # Download and analyze sample JSON logs
  python main.py --convert sample_json_logs         # Download, convert, and analyze
        """
    )
    
    parser.add_argument(
        '--file', '-f',
        type=str,
        help='Log file to analyze (JSON, LOG, TXT, CSV formats supported)'
    )
    
    parser.add_argument(
        '--list-sources', '-l',
        action='store_true',
        help='List available log sources'
    )
    
    parser.add_argument(
        '--download', '-d',
        type=str,
        help='Download and analyze logs from specific source'
    )
    
    parser.add_argument(
        '--convert', '-c',
        type=str,
        help='Download, convert to JSON, and analyze logs'
    )
    
    parser.add_argument(
        '--source', '-s',
        type=str,
        default='sample_json_logs',
        help='Default source to download and analyze'
    )
    
    parser.add_argument(
        '--optimize', '-o',
        action='store_true',
        help='Enable log optimization for large files'
    )
    
    args = parser.parse_args()
    
    # Set optimization flag
    if args.optimize:
        os.environ['ENABLE_LOG_OPTIMIZATION'] = 'true'
    
    # Initialize LogInvestigator
    log_investigator = LogInvestigator(args.file)
    
    # Handle different modes
    if args.list_sources:
        print_header("Available Log Sources")
        log_investigator.list_sources()
    elif args.download:
        print_header(f"Downloading and Analyzing {args.download}")
        log_investigator.download_logs(args.download)
    elif args.convert:
        print_header(f"Downloading, Converting, and Analyzing {args.convert}")
        log_investigator.download_and_convert(args.convert)
    elif args.file:
        # Analyze the specified file
        log_investigator.run()
    else:
        # Default: download and analyze sample JSON logs
        print_header(f"Auto-downloading and Analyzing {args.source}")
        log_investigator.download_logs(args.source)


if __name__ == "__main__":
    main()
