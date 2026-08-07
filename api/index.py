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
        for row in content_div.find_all('tr'):
            line = row.get_text().replace('\xa0', ' ')
            extracted_lines.append(line.rstrip('\n\r'))

    # Backend Smart Indentation Stripper: removes uniform table offsets while keeping relative chord spaces
    non_empty_lines = [l for l in extracted_lines if l.strip()]
    if non_empty_lines:
        min_indent = float('inf')
        for l in non_empty_lines:
            leading_spaces = len(l) - len(l.lstrip(' \t'))
            if leading_spaces < min_indent:
                min_indent = leading_spaces

        if min_indent != float('inf') and min_indent > 0:
            trimmed_lines = []
            for l in extracted_lines:
                if len(l) >= min_indent and l[:min_indent].isspace():
                    trimmed_lines.append(l[min_indent:])
                else:
                    trimmed_lines.append(l)
            extracted_lines = trimmed_lines

    raw_text = "\n".join(extracted_lines)
    normalized_text = re.sub(r'\n{3,}', '\n\n', raw_text).strip()

    return jsonify({"content": normalized_text})