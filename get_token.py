import base64
import requests
import datetime

# client info from developer.spotify.com
client_id = '3818e4e25f4c430c822a0948f79791a7'
client_secret = '0fb6b42963f7494e9df38e5f56967ad8'

# create credentials string in base64
client_creds = f'{client_id}:{client_secret}'
client_creds_uft8 = client_creds.encode() # required for base64 encoding
client_creds_b64 = base64.b64encode(client_creds_uft8) # api requires base64
client_creds_b64_str = client_creds_b64.decode() # api requires string

# Required - set to: client_credentials
token_data = {
    'grant_type':'client_credentials'
}

# Basic <base64 encoded client_id:client_secret>
token_header = {
    'Authorization': f'Basic {client_creds_b64_str}'
}

# POST to:
token_url = 'https://accounts.spotify.com/api/token'

# create POST request
r = requests.post(token_url, data = token_data, headers = token_header)

# check if request was valid
valid_request = r.status_code in range(200,299)

# if valid - convert to json and extract required values from dictionary
if valid_request:
    token_data = r.json()

    access_token = token_data['access_token']
    #expires_in = token_data['expires_in']

print(token_data)
