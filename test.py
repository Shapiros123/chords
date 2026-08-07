import pandas as pd
import json

df = pd.read_csv("tab4u_guitar_urls_only.csv")
songs = []
for url in df['song_url'].tolist():
    filename = url.split('/')[-1].replace('.html', '')
    parts = filename.split('_', 1)
    name_part = parts[1] if len(parts) > 1 else filename
    if "_-_" in name_part:
        artist, title = name_part.split("_-_", 1)
    else:
        artist, title = "Unknown", name_part
    songs.append({
        "Artist": artist.replace('_', ' '),
        "Title": title.replace('_', ' '),
        "URL": url
    })

# Save it directly inside the api folder
with open("api/songs.json", "w", encoding="utf-8") as f:
    json.dump(songs, f, ensure_ascii=False, indent=4)

print("Created api/songs.json successfully!")