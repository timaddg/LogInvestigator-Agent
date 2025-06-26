#!/usr/bin/env python3
"""
Log Downloader CLI for Log Investigator.
Download sample log files from various online sources.
"""

import sys
import argparse
from log_downloader import LogDownloader
from utils import print_header, print_info, print_success, print_error


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Download sample log files for Log Investigator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python download_logs.py --list                    # List all available sources
  python download_logs.py --download nginx_logs     # Download nginx logs
  python download_logs.py --download-all            # Download all sources
  python download_logs.py --convert nginx_logs      # Download and convert to JSON
        """
    )
    
    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help='List all available log sources'
    )
    
    parser.add_argument(
        '--download', '-d',
        type=str,
        help='Download logs from specific source'
    )
    
    parser.add_argument(
        '--download-all', '-a',
        action='store_true',
        help='Download all available log sources'
    )
    
    parser.add_argument(
        '--convert', '-c',
        type=str,
        help='Download and convert logs to JSON format'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Output file name (default: auto-generated)'
    )
    
    parser.add_argument(
        '--output-dir', '-D',
        type=str,
        default='downloaded_logs',
        help='Output directory for downloads (default: downloaded_logs)'
    )
    
    args = parser.parse_args()
    
    # Initialize downloader
    downloader = LogDownloader()
    
    try:
        if args.list:
            print_header("Available Log Sources")
            downloader.list_sources()
            
        elif args.download:
            print_header(f"Downloading {args.download}")
            result = downloader.download_logs(args.download, args.output)
            if result:
                print_success(f"Successfully downloaded to: {result}")
                print_info("You can now use this file with your Log Investigator!")
                
        elif args.download_all:
            print_header("Downloading All Log Sources")
            sources = list(downloader.get_available_sources().keys())
            print_info(f"Downloading {len(sources)} sources...")
            
            results = downloader.download_multiple_sources(sources, args.output_dir)
            if results:
                print_success(f"Successfully downloaded {len(results)} files to {args.output_dir}/")
                print_info("Files downloaded:")
                for file in results:
                    print(f"  - {file}")
                    
        elif args.convert:
            print_header(f"Downloading and Converting {args.convert}")
            result = downloader.download_and_convert_to_json(args.convert, args.output)
            if result:
                print_success(f"Successfully converted to: {result}")
                print_info("This JSON file is ready for Log Investigator analysis!")
                
        else:
            parser.print_help()
            
    except KeyboardInterrupt:
        print_error("Download interrupted by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 