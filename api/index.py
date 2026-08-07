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
        # Tab4U organizes song text inside HTML table rows and cells with website padding
        for row in content_div.find_all('tr'):
            cells = row.find_all(['td', 'th'])
            if cells:
                cell_texts = []
                for cell in cells:
                    # Normalize all unicode spaces inside each cell
                    t = cell.get_text().replace('\xa0', ' ').replace('\u200b', '').replace('\u3000', ' ')
                    t = re.sub(r'[\u00a0\u1680\u2000-\u200a\u2028\u2029\u202f\u205f]', ' ', t).strip()
                    if t:
                        cell_texts.append(t)
                # Combine table cells cleanly with a fixed separation space
                line = "   ".join(cell_texts)
            else:
                line = row.get_text().replace('\xa0', ' ').replace('\u200b', '')

            cleaned = line.rstrip('\n\r')
            if cleaned.strip():
                extracted_lines.append(cleaned)

    # Fallback if no table structure is found
    if not extracted_lines and content_div:
        raw_text = content_div.get_text().replace('\xa0', ' ').replace('\u200b', '')
        for line in raw_text.splitlines():
            cleaned_line = line.rstrip('\n\r')
            if cleaned_line.strip():
                extracted_lines.append(cleaned_line)

    # Clean leading uniform block indentation
    non_empty = [l for l in extracted_lines if l.strip()]
    if non_empty:
        min_indent = min(len(l) - len(l.lstrip(' \t')) for l in non_empty)
        if min_indent > 0:
            extracted_lines = [l[min_indent:] if len(l) >= min_indent and l[:min_indent].isspace() else l for l in
                               extracted_lines]

    normalized_text = "\n".join(extracted_lines)
    normalized_text = re.sub(r'\n{3,}', '\n\n', normalized_text).strip()

    return jsonify({"content": normalized_text})