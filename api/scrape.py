from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import json
import requests
from bs4 import BeautifulSoup
import os

# Load the song directory from the local JSON file
json_path = os.path.join(os.path.dirname(__file__), 'songs.json')
with open(json_path, 'r', encoding='utf-8') as f:
    song_directory = json.load(f)


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        # Route 1: Serve the song index
        if parsed_path.path == '/api/songs':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(song_directory, ensure_ascii=False).encode('utf-8'))
            return

        # Route 2: Scrape a specific song on demand
        elif parsed_path.path == '/api/scrape':
            url_list = query_params.get('url')
            if not url_list:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": "No URL provided"}).encode('utf-8'))
                return

            target_url = url_list[0]
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(target_url, headers=headers)

            if response.status_code != 200:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Failed to fetch song"}).encode('utf-8'))
                return

            soup = BeautifulSoup(response.text, 'html.parser')
            extracted_lines = []
            content_div = soup.find('div', id='songContentTPL')

            if content_div:
                for row in content_div.find_all('tr'):
                    line = row.get_text().replace('\xa0', ' ')
                    if line.strip():
                        extracted_lines.append(line.rstrip('\n'))

            result = {"content": "\n".join(extracted_lines)}

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result, ensure_ascii=False).encode('utf-8'))
            return

        else:
            self.send_response(404)
            self.end_headers()