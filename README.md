# music-suggestion

 ### KOD ÇIKTISI
 
 ![abcd](https://github.com/erent8/music-suggestion/assets/86615310/335db117-39ff-4060-9d62-639d763fe36d)



 Spotify API'sini kullanarak kullanıcının en iyi şarkılarını alır ve ardından bu şarkılardan rastgele seçilen birkaçını listeleyen bir Python uygulamasını içerir. İşte kodun adım adım nasıl yazılacağının anlatımı:

İlk adımda, Spotify API'sine erişim için kullanılacak bir token oluşturuyoruz. Bu token'i Spotify Developer Portal'da oluşturabilirsiniz.

fetch_web_api adlı bir fonksiyon oluşturuyoruz. Bu fonksiyon, belirli bir API endpoint'ine istek yapmak için kullanılır. GET veya POST gibi HTTP yöntemlerini kullanabiliriz.

get_top_tracks fonksiyonunu oluşturuyoruz. Bu fonksiyon, kullanıcının en iyi şarkılarını Spotify API'si aracılığıyla alır. limit parametresi ile alınacak şarkı sayısını ayarlayabilirsiniz.

get_random_tracks fonksiyonunu oluşturuyoruz. Bu fonksiyon, kullanıcının en iyi şarkılarını alır ve bu şarkılar arasından belirtilen sayıda rastgele şarkı seçer. Seçilen şarkıları bir liste olarak döndürür.

Son olarak, kullanıcıdan alınan num_tracks değerine göre rastgele önerilen şarkıları listeleyen bir döngü oluşturuyoruz.

Bu kodu çalıştırmadan önce şu adımları izlemeniz gerekecektir:

Spotify Developer Portal'da bir uygulama oluşturun ve API anahtarınızı alın.

token değişkenine Spotify API anahtarınızı ekleyin.

Kodu bir Python dosyasına kaydedin (örneğin, "spotify_music_suggestions.py" olarak kaydedebilirsiniz).

Python'u çalıştırın: python spotify_music_suggestions.py

Bu şekilde, her çalıştırdığınızda belirlediğiniz sayıda rastgele şarkı önerisi alacaksınız.
