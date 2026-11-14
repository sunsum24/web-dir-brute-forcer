# Web Directory Brute-Forcer

A multi-threaded Python script designed for Red Team engagements to discover hidden directories and files on web servers.

## The Problem
Web applications often contain hidden administrative panels, backup files, or configuration directories that are not linked in the main navigation. 

## The Solution
This script takes a target URL and a wordlist, firing HTTP GET requests to guess directory names. It uses `concurrent.futures` to scan multiple paths simultaneously, making it significantly faster than basic loops. It flags `200 OK`, `301/302 Redirect`, and `403 Forbidden` responses as valid finds.

## Usage
1. Ensure you have `requests` installed: `pip install requests`
2. Run the scanner:
`python dir_scanner.py <target_url> <wordlist.txt>`

*Disclaimer: This tool is for authorized penetration testing and educational purposes only.*
