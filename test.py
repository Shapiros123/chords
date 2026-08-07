import json
from urllib.parse import unquote

with open("api/songs.json", "r", encoding="utf-8") as f:
    songs = json.load(f)

for song in songs:
    # Decode percent-encoded text for both Title and Artist
    decoded_url = unquote(song["URL"])
    filename = decoded_url.split('/')[-1].replace('.html', '')
    parts = filename.split('_', 1)
    name_part = parts[1] if len(parts) > 1 else filename
    if "_-_" in name_part:
        artist, title = name_part.split("_-_", 1)
    else:
        artist, title = "Unknown", name_part

    song["Artist"] = artist.replace('_', ' ')
    song["Title"] = title.replace('_', ' ')

with open("api/songs.json", "w", encoding="utf-8") as f:
    json.dump(songs, f, ensure_ascii=False, indent=4)

print("Successfully fixed and decoded api/songs.json!")