from flask import Flask, jsonify, request
import os
import json
import re

app = Flask(__name__)

# Load song directory from the JSON file on cold start
json_path = os.path.join(os.path.dirname(__file__), 'songs.json')
with open(json_path, 'r', encoding='utf-8') as f:
    song_directory = json.load(f)


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
        for br in content_div.find_all("br"):
            br.replace_with("\n")

        for row in content_div.find_all(['tr', 'p', 'div']):
            text = row.get_text().replace('\xa0', ' ')
            # Compress runs of 7 or more spaces down to 1 space
            cleaned = re.sub(r' {7,}', ' ', text).rstrip('\n\r')
            if cleaned.strip():
                extracted_lines.append(cleaned)

    if not extracted_lines and content_div:
        raw_text = content_div.get_text().replace('\xa0', ' ')
        extracted_lines = [re.sub(r' {7,}', ' ', line).rstrip('\n\r') for line in raw_text.splitlines() if line.strip()]

    # Strip uniform leading indentation
    non_empty = [l for l in extracted_lines if l.strip()]
    if non_empty:
        min_indent = min(len(l) - len(l.lstrip(' \t')) for l in non_empty)
        if min_indent > 0:
            extracted_lines = [l[min_indent:] if len(l) >= min_indent and l[:min_indent].isspace() else l for l in
                               extracted_lines]

    normalized_text = "\n".join(extracted_lines)
    normalized_text = re.sub(r'\n{3,}', '\n\n', normalized_text).strip()

    return jsonify({"content": normalized_text})