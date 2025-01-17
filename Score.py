from typing import List, Dict
import copy


class Score:

    def __init__(self, deck_names: List[str]) -> None:
        self.__scores: Dict[str, int] = {}
        for deck_name in deck_names:
            self.__scores[deck_name] = 0

    def __str__(self) -> str:
        return str(self.__scores)

    def update(self, winner: str, loser: str) -> None:
        self.__scores[winner] += 1
        self.__scores[loser] -= 1

    def get_scores(self) -> Dict[str, int]:
        return copy.copy(self.__scores)
