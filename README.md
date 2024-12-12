# Music Suggestion
![download](https://github.com/user-attachments/assets/84ee6c6a-a3e2-4228-982f-19fb0a4cab9d)
* This project is a Python application that lists recommended songs to the user using Spotify API. It fetches the most popular songs of the users and provides random suggestions.
- [Medium Link](medium.com/@erennt8/spotify-api-ile-müzik-öneri-uygulaması-a5f6a7debf45)
## Requirements

- **Spotify Developer Account**: You need to register to [Spotify Developer Portal ](https://developer.spotify.com/) to access Spotify API.
- **Spotify API Token**: An `Access Token` is required to connect to Spotify API. OAuth 2.0 authorization flow must be used to obtain the token.
- **Python `requests` Library**: You need to install this library which is required to communicate with Spotify API.

```bash
pip install requests
```
### Spotify Developer Account and Application Creation
Create an account by accessing the [Spotify Developer Portal](https://developer.spotify.com/)here.
- After logging in, create a new application by clicking on the Create an App option from the Dashboard section.
- You will be able to see the Client ID and Client Secret information on the page of the application you created.

### Spotify API Token Acquisition
- Get an Access Token to connect to the Spotify API. You can use Spotify's OAuth 2.0 based authorization system for this.
- You can get an Access Token using Authorization Code Flow or Client Credentials Flow.
- Token Acquisition with Authorization Code Flow: First send an authorization request to get access permission from the user. Then get the Access Token with the authorization code you get.

- Token Acquisition with Client Credentials Flow: It can only be used for projects that require access to public data. This flow allows you to get an Access Token directly using your application's credentials.

### Spotify API Endpoint Information
Spotify API endpoints start with /v1. For example, to get the user's most popular songs, you can use the v1/me/top/tracks endpoint.

You can access the Spotify API documentation by reviewing the Spotify API Reference page.
### Usage
SPOTIFY_API_TOKEN must be replaced with a valid Access Token that you received.

### To run the project:

```python
main.py
```
When the code is run, the user will be listed with randomly suggested songs.

### CODE OUTPUT

---------------------------------------------------------------------------------------------------------------

![abcd](https://github.com/erent8/music-suggestion/assets/86615310/335db117-39ff-4060-9d62-639d763fe36d)

----------------------------------------------------------------------------------------------------

### License
This project is licensed under the MIT license
