import requests
import random
import os
from dataclasses import dataclass
from typing import List, Optional

# Spotify API Authorization token
SPOTIFY_API_TOKEN = os.getenv('SPOTIFY_API_TOKEN', 'YOUR_SPOTIFY_API_KEY')

# File paths
RECOMMENDED_SONGS_FILE = 'recommended_songs.txt'
LIKED_SONGS_FILE = 'liked_songs.txt'

@dataclass
class Track:
    id: str
    name: str
    artists: List[str]
    album_name: str
    album_image_url: str
    preview_url: Optional[str]
    uri: str

    def format_display(self) -> str:
        artists_str = ', '.join(self.artists)
        return f"{self.name} by {artists_str} (Album: {self.album_name})"

def fetch_from_spotify_api(endpoint, request_method, request_body=None):
    """
    Generic function to interact with Spotify's Web API.
    """
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
    """
    Fetch the user's top tracks from Spotify.
    """
    endpoint = f'v1/me/top/tracks?time_range=short_term&limit={limit}'
    return fetch_from_spotify_api(endpoint, 'GET')

def parse_track_data(track_data) -> Track:
    """
    Parse raw track data from Spotify API into Track object.
    """
    return Track(
        id=track_data['id'],
        name=track_data['name'],
        artists=[artist['name'] for artist in track_data['artists']],
        album_name=track_data['album']['name'],
        album_image_url=track_data['album']['images'][0]['url'] if track_data['album']['images'] else None,
        preview_url=track_data.get('preview_url'),
        uri=track_data['uri']
    )

def get_track_recommendations(seed_tracks: List[str], limit=10):
    """
    Get track recommendations based on seed tracks.
    """
    seed_tracks_str = ','.join(seed_tracks[:5])  # Spotify allows max 5 seed tracks
    endpoint = f'v1/recommendations?seed_tracks={seed_tracks_str}&limit={limit}'
    response = fetch_from_spotify_api(endpoint, 'GET')
    
    if response and 'tracks' in response:
        return [parse_track_data(track) for track in response['tracks']]
    return []

def load_recommended_songs():
    """
    Load already recommended songs from a file.
    """
    if os.path.exists(RECOMMENDED_SONGS_FILE):
        with open(RECOMMENDED_SONGS_FILE, 'r') as file:
            return set(line.strip() for line in file)
    return set()

def save_recommended_songs(songs: List[Track]):
    """
    Save newly recommended songs to a file.
    """
    with open(RECOMMENDED_SONGS_FILE, 'a') as file:
        for song in songs:
            file.write(f"{song.format_display()}\n")

def load_liked_songs():
    """
    Load the user's liked songs from a file.
    """
    if os.path.exists(LIKED_SONGS_FILE):
        with open(LIKED_SONGS_FILE, 'r') as file:
            return [line.strip() for line in file]
    return []

def save_liked_song(song: str):
    """
    Save a single liked song to the liked songs file.
    """
    with open(LIKED_SONGS_FILE, 'a') as file:
        file.write(f"{song}\n")

def get_random_tracks(limit=10) -> List[Track]:
    """
    Get random tracks from the user's top tracks and recommendations.
    """
    top_tracks_response = get_top_tracks(limit)
    recommended_songs = load_recommended_songs()
    
    if top_tracks_response and 'items' in top_tracks_response:
        top_tracks = [parse_track_data(track) for track in top_tracks_response['items']]
        
        # Get seed tracks for recommendations
        seed_tracks = random.sample([track.id for track in top_tracks], min(5, len(top_tracks)))
        recommended_tracks = get_track_recommendations(seed_tracks, limit)
        
        # Combine and shuffle tracks
        all_tracks = top_tracks + recommended_tracks
        random_tracks = random.sample(all_tracks, min(limit, len(all_tracks)))
        
        # Filter out already recommended songs
        new_tracks = [track for track in random_tracks 
                     if track.format_display() not in recommended_songs]
        
        if new_tracks:
            save_recommended_songs(new_tracks)
        return new_tracks
    return []

def create_playlist(name: str, track_uris: List[str]):
    """
    Create a new playlist on Spotify and add tracks to it.
    """
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
    """
    Main function to display recommended songs and handle user interaction.
    """
    num_tracks = 15  # Number of random tracks to recommend
    random_songs = get_random_tracks(num_tracks)  # Get random songs
    
    print("\nRecommended Songs:")
    if random_songs:
        for i, song in enumerate(random_songs, start=1):
            print(f"{i}. {song.format_display()}")
        while True:
            print("\nOptions:")
            print("1. Save a song to Liked Songs")
            print("2. Refresh Recommendations")
            print("3. Create a Spotify Playlist from Recommendations")
            print("4. View Liked Songs")
            print("5. Exit")
            
            choice = input("Choose an option: ")
            if choice == "1":
                # Save a liked song
                song_number = int(input("Enter the song number to like: "))
                if 1 <= song_number <= len(random_songs):
                    save_liked_song(random_songs[song_number - 1].format_display())
                    print("Song saved to Liked Songs.")
                else:
                    print("Invalid song number.")
            elif choice == "2":
                # Refresh the recommended songs
                random_songs = get_random_tracks(num_tracks)
                print("\nNew Recommended Songs:")
                for i, song in enumerate(random_songs, start=1):
                    print(f"{i}. {song.format_display()}")
            elif choice == "3":
                # Create a Spotify playlist
                playlist_name = input("Enter a name for the playlist: ")
                track_uris = [f"spotify:track:{song.id}" for song in random_songs]
                create_playlist(playlist_name, track_uris)
            elif choice == "4":
                # View liked songs
                liked_songs = load_liked_songs()
                if liked_songs:
                    print("\nLiked Songs:")
                    for i, song in enumerate(liked_songs, start=1):
                        print(f"{i}. {song}")
                else:
                    print("No liked songs yet.")
            elif choice == "5":
                # Exit the program
                break
            else:
                print("Invalid choice. Please try again.")
    else:
        print("No new song recommendations found.")

if __name__ == "__main__":
    main()
