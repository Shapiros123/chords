from flask import Flask, jsonify, request
import os
import pandas as pd
from urllib.parse import unquote

app = Flask(__name__)

# Load CSV data once on cold start
csv_path = os.path.join(os.path.dirname(__file__), '..', 'tab4u_guitar_urls_only.csv')
df = pd.read_csv(csv_path)


def extract_names_from_url(url):
    filename = url.split('/')[-1].replace('.html', '')
    decoded_filename = unquote(filename)
    parts = decoded_filename.split('_', 1)
    name_part = parts[1] if len(parts) > 1 else decoded_filename
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


@app.route('/api/songs', methods=['GET'])
def get_songs():
    return jsonify(song_directory)


@app.route('/api/scrape', methods=['GET'])
def scrape_song():
    target_url = request.args.get('url')
    if not target_url:
        return jsonify({"error": "No URL provided"}), 400

    import requests
    from bs4 import BeautifulSoup

    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(target_url, headers=headers)

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch song"}), 500

    soup = BeautifulSoup(response.text, 'html.parser')
    extracted_lines = []
    content_div = soup.find('div', id='songContentTPL')

    if content_div:
        for row in content_div.find_all('tr'):
            line = row.get_text().replace('\xa0', ' ')
            if line.strip():
                extracted_lines.append(line.rstrip('\n'))

    return jsonify({"content": "\n".join(extracted_lines)})