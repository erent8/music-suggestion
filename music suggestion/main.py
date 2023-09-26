import requests
import random

# Spotify API Authorization token
token = 'BQDk_rrqrpKNc0BIa63z5XTBfsRagBVIM8Dlw2ffoeMb2_fKD-NecCxzXsmOuquS8QTGtf7xOY1xqQGCOKZ38Xq5uQ0-WFS2GO75VjzI_6IiUFJDYtykzXBMMWdqgxTuXn4DJ4zcXPHbyqaOkb62BIexkjuzmUBY31Yq69sPFkW4AEfhPRi5azHFLCYDmwI_IHKyScfXdLMF1tqBM-cQ1ZTUo5r2mzoktLB7T5atDP1eFqYITCZSanLwJA0oxMWeN85PZ69ULbay9aUzJuyXv1z7KcMz'

def fetch_web_api(endpoint, method, body=None):
    headers = {
        'Authorization': f'Bearer {token}',
    }

    url = f'https://api.spotify.com/{endpoint}'
    if method == 'GET':
        response = requests.get(url, headers=headers)
    elif method == 'POST':
        response = requests.post(url, headers=headers, json=body)

    return response.json()

def get_top_tracks(limit=100):
    endpoint = f'v1/me/top/tracks?time_range=short_term&limit={limit}'
    return fetch_web_api(endpoint, 'GET')

def get_random_tracks(limit=10):
    top_tracks = get_top_tracks(limit)
    if 'items' in top_tracks:
        random_tracks = random.sample(top_tracks['items'], limit)
        return [
            f"{track['name']} by {', '.join([artist['name'] for artist in track['artists']])}"
            for track in random_tracks
        ]
    else:
        return ["Top tracks could not be fetched."]

num_tracks = 50  # Almak istediğiniz şarkı sayısını burada ayarlayın
random_songs = get_random_tracks(num_tracks)
print("Önerilen Şarkılar:")
for i, song in enumerate(random_songs, start=1):
    print(f"{i}. {song}")
