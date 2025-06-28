#!/usr/bin/env python3
"""
Log Investigator - Main Entry Point

A modular, AI-powered log analysis tool for cybersecurity and system administration.
"""

import sys
import os
import argparse

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def main():
    """Main entry point with options to run CLI or web server."""
    parser = argparse.ArgumentParser(
        description="Log Investigator - AI-Powered Log Analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run.py cli                                    # Run CLI interface
  python run.py web                                    # Run web server
  python run.py cli --file sample.json                 # Analyze specific file
  python run.py cli --list-sources                     # List available sources
        """
    )
    
    parser.add_argument(
        'mode',
        choices=['cli', 'web'],
        help='Run mode: cli (command line) or web (Flask server)'
    )
    
    parser.add_argument(
        '--file', '-f',
        type=str,
        help='Log file to analyze (CLI mode only)'
    )
    
    parser.add_argument(
        '--list-sources', '-l',
        action='store_true',
        help='List available log sources (CLI mode only)'
    )
    
    parser.add_argument(
        '--download', '-d',
        type=str,
        help='Download and analyze logs from specific source (CLI mode only)'
    )
    
    parser.add_argument(
        '--convert', '-c',
        type=str,
        help='Download, convert to JSON, and analyze logs (CLI mode only)'
    )
    
    parser.add_argument(
        '--source', '-s',
        type=str,
        default='sample_json_logs',
        help='Default source to download and analyze (CLI mode only)'
    )
    
    args = parser.parse_args()
    
    if args.mode == 'cli':
        # Import and run CLI
        from main import main as cli_main
        # Set up sys.argv for CLI compatibility
        sys.argv = ['main.py']
        if args.file:
            sys.argv.extend(['--file', args.file])
        if args.list_sources:
            sys.argv.append('--list-sources')
        if args.download:
            sys.argv.extend(['--download', args.download])
        if args.convert:
            sys.argv.extend(['--convert', args.convert])
        if args.source:
            sys.argv.extend(['--source', args.source])
        
        cli_main()
        
    elif args.mode == 'web':
        # Import and run web server
        from api.app import app
        print("Starting Log Investigator Web Interface...")
        print("Frontend: http://localhost:4000")
        print("Backend:  http://localhost:8000")
        app.run(debug=True, host='0.0.0.0', port=8000)

if __name__ == "__main__":
    main() 