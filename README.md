# Music Suggestion
![download](https://github.com/user-attachments/assets/84ee6c6a-a3e2-4228-982f-19fb0a4cab9d)


Bu proje, Spotify API'yi kullanarak kullanıcıya önerilen şarkıları listeleyen bir Python uygulamasıdır. Kullanıcıların en popüler şarkılarını getirir ve rastgele öneriler sunar.

## Gereksinimler

- **Spotify Developer Hesabı**: Spotify API’ye erişim için [Spotify Developer Portal'a ](https://developer.spotify.com/) kaydolmanız gerekmektedir.
- **Spotify API Token**: Spotify API’ye bağlanabilmek için bir `Access Token` gereklidir. Token almak için OAuth 2.0 yetkilendirme akışı kullanılmalıdır.
- **Python `requests` Kütüphanesi**: Spotify API ile iletişim kurmak için gerekli olan bu kütüphaneyi yüklemelisiniz.
  
  ```bash
  pip install requests

### Spotify Developer Hesabı ve Uygulama Oluşturma
[Spotify Developer Portal'a ](https://developer.spotify.com/)buradan ulaşarak bir hesap oluşturun.
- Giriş yaptıktan sonra, Dashboard bölümünden Create an App seçeneğine tıklayarak yeni bir uygulama oluşturun.
- Oluşturduğunuz uygulamanın sayfasında Client ID ve Client Secret bilgilerini görebileceksiniz.
### Spotify API Token Alımı
- Spotify API’ye bağlanmak için bir Access Token alın. Bunun için Spotify’ın OAuth 2.0 tabanlı yetkilendirme sistemini kullanabilirsiniz.
- Authorization Code Flow veya Client Credentials Flow kullanarak bir Access Token elde edebilirsiniz.
- Authorization Code Flow ile Token Alımı: Kullanıcıdan erişim izni almak için öncelikle bir yetkilendirme isteği gönderin. Daha sonra elde ettiğiniz authorization code ile Access Token alın.

- Client Credentials Flow ile Token Alımı: Sadece genel verilere erişim gerektiren projeler için kullanılabilir. Bu akış, uygulamanızın kimlik bilgilerini kullanarak direkt bir Access Token almanızı sağlar.

### Spotify API Endpoint Bilgileri
Spotify API endpoint’leri /v1 ile başlar. Örneğin, kullanıcının en popüler şarkılarını almak için v1/me/top/tracks endpoint'ini kullanabilirsiniz.
Spotify API dökümantasyonuna erişmek için Spotify API Reference sayfasını inceleyebilirsiniz.
### Kullanım
SPOTIFY_API_TOKEN değeri, aldığınız geçerli bir Access Token ile değiştirilmelidir.

### Projeyi çalıştırmak için:

```python
Spotify.py
```
Kod çalıştırıldığında, kullanıcıya rastgele önerilen şarkılar listelenecektir.

 ### KOD ÇIKTISI

 ---------------------------------------------------------------------------------------------------------------

 
 ![abcd](https://github.com/erent8/music-suggestion/assets/86615310/335db117-39ff-4060-9d62-639d763fe36d)

 
-----------------------------------------------------------------------------------------------------------------

### Lisans
Bu proje MIT lisansı altında lisanslanmıştır





 
