# Music Suggestion
![download](https://github.com/user-attachments/assets/84ee6c6a-a3e2-4228-982f-19fb0a4cab9d)

Bu proje, Spotify API kullanarak kullanıcıya şarkı önerileri sunan bir Python uygulamasıdır. Kullanıcının en popüler şarkılarını ve benzer şarkıları alarak rastgele öneriler sunar.

## Özellikler

- Modern grafik kullanıcı arayüzü (GUI)
- Albüm kapak resimleri görüntüleme
- Şarkı önizleme dinleme özelliği
- Beğenilen şarkıları kaydetme
- Önerilen şarkılardan playlist oluşturma
- Akıllı şarkı önerileri (benzer şarkıları önerme)

## Gereksinimler

- **Spotify Developer Hesabı**: [Spotify Developer Portal](https://developer.spotify.com/)'a kayıt olmanız gerekmektedir.
- **Spotify API Token**: API'ye bağlanmak için `Access Token` gereklidir. Token almak için OAuth 2.0 yetkilendirme akışı kullanılmalıdır.
- **Python Paketleri**: Gerekli paketleri yüklemek için:

```bash
pip install -r requirements.txt
```

### Spotify Developer Hesabı ve Uygulama Oluşturma

1. [Spotify Developer Portal](https://developer.spotify.com/)'a giriş yapın
2. Dashboard bölümünden "Create an App" seçeneğine tıklayarak yeni bir uygulama oluşturun
3. Oluşturduğunuz uygulamanın sayfasında Client ID ve Client Secret bilgilerini görebilirsiniz

### Spotify API Token Alma

- Spotify API'ye bağlanmak için Access Token almanız gerekir
- Authorization Code Flow veya Client Credentials Flow kullanabilirsiniz
- Authorization Code Flow ile Token Alma:
  1. Kullanıcıdan erişim izni almak için yetkilendirme isteği gönderin
  2. Aldığınız yetkilendirme koduyla Access Token'ı alın
- Client Credentials Flow ile Token Alma:
  - Sadece genel verilere erişim gerektiren projeler için kullanılabilir
  - Uygulama kimlik bilgilerinizi kullanarak doğrudan Access Token alabilirsiniz

### Kullanım

1. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

2. `music suggestion/Spotify.py` dosyasında `SPOTIFY_API_TOKEN` değişkenini aldığınız token ile güncelleyin veya environment variable olarak ayarlayın:
```python
SPOTIFY_API_TOKEN = 'YOUR_SPOTIFY_API_KEY'
```

3. Uygulamayı başlatın:
```python
python music_suggestion/gui.py
```

### Ekran Görüntüleri

![abcd](https://github.com/erent8/music-suggestion/assets/86615310/335db117-39ff-4060-9d62-639d763fe36d)

### Lisans

Bu proje MIT lisansı altında lisanslanmıştır.
