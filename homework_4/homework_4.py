from typing import Generator, List, Set

class Player:
    def __init__(self, first_name: str, last_name: str):
        self.first_name: str = first_name
        self.last_name: str = last_name

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

team: list[Player] = [
    Player("John", "Smith"),
    Player("Marry", "Smith"),
    Player("Jack", "Hill"),
    Player("Nick", "Doe"),
    Player("John", "Doe"),
    Player("Marry", "Doe"),
]

def dedup(collection: List[Player]) -> Generator[str, None, None]:
    seen_first_names: Set[str] = set()
    for player in collection:
        if player.first_name not in seen_first_names:
            seen_first_names.add(player.first_name)
            yield str(player)

for player in dedup(team):
    print(player)
