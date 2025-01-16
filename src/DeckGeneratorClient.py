import logging
import os
import requests
from urllib.parse import urljoin
from typing import Any, Dict
from dotenv import load_dotenv


load_dotenv()


class DeckGeneratorClient:
    """
    A client to interact with the Deck Generator API.
    """

    def __init__(self):
        """
        Initialize the DeckGeneratorClient.

        :param api_stem: The base URL of the API.
        """
        self.api_stem = os.getenv("API_STEM")
        self.logger = logging.getLogger(self.__class__.__name__)
        self.session = requests.Session()

    def generate(self, num_decks: int, min_num_colors: int, max_num_colors: int) -> Dict[str, Any]:
        """
        Generate decks with the specified parameters.

        :param num_decks: Number of decks to generate.
        :param min_num_colors: Minimum number of colors per deck.
        :param max_num_colors: Maximum number of colors per deck.
        :return: The response from the API as a dictionary.
        """
        url = urljoin(self.api_stem, "generateDecks")
        params = {
            "numDecks": num_decks,
            "minNumColors": min_num_colors,
            "maxNumColors": max_num_colors
        }

        self.logger.info(f"Requesting {num_decks} decks with {min_num_colors} to {max_num_colors} colors.")
        try:
            response = self.session.post(url, params=params)
            response.raise_for_status()
            self.logger.info(f"Deck generator API response: {response.text}")
            return response.text
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to request decks: {e}.")
            raise


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    client = DeckGeneratorClient()
    response = client.generate(2, 2, 3)
    print(response)
