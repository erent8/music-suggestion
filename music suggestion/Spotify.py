import requests
import random
import os

# Spotify API Authorization token
SPOTIFY_API_TOKEN = 'YOUR_SPOTIFY_API_KEY'
RECOMMENDED_SONGS_FILE = 'recommended_songs.txt'
LIKED_SONGS_FILE = 'liked_songs.txt'

def fetch_from_spotify_api(endpoint, request_method, request_body=None):
    headers = {
        'Authorization': f'Bearer {SPOTIFY_API_TOKEN}',
    }
    url = f'https://api.spotify.com/{endpoint}'
    try:
        if request_method == 'GET':
            response = requests.get(url, headers=headers)
        elif request_method == 'POST':
            response = requests.post(url, headers=headers, json=request_body)
        else:
            raise ValueError("Invalid HTTP method. Use 'GET' or 'POST'.")
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return None

def get_top_tracks(limit=50):
    endpoint = f'v1/me/top/tracks?time_range=short_term&limit={limit}'
    return fetch_from_spotify_api(endpoint, 'GET')

def load_recommended_songs():
    if os.path.exists(RECOMMENDED_SONGS_FILE):
        with open(RECOMMENDED_SONGS_FILE, 'r') as file:
            return set(line.strip() for line in file)
    return set()

def save_recommended_songs(songs):
    with open(RECOMMENDED_SONGS_FILE, 'a') as file:
        for song in songs:
            file.write(f"{song}\n")

def load_liked_songs():
    if os.path.exists(LIKED_SONGS_FILE):
        with open(LIKED_SONGS_FILE, 'r') as file:
            return [line.strip() for line in file]
    return []

def save_liked_song(song):
    with open(LIKED_SONGS_FILE, 'a') as file:
        file.write(f"{song}\n")

def get_random_tracks(limit=10):
    top_tracks = get_top_tracks(limit)
    recommended_songs = load_recommended_songs()
    
    if top_tracks and 'items' in top_tracks:
        random_tracks = random.sample(top_tracks['items'], min(limit, len(top_tracks['items'])))
        formatted_tracks = [
            f"{track['name']} by {', '.join([artist['name'] for artist in track['artists']])} (Album: {track['album']['name']})"
            for track in random_tracks
        ]
        new_tracks = [track for track in formatted_tracks if track not in recommended_songs]
        if new_tracks:
            save_recommended_songs(new_tracks)
        return new_tracks
    else:
        return ["Top tracks could not be fetched."]

def create_playlist(name, track_uris):
    endpoint = "v1/me/playlists"
    body = {
        "name": name,
        "description": "Playlist created with Music Suggestion app",
        "public": False
    }
    playlist_response = fetch_from_spotify_api(endpoint, "POST", body)
    if playlist_response and "id" in playlist_response:
        playlist_id = playlist_response["id"]
        endpoint = f"v1/playlists/{playlist_id}/tracks"
        fetch_from_spotify_api(endpoint, "POST", {"uris": track_uris})
        print(f"Playlist '{name}' created successfully!")
    else:
        print("Failed to create playlist.")

def main():
    num_tracks = 15
    random_songs = get_random_tracks(num_tracks)
    
    print("\nRecommended Songs:")
    if random_songs:
        for i, song in enumerate(random_songs, start=1):
            print(f"{i}. {song}")
        while True:
            print("\nOptions:")
            print("1. Save a song to Liked Songs")
            print("2. Refresh Recommendations")
            print("3. Create a Spotify Playlist from Recommendations")
            print("4. View Liked Songs")
            print("5. Exit")
            
            choice = input("Choose an option: ")
            if choice == "1":
                song_number = int(input("Enter the song number to like: "))
                if 1 <= song_number <= len(random_songs):
                    save_liked_song(random_songs[song_number - 1])
                    print("Song saved to Liked Songs.")
                else:
                    print("Invalid song number.")
            elif choice == "2":
                random_songs = get_random_tracks(num_tracks)
                print("\nNew Recommended Songs:")
                for i, song in enumerate(random_songs, start=1):
                    print(f"{i}. {song}")
            elif choice == "3":
                playlist_name = input("Enter a name for the playlist: ")
                track_uris = [f"spotify:track:{song.split(' - ')[0]}" for song in random_songs]
                create_playlist(playlist_name, track_uris)
            elif choice == "4":
                liked_songs = load_liked_songs()
                if liked_songs:
                    print("\nLiked Songs:")
                    for i, song in enumerate(liked_songs, start=1):
                        print(f"{i}. {song}")
                else:
                    print("No liked songs yet.")
            elif choice == "5":
                break
            else:
                print("Invalid choice. Please try again.")
    else:
        print("No new song recommendations found.")

if __name__ == "__main__":
    main()
