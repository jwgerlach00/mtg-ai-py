import logging
import os
import requests
from urllib.parse import urljoin
from dotenv import load_dotenv
import itertools
import random
from typing import Dict

from client.score import Score


load_dotenv()


class CardForgeClient:

    def __init__(self) -> None:
        self.api_stem = os.getenv("CARD_FORGE_API_STEM")
        self.logger = logging.getLogger(self.__class__.__name__)
        self.session = requests.Session()
        random.seed(42)  # Required for reproducibility of the sampler

    def sample_simulate(self, num_games: int, num_rounds_per_game: int, num_decks: int, num_simulations: int) -> Dict[str, int]:
        max_num_samples = num_decks * (num_decks - 1) // 2

        if (num_simulations > max_num_samples):
            raise ValueError(f"Number of samples must be less than or equal to {max_num_samples}.")
        
        # Generate all unique pairs
        deck_names = [f"deck-{i}" for i in range(num_decks)]
        all_pairs = list(itertools.combinations(deck_names, 2))

        score = Score(deck_names)

        # Randomly sample the required number of pairs
        sampled_pairs = random.sample(all_pairs, num_simulations)

        # Simulate games for each pair
        for deck1, deck2 in sampled_pairs:
            result = self.simulate(num_games, num_rounds_per_game, deck1, deck2)

            if (result == deck1):
                score.update(winner=deck1, loser=deck2)
            elif (result == deck2):
                score.update(winner=deck2, loser=deck1)
            else:
                raise ValueError(f"Invalid result: {result}.")
            
        return score.get_scores()

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
