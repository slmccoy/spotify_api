from client_token import ClientToken
import requests
from urllib.parse import urlencode

client_id = '3818e4e25f4c430c822a0948f79791a7'
client_secret = '0fb6b42963f7494e9df38e5f56967ad8'

client = ClientToken(client_id, client_secret)
client.get_token()
access_token = client.access_token


base_url = 'https://api.spotify.com/v1/'

# Authorization - Bearer <Access Token>
headers = {
    'Authorization': f'Bearer {access_token}'
}

# consider featured playlists
featured_playlists_endpoint = 'browse/featured-playlists/?limit=50'
featured_playlists_url = f'{base_url}{featured_playlists_endpoint}'

# note: max 50 per request as above in url
response = requests.get(featured_playlists_url,headers=headers)

playlists = response.json()['playlists']['items']

# Keys in each playlist dictionary:
# ['collaborative', 'description', 'external_urls', 'href', 'id', 'images', 'name', 'owner', 'primary_color', 'public', 'snapshot_id', 'tracks', 'type', 'uri']

# Get playlist ids
featured_playlist_dict = {}

for playlist in playlists:
    playlist_id = playlist['id']
    playlist_name = playlist['name']

    if playlist_id in featured_playlist_dict.keys():
        continue

    playlist_dict = {}
    playlist_dict['name'] = playlist_name
    playlist_dict['tracks'] = {}
    featured_playlist_dict[playlist_id] = playlist_dict


    # Get tracks for each playlist
    playlist_url_endpoint = f'playlists/{playlist_id}/tracks'
    playlist_url = f'{base_url}{playlist_url_endpoint}'
    playlist_response = requests.get(playlist_url, headers=headers)
    playlist_data = playlist_response.json()['items']


    for track_data in playlist_data:
        track = track_data['track']

        # keys in track:
        #['album', 'artists', 'available_markets', 'disc_number', 'duration_ms', #'episode', 'explicit', 'external_ids', 'external_urls', 'href', 'id', 'is_local', #'name', 'popularity', 'preview_url', 'track', 'track_number', 'type', 'uri']

        track_name = track['name']

        featured_playlist_dict[playlist_id]['tracks'][track_name] = []

        artists = track['artists']
        for artist in artists:

            #keys in artist:
            # ['external_urls', 'href', 'id', 'name', 'type', 'uri']

            artist_name = artist['name']

            featured_playlist_dict[playlist_id]['tracks'][track_name].append(artist_name)

#print(featured_playlist_dict)
