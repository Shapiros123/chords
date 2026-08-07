from flask import Flask, jsonify, request
import os
import json
from bs4 import BeautifulSoup
import requests

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

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9,he;q=0.8'
    }

    try:
        response = requests.get(target_url, headers=headers, timeout=10)
        # Automatically detect and apply correct Hebrew encoding
        response.encoding = response.apparent_encoding

        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch song from source"}), 500

        soup = BeautifulSoup(response.text, 'html.parser')

        # Target Tab4U's native content containers
        content_div = soup.find('div', id='songContentTPL') or soup.find('div', id='songContent') or soup.find('div',
                                                                                                               class_='song_block')

        if not content_div:
            return jsonify({"error": "Song content block not found"}), 404

        # Clean out ads, scripts, and unnecessary elements
        for unwanted in content_div.find_all(['script', 'style', 'iframe', 'ins', 'ads']):
            unwanted.decompose()

        # Strip inline event handlers (onmouseover, onclick, etc.) left over
        # from tab4u's own JS (e.g. sCI/CO chord-tooltip functions) which
        # don't exist on our page and throw console errors on hover/click.
        for tag in content_div.find_all(True):
            for attr in list(tag.attrs):
                if attr.startswith('on'):
                    del tag.attrs[attr]

        # Normalize non-breaking spaces (&nbsp; / \xa0) to regular spaces
        html_output = str(content_div).replace('\xa0', ' ')

        return jsonify({"html": html_output})

    except Exception as e:
        return jsonify({"error": str(e)}), 500