"""
Utilities module for Log Investigator.
Common helper functions and display formatting.
"""

import sys
from typing import Dict, Any, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

console = Console()


def print_header(title: str) -> None:
    """Print a formatted header."""
    console.print(f"\n🔍 {title}", style="bold blue")
    console.print("=" * 60, style="blue")


def print_success(message: str) -> None:
    """Print a success message."""
    console.print(f"✅ {message}", style="bold green")


def print_error(message: str) -> None:
    """Print an error message."""
    console.print(f"❌ {message}", style="bold red")


def print_warning(message: str) -> None:
    """Print a warning message."""
    console.print(f"⚠️ {message}", style="bold yellow")


def print_info(message: str) -> None:
    """Print an info message."""
    console.print(f"ℹ️ {message}", style="bold cyan")


def display_log_statistics(stats: Dict[str, Any]) -> None:
    """Display log statistics in a formatted table."""
    if not stats:
        print_warning("No statistics available")
        return
    
    table = Table(title="Log Statistics")
    table.add_column("Metric", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")
    
    # Basic stats
    table.add_row("Total Entries", str(stats.get('total_entries', 0)))
    table.add_row("Errors", str(stats.get('error_count', 0)))
    table.add_row("Warnings", str(stats.get('warning_count', 0)))
    
    # Time range
    time_range = stats.get('time_range', {})
    if time_range.get('earliest') and time_range.get('latest'):
        table.add_row("Time Range", f"{time_range['earliest']} to {time_range['latest']}")
    
    console.print(table)
    
    # Log levels breakdown
    if stats.get('levels'):
        levels_table = Table(title="Log Levels Breakdown")
        levels_table.add_column("Level", style="cyan")
        levels_table.add_column("Count", style="magenta")
        
        for level, count in stats['levels'].items():
            levels_table.add_row(level, str(count))
        
        console.print(levels_table)
    
    # Services breakdown
    if stats.get('services'):
        services_table = Table(title="Services Breakdown")
        services_table.add_column("Service", style="cyan")
        services_table.add_column("Count", style="magenta")
        
        for service, count in stats['services'].items():
            services_table.add_row(service, str(count))
        
        console.print(services_table)


def display_analysis_results(analysis: str) -> None:
    """Display AI analysis results in a formatted panel."""
    if not analysis:
        print_error("No analysis results to display")
        return
    
    panel = Panel(
        Text(analysis, style="white"),
        title="AI Analysis Results",
        border_style="blue",
        padding=(1, 2)
    )
    console.print(panel)


def format_duration(seconds: float) -> str:
    """Format duration in a human-readable way."""
    if seconds < 1:
        return f"{seconds * 1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"


def exit_with_error(message: str, exit_code: int = 1) -> None:
    """Exit the application with an error message."""
    print_error(message)
    sys.exit(exit_code)


def exit_success(message: str = "Analysis complete!") -> None:
    """Exit the application with a success message."""
    print_success(message)
    sys.exit(0)


def validate_file_exists(file_path: str) -> bool:
    """Validate that a file exists."""
    import os
    if not os.path.exists(file_path):
        print_error(f"File not found: {file_path}")
        return False
    return True


def get_file_size(file_path: str) -> str:
    """Get human-readable file size."""
    import os
    try:
        size_bytes = os.path.getsize(file_path)
        if size_bytes < 1024:
            return f"{size_bytes}B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f}KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f}MB"
    except OSError:
        return "Unknown" 