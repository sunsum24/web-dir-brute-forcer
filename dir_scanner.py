import requests
import sys
from concurrent.futures import ThreadPoolExecutor

# Suppress harmless SSL warnings for testing environments
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def check_directory(base_url, directory):
    # Ensure the URL ends with a slash and doesn't have double slashes
    url = f"{base_url.rstrip('/')}/{directory}"
    
    try:
        # We use a timeout so the script doesn't hang on bad connections
        response = requests.get(url, timeout=3, verify=False, allow_redirects=False)
        
        # If the server returns a 200 OK, the directory likely exists
        if response.status_code == 200:
            print(f"[+] Found: {url} (Status: 200 OK)")
        # 301/302 means it exists but is redirecting (e.g., to a login page)
        elif response.status_code in [301, 302, 403]:
            print(f"[!] Found: {url} (Status: {response.status_code})")
            
    except requests.exceptions.RequestException:
        pass # Ignore connection errors and timeouts

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python dir_scanner.py <target_url> <wordlist_file>")
        print("Example: python dir_scanner.py http://scanme.nmap.org wordlist.txt")
        sys.exit(1)
        
    target = sys.argv[1]
    wordlist = sys.argv[2]
    
    print(f"[*] Starting directory brute-force on: {target}")
    
    try:
        with open(wordlist, 'r') as f:
            directories = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[-] Error: Wordlist '{wordlist}' not found.")
        sys.exit(1)

    # Use ThreadPoolExecutor to scan multiple directories at once (faster)
    print(f"[*] Loaded {len(directories)} words. Starting threads...\n")
    with ThreadPoolExecutor(max_workers=10) as executor:
        for directory in directories:
            executor.submit(check_directory, target, directory)
            
    print("\n[*] Scan complete.")
