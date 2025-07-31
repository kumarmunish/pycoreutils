#!/usr/bin/env python3
"""
Log analysis example using pycoreutils.
Demonstrates parsing and analyzing log files.
"""

from pycoreutils import FileOps, TextUtils, ProcessUtils
import re
from collections import Counter


def analyze_log_file(log_path):
    """Analyze a log file and extract useful statistics."""
    
    print(f"Analyzing log file: {log_path}")
    
    # Get basic file stats
    lines, words, chars = FileOps.wc(log_path)
    print(f"File stats: {lines} lines, {words} words, {chars} characters")
    
    # Find error lines
    error_lines = TextUtils.grep("ERROR|WARN", log_path, ignore_case=True)
    print(f"\nFound {len(error_lines)} error/warning lines:")
    for line in error_lines[:5]:  # Show first 5
        print(f"  {line}")
    
    # Analyze IP addresses (common log format)
    ip_pattern = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
    all_lines = FileOps.cat(log_path).split('\n')
    
    ips = []
    for line in all_lines:
        matches = re.findall(ip_pattern, line)
        ips.extend(matches)
    
    if ips:
        ip_counts = Counter(ips)
        print(f"\nTop 5 IP addresses:")
        for ip, count in ip_counts.most_common(5):
            print(f"  {ip}: {count} requests")
    
    # Find lines with specific status codes (if web logs)
    error_codes = TextUtils.grep(r' (4\d\d|5\d\d) ', log_path)
    print(f"\nHTTP error responses: {len(error_codes)}")
    
    return {
        'total_lines': lines,
        'error_lines': len(error_lines),
        'unique_ips': len(set(ips)) if ips else 0,
        'http_errors': len(error_codes)
    }


def create_sample_log():
    """Create a sample log file for demonstration."""
    
    sample_log = """2024-01-15 10:30:15 INFO 192.168.1.100 GET /index.html 200 1234
2024-01-15 10:30:16 INFO 192.168.1.101 GET /about.html 200 5678
2024-01-15 10:30:17 ERROR 192.168.1.102 GET /missing.html 404 0
2024-01-15 10:30:18 INFO 192.168.1.100 POST /login 200 890
2024-01-15 10:30:19 WARN 192.168.1.103 GET /admin 401 0
2024-01-15 10:30:20 INFO 192.168.1.101 GET /products 200 3456
2024-01-15 10:30:21 ERROR 192.168.1.104 GET /api/data 500 0
2024-01-15 10:30:22 INFO 192.168.1.100 GET /contact 200 2345
2024-01-15 10:30:23 INFO 192.168.1.105 GET /index.html 200 1234
2024-01-15 10:30:24 WARN 192.168.1.102 GET /restricted 403 0
"""
    
    with open("sample.log", "w") as f:
        f.write(sample_log)
    
    return "sample.log"


def main():
    """Main log analysis demo."""
    
    print("=== Log Analysis Demo ===\n")
    
    # Create sample log
    log_file = create_sample_log()
    print(f"Created sample log file: {log_file}")
    
    # Analyze the log
    stats = analyze_log_file(log_file)
    
    print(f"\n=== Analysis Summary ===")
    print(f"Total lines: {stats['total_lines']}")
    print(f"Error/Warning lines: {stats['error_lines']}")
    print(f"Unique IP addresses: {stats['unique_ips']}")
    print(f"HTTP errors: {stats['http_errors']}")
    
    # Demonstrate real-time log monitoring simulation
    print(f"\n=== Recent Activity (last 3 lines) ===")
    recent_lines = FileOps.tail(log_file, 3)
    for line in recent_lines:
        print(f"  {line}")
    
    # Clean up
    FileOps.rm(log_file)
    print(f"\nCleaned up {log_file}")


if __name__ == "__main__":
    main()
