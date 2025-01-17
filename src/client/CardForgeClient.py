import logging
import os
import requests
from urllib.parse import urljoin
from dotenv import load_dotenv


load_dotenv()


class CardForgeClient:

    def __init__(self) -> None:
        self.api_stem = os.getenv("CARD_FORGE_API_STEM")
        self.logger = logging.getLogger(self.__class__.__name__)
        self.session = requests.Session()
        
    def simulate(self, num_games: int, num_rounds_per_game: int, deck1_name: str, deck2_name: str) -> str:
        url = urljoin(self.api_stem, "simulate")
        params = {
            "numGames": num_games,
            "numRoundsPerGame": num_rounds_per_game,
            "deck1Name": deck1_name,
            "deck2Name": deck2_name
        }
        
        self.logger.info(f"Requesting simulation.")
        try:
            response = self.session.post(url, params=params)
            response.raise_for_status()
            self.logger.info(f"Card forge API response: {response.text}.")
            return response.text
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to request simulation: {e}.")
            raise


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    client = CardForgeClient()
    response = client.simulate(1, 3, "deck-0", "deck-1")
