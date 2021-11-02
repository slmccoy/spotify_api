import base64
import requests
import datetime

class ClientToken:
    client_id = None
    client_secret = None
    access_token = None

    token_url = 'https://accounts.spotify.com/api/token'

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

# for checking
client_id = '3818e4e25f4c430c822a0948f79791a7'
client_secret = '0fb6b42963f7494e9df38e5f56967ad8'

client = ClientToken(client_id, client_secret)
client.get_token()
