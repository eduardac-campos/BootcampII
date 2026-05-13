import unittest
from unittest.mock import patch, MagicMock
from punkapi_integration import app, get_beer_data


class TestGetBeerData(unittest.TestCase):

    @patch('punkapi_integration.requests.get')
    def test_get_beer_data_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {
                "id": "madtree-brewing",
                "name": "MadTree Brewing",
                "brewery_type": "regional",
                "city": "Cincinnati",
                "state": "Ohio",
                "country": "United States",
                "website_url": "http://www.madtreebrewing.com",
                "phone": "5138362265"
            }
        ]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = get_beer_data("MadTree")
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'MadTree Brewing')

    @patch('punkapi_integration.requests.get')
    def test_get_beer_data_not_found(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = []
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = get_beer_data("cerveja_inexistente_xyz_123")
        self.assertEqual(result, [])

    @patch('punkapi_integration.requests.get')
    def test_get_beer_data_api_error(self, mock_get):
        import requests
        mock_get.side_effect = requests.exceptions.ConnectionError("API indisponível")

        result = get_beer_data("qualquer_cerveja")
        self.assertIsNone(result)


class TestIndexRoute(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_index_get(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Buscador de Cervejarias', response.data)

    @patch('punkapi_integration.get_beer_data')
    def test_index_post_found(self, mock_get_beer):
        mock_get_beer.return_value = [
            {
                "name": "BrewDog",
                "brewery_type": "regional",
                "city": "Ellon",
                "state": "Scotland",
                "country": "United Kingdom",
                "website_url": "https://www.brewdog.com",
                "phone": "N/A"
            }
        ]
        response = self.client.post('/', data={'beer': 'BrewDog'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'BrewDog', response.data)

    @patch('punkapi_integration.get_beer_data')
    def test_index_post_not_found(self, mock_get_beer):
        mock_get_beer.return_value = []
        response = self.client.post('/', data={'beer': 'cerveja_inexistente'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('não encontrada'.encode('utf-8'), response.data)


if __name__ == '__main__':
    unittest.main()
