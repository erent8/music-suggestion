import requests  # For making HTTP requests to Spotify API
import random  # For selecting random songs
import os  # For file operations

# Spotify API Authorization token - replace 'YOUR_SPOTIFY_API_KEY' with your actual token
SPOTIFY_API_TOKEN = 'YOUR_SPOTIFY_API_KEY'

# File to store recommended songs
RECOMMENDED_SONGS_FILE = 'recommended_songs.txt'

# File to store liked songs
LIKED_SONGS_FILE = 'liked_songs.txt'

def fetch_from_spotify_api(endpoint, request_method, request_body=None):
    """
    Generic function to interact with Spotify's Web API.
    
    :param endpoint: The Spotify API endpoint (e.g., 'v1/me/top/tracks').
    :param request_method: The HTTP method ('GET' or 'POST').
    :param request_body: Optional JSON body for POST requests.
    :return: Parsed JSON response from Spotify API or None if an error occurs.
    """
    headers = {
        'Authorization': f'Bearer {SPOTIFY_API_TOKEN}',  # Add the authorization token
    }
    url = f'https://api.spotify.com/{endpoint}'  # Full API URL
    try:
        # Handle GET and POST requests
        if request_method == 'GET':
            response = requests.get(url, headers=headers)
        elif request_method == 'POST':
            response = requests.post(url, headers=headers, json=request_body)
        else:
            raise ValueError("Invalid HTTP method. Use 'GET' or 'POST'.")
        
        response.raise_for_status()  # Raise exception for HTTP errors
        return response.json()  # Return the parsed JSON response
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")  # Log errors if any
        return None

def get_top_tracks(limit=50):
    """
    Fetch the user's top tracks from Spotify.
    
    :param limit: Number of tracks to retrieve (maximum is 50).
    :return: List of top tracks or None if API call fails.
    """
    endpoint = f'v1/me/top/tracks?time_range=short_term&limit={limit}'
    return fetch_from_spotify_api(endpoint, 'GET')

def load_recommended_songs():
    """
    Load already recommended songs from a file.
    
    :return: A set of recommended songs.
    """
    if os.path.exists(RECOMMENDED_SONGS_FILE):
        with open(RECOMMENDED_SONGS_FILE, 'r') as file:
            return set(line.strip() for line in file)  # Read and return as a set
    return set()

def save_recommended_songs(songs):
    """
    Save newly recommended songs to a file.
    
    :param songs: List of songs to save.
    """
    with open(RECOMMENDED_SONGS_FILE, 'a') as file:
        for song in songs:
            file.write(f"{song}\n")  # Write each song on a new line

def load_liked_songs():
    """
    Load the user's liked songs from a file.
    
    :return: A list of liked songs.
    """
    if os.path.exists(LIKED_SONGS_FILE):
        with open(LIKED_SONGS_FILE, 'r') as file:
            return [line.strip() for line in file]  # Read and return as a list
    return []

def save_liked_song(song):
    """
    Save a single liked song to the liked songs file.
    
    :param song: The song to save.
    """
    with open(LIKED_SONGS_FILE, 'a') as file:
        file.write(f"{song}\n")  # Write the song on a new line

def get_random_tracks(limit=10):
    """
    Get random tracks from the user's top tracks.
    
    :param limit: The number of random tracks to fetch.
    :return: A list of formatted track strings.
    """
    top_tracks = get_top_tracks(limit)  # Fetch top tracks
    recommended_songs = load_recommended_songs()  # Load previously recommended songs
    
    if top_tracks and 'items' in top_tracks:
        # Randomly select tracks from the top tracks list
        random_tracks = random.sample(top_tracks['items'], min(limit, len(top_tracks['items'])))
        formatted_tracks = [
            f"{track['name']} by {', '.join([artist['name'] for artist in track['artists']])} (Album: {track['album']['name']})"
            for track in random_tracks
        ]
        # Exclude tracks already recommended
        new_tracks = [track for track in formatted_tracks if track not in recommended_songs]
        if new_tracks:
            save_recommended_songs(new_tracks)  # Save new recommendations
        return new_tracks
    else:
        return ["Top tracks could not be fetched."]

def create_playlist(name, track_uris):
    """
    Create a new playlist on Spotify and add tracks to it.
    
    :param name: The name of the playlist.
    :param track_uris: List of Spotify track URIs to add to the playlist.
    """
    endpoint = "v1/me/playlists"
    body = {
        "name": name,
        "description": "Playlist created with Music Suggestion app",
        "public": False  # Set playlist visibility to private
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
                # Save a liked song
                song_number = int(input("Enter the song number to like: "))
                if 1 <= song_number <= len(random_songs):
                    save_liked_song(random_songs[song_number - 1])
                    print("Song saved to Liked Songs.")
                else:
                    print("Invalid song number.")
            elif choice == "2":
                # Refresh the recommended songs
                random_songs = get_random_tracks(num_tracks)
                print("\nNew Recommended Songs:")
                for i, song in enumerate(random_songs, start=1):
                    print(f"{i}. {song}")
            elif choice == "3":
                # Create a Spotify playlist
                playlist_name = input("Enter a name for the playlist: ")
                track_uris = [f"spotify:track:{song.split(' - ')[0]}" for song in random_songs]
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
