import requests
import random

# Spotify API Authorization token
# Spotify API anahtarınızı buraya ekleyin
SPOTIFY_API_TOKEN = 'YOUR_SPOTIFY_API_KEY'

def fetch_from_spotify_api(endpoint, request_method, request_body=None):
    """
    Spotify Web API'dan veri çeken fonksiyon.

    :param endpoint: API'nin istek yapılacak endpoint'i
    :param request_method: HTTP metodunu belirtir ('GET' veya 'POST')
    :param request_body: POST isteği için gerekli veri (varsayılan: None)
    :return: API'dan gelen yanıtın JSON formatında verilmiş hali
    """
    headers = {
        'Authorization': f'Bearer {SPOTIFY_API_TOKEN}',
    }
    
    url = f'https://api.spotify.com/{endpoint}'
    
    if request_method == 'GET':
        response = requests.get(url, headers=headers)
    elif request_method == 'POST':
        response = requests.post(url, headers=headers, json=request_body)
    else:
        raise ValueError("Geçersiz HTTP metodu. 'GET' veya 'POST' kullanılmalıdır.")
    
    response.raise_for_status()  # HTTP hata kodlarına karşı bir istisna fırlatır
    return response.json()

def get_top_tracks(limit=50):
    """
    Kullanıcının en popüler şarkılarını alır.

    :param limit: Alınacak şarkı sayısı (varsayılan: 50)
    :return: En popüler şarkıların JSON formatında listesi
    """
    endpoint = f'v1/me/top/tracks?time_range=short_term&limit={limit}'
    return fetch_from_spotify_api(endpoint, 'GET')

def get_random_tracks(limit=10):
    """
    Rastgele şarkılar seçer ve bunları formatlar.

    :param limit: Seçilecek rastgele şarkı sayısı (varsayılan: 10)
    :return: Rastgele seçilmiş şarkıların formatlanmış listesi
    """
    top_tracks = get_top_tracks(limit)
    
    if 'items' in top_tracks:
        random_tracks = random.sample(top_tracks['items'], min(limit, len(top_tracks['items'])))
        formatted_tracks = [
            f"{track['name']} by {', '.join([artist['name'] for artist in track['artists']])}"
            for track in random_tracks
        ]
        return formatted_tracks
    else:
        return ["Top tracks could not be fetched."]

def main():
    """
    Programın ana fonksiyonu. Şarkıları alır ve ekrana basar.
    """
    num_tracks = 15  # Almak istediğiniz şarkı sayısını burada ayarlayın
    random_songs = get_random_tracks(num_tracks)
    
    print("Önerilen Şarkılar:")
    for i, song in enumerate(random_songs, start=1):
        print(f"{i}. {song}")

if __name__ == "__main__":
    main()
