import logging

from client import DeckGeneratorClient, CardForgeClient
from config import NUM_DECKS, MIN_NUM_COLORS, MAX_NUM_COLORS, NUM_GAMES, NUM_ROUNDS_PER_GAME


def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Generate decks
    deckGeneratorClient = DeckGeneratorClient()
    deckGeneratorResponse = deckGeneratorClient.generate(NUM_DECKS, MIN_NUM_COLORS, MAX_NUM_COLORS)

    # Simulate games
    cardForgeClient = CardForgeClient()
    cardForgeResponse = cardForgeClient.simulate(NUM_GAMES, NUM_ROUNDS_PER_GAME, f"deck-0", f"deck-1")
    logger.info(f"Deck generator response: {deckGeneratorResponse}")
    logger.info(f"Card forge response: {cardForgeResponse}")


if __name__ == "__main__":
    main()
