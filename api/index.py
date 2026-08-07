from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse, unquote
import json
import requests
from bs4 import BeautifulSoup
import os
import pandas as pd

csv_path = os.path.join(os.path.dirname(__file__), '..', 'tab4u_guitar_urls_only.csv')
df = pd.read_csv(csv_path)


def extract_names_from_url(url):
    filename = url.split('/')[-1].replace('.html', '')

    # Decode the percent-encoded Hebrew characters into real text
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