import unittest
from unittest.mock import patch, MagicMock
from punkapi_integration import app, get_beer_data, buscar_brasileira


class TestBuscarBrasileira(unittest.TestCase):

    def test_encontra_brahma(self):
        result = buscar_brasileira("Brahma")
        self.assertIsNotNone(result)
        self.assertEqual(result['name'], 'Brahma')
        self.assertEqual(result['country'], 'Brasil')

    def test_encontra_colorado(self):
        result = buscar_brasileira("Colorado")
        self.assertIsNotNone(result)
        self.assertIn('Colorado', result['name'])

    def test_busca_case_insensitive(self):
        result = buscar_brasileira("eisenbahn")
        self.assertIsNotNone(result)
        self.assertEqual(result['name'], 'Eisenbahn')

    def test_nao_encontra_inexistente(self):
        result = buscar_brasileira("cerveja_xyz_inexistente")
        self.assertIsNone(result)


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
        self.assertEqual(result[0]['name'], 'MadTree Brewing')

    @patch('punkapi_integration.requests.get')
    def test_get_beer_data_not_found(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = []
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = get_beer_data("cerveja_inexistente_xyz")
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
        self.assertIn('Buscador de Cervejarias'.encode('utf-8'), response.data)

    def test_index_post_cervejaria_brasileira(self):
        response = self.client.post('/', data={'beer': 'Brahma'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Brahma'.encode('utf-8'), response.data)
        self.assertIn('Brasil'.encode('utf-8'), response.data)

    def test_index_post_cervejaria_brasileira_colorado(self):
        response = self.client.post('/', data={'beer': 'Colorado'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Colorado'.encode('utf-8'), response.data)
        self.assertIn('Brasil'.encode('utf-8'), response.data)

    @patch('punkapi_integration.get_beer_data')
    def test_index_post_internacional(self, mock_get_beer):
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
        response = self.client.post('/', data={'beer': 'cerveja_xyz_inexistente'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('não encontrada'.encode('utf-8'), response.data)


if __name__ == '__main__':
    unittest.main()
