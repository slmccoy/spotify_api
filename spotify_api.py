import base64
import requests
import datetime

class SpotifyAPI:
    client_id = None
    client_secret = None
    access_token = None

    token_url = 'https://accounts.spotify.com/api/token'
    base_url = 'https://api.spotify.com/v1/'

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def client_creds(self):
        client_id = self.client_id
        client_secret = self.client_secret

        if client_id == None or client_secret == None:
            raise Exception('You must set client_id and client_secret')

        client_creds = f'{client_id}:{client_secret}'
        client_creds_uft8 = client_creds.encode()
        client_creds_b64 = base64.b64encode(client_creds_uft8)
        return client_creds_b64.decode()

    def token_data(self):
        return {
            'grant_type':'client_credentials'
        }

    def token_header(self):
        client_creds = self.client_creds()
        return {
            'Authorization': f'Basic {client_creds}'
        }

    def get_token(self):
        token_url = self.token_url
        token_data = self.token_data()
        token_header = self.token_header()

        response = requests.post(token_url, data = token_data, headers = token_header)

        if response.status_code not in range(200,299):
            return False

        token_data = response.json()
        access_token = token_data['access_token']

        self.access_token = access_token

        return True

    '''
    Get Data
    '''

    def headers(self):
        access_token = self.access_token

        return {
            'Authorization': f'Bearer {access_token}'
        }

    def get_featured_playlist(self):
        base_url = self.base_url
        headers = self.headers()

        featured_playlists_endpoint = 'browse/featured-playlists/?limit=50'
        featured_playlists_url = f'{base_url}{featured_playlists_endpoint}'

        response = requests.get(featured_playlists_url,headers=headers)

        #Should return a list of dictionaries - one for each playlist
        return response.json()['playlists']['items']

    def get_playlist_details(self, playlist_id):
        base_url = self.base_url
        headers = self.headers()

        playlist_url_endpoint = f'playlists/{playlist_id}/tracks'
        playlist_url = f'{base_url}{playlist_url_endpoint}'

        playlist_response = requests.get(playlist_url, headers=headers)

        #Should return a list of dictionaries - one for each track
        return playlist_response.json()['items']

    def extract_track_details(self, track_info):

        track = track_info['track']

        track_name = track['name']

        artists = track['artists']
        artist_list = []
        for artist in artists:
            artist_name = artist['name']
            artist_list.append(artist_name)

        return (track_name,artist_list)

    def featured_playlist_dict(self):
        featured_playlists = {}
        featured_playlists_list = self.get_featured_playlist()

        for playlist_info in featured_playlists_list:

            playlist_id = playlist_info['id']
            playlist_name = playlist_info['name']

            if playlist_id in featured_playlists.keys():
                continue

            featured_playlists[playlist_id] = {
                'name':playlist_name,
                'tracks': []
            }

            track_list = self.get_playlist_details(playlist_id)

            for track_info in track_list:
                track_name, artist_list = self.extract_track_details(track_info)
                featured_playlists[playlist_id]['tracks'].append((track_name,artist_list))

        return featured_playlists

#for checking
client_id = '3818e4e25f4c430c822a0948f79791a7'
client_secret = '0fb6b42963f7494e9df38e5f56967ad8'

client = SpotifyAPI(client_id, client_secret)
client.get_token()
playlists = client.featured_playlist_dict()
print(isinstance(playlists,dict))
