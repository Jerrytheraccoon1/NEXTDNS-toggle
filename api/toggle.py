from http.server import BaseHTTPRequestHandler
import json
import urllib.request
import urllib.parse

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        API_KEY = "65cfb3f31b90b2e9b429422f8781660a1a2a08b9"
        CONFIG_ID = "d6ddb9"
        DOMAIN = "ppq.apple.com"
        
        base_url = f"https://api.nextdns.io/profiles/{CONFIG_ID}/denylist"
        headers = {"X-Api-Key": API_KEY, "Content-Type": "application/json"}

        try:
            # 1. Check current status (GET)
            req = urllib.request.Request(base_url, headers=headers)
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                domains = data.get('data', [])
                is_blocked = any(d.get('id') == DOMAIN for d in domains)

            if is_blocked:
                # 2. DELETE (Unblock)
                delete_url = f"{base_url}/{DOMAIN}"
                del_req = urllib.request.Request(delete_url, headers=headers, method='DELETE')
                urllib.request.urlopen(del_req)
                res_msg = f"UNBLOCKED: {DOMAIN}"
            else:
                # 3. POST (Block)
                post_data = json.dumps({"id": DOMAIN}).encode('utf-8')
                post_req = urllib.request.Request(base_url, data=post_data, headers=headers, method='POST')
                urllib.request.urlopen(post_req)
                res_msg = f"BLOCKED: {DOMAIN}"

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"result": res_msg}).encode())

        except Exception as e:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
