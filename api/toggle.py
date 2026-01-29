from http.server import BaseHTTPRequestHandler
import json
import requests

# Your Credentials
API_KEY = "65cfb3f31b90b2e9b429422f8781660a1a2a08b9"
CONFIG_ID = "d6ddb9"
DOMAIN = "ppq.apple.com"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = f"https://api.nextdns.io/profiles/{CONFIG_ID}/denylist"
        headers = {"X-Api-Key": API_KEY, "Content-Type": "application/json"}

        # 1. Check if domain is already blocked
        response = requests.get(url, headers=headers)
        data = response.json().get('data', [])
        is_blocked = any(item.get('id') == DOMAIN for item in data)

        if is_blocked:
            # 2. If blocked, DELETE (Unblock)
            delete_url = f"{url}/{DOMAIN}"
            requests.delete(delete_url, headers=headers)
            status = "Unblocked"
        else:
            # 3. If not blocked, POST (Block)
            requests.post(url, headers=headers, json={"id": DOMAIN})
            status = "Blocked"

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "success", "action": status}).encode())
