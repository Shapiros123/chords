from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import json
import requests
from bs4 import BeautifulSoup
import os
import pandas as pd

# Load the CSV once when the function cold-starts
csv_path = os.path.join(os.path.dirname(__file__), '..', 'tab4u_guitar_urls_only.csv')
df = pd.read_csv(csv_path)


def extract_names_from_url(url):
    filename = url.split('/')[-1].replace('.html', '')
    parts = filename.split('_', 1)
    name_part = parts[1] if len(parts) > 1 else filename
    if "_-_" in name_part:
        artist, title = name_part.split("_-_", 1)
    else:
        artist, title = "Unknown", name_part
    return {
        "Artist": artist.replace('_', ' '),
        "Title": title.replace('_', ' '),
        "URL": url
    }


song_directory = [extract_names_from_url(url) for url in df['song_url'].tolist()]


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        # Route 1: Get the list of songs for the sidebar
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

            # Scrape Tab4U live
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