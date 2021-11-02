import unittest
from spotify_api import SpotifyAPI

class TestSpotifyAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client_id = '3818e4e25f4c430c822a0948f79791a7'
        cls.client_secret = '0fb6b42963f7494e9df38e5f56967ad8'
        cls.client = SpotifyAPI(cls.client_id, cls.client_secret)
        cls.client.get_token()

    def test_token(self):
        self.assertTrue(self.client.get_token)

    def test_get_featured_playlist(self):
        # check this creates a list
        self.assertIsInstance(self.client.get_featured_playlist(),list)

        # check this list contains dictionaries
        for playlist_info in self.client.get_featured_playlist():
            self.assertIsInstance(playlist_info, dict)

    def test_get_playlist_details(self):
        # get playlist ids
        for playlist_info in self.client.get_featured_playlist():
            playlist_id = playlist_info['id']

            # check this creates a list
            self.assertIsInstance(self.client.get_playlist_details(playlist_id),list)

            # check this list contains dictionaries
            for track_info in self.client.get_playlist_details(playlist_id):
                self.assertIsInstance(track_info, dict)

    def test_featured_playlist_dict(self):
        # check returns a final dictionary
        self.assertIsInstance(self.client.featured_playlist_dict(),dict)

if __name__ == '__main__':
    unittest.main()
