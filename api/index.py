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

    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(target_url, headers=headers)

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch song"}), 500

    soup = BeautifulSoup(response.text, 'html.parser')
    content_div = soup.find('div', id='songContentTPL')

    if not content_div:
        return jsonify({"error": "Song content not found"}), 404

    # Clean out ads, scripts, and unnecessary elements
    for unwanted in content_div.find_all(['script', 'style', 'iframe', 'ins', 'ads']):
        unwanted.decompose()

    # Return the raw native HTML structure so the browser renders Tab4U's layout grid natively
    return jsonify({"html": str(content_div)})