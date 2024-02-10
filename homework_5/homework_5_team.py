from typing import Dict, Any

team: Dict[int, Dict[str, Any]] = {
    1: {"name": "John", "age": 20},
    5: {"name": "Alex", "age": 21},
    7: {"name": "Mattew", "age": 18},
    13: {"name": "Conor", "age": 19}
}


def repr_players(team: Dict[int, Dict[str, Any]]):
    for number, player in team.items():
        print(f"Player number: {number}, "
              f"Name: {player['name']}, "
              f"Age: {player['age']}")


def add_player(name: str, age: int, number: int):
    if number in team:
        print("Player number already exists. "
              "Please choose a different number.")
    else:
        team[number] = {"name": name, "age": age}
        print(f"Player {name} added successfully.")


def del_player(number: int):
    if number not in team:
        print("Player number does not exist.")
    else:
        del team[number]
        print(f"Player with number {number} deleted successfully.")


def update_player(name: str, age: int, number: int):
    if number not in team:
        print("Player number does not exist.")
    else:
        team[number] = {"name": name, "age": age}
        print(f"Player with number {number} updated successfully.")


def main():
    repr_players(team)
    operations = ("add", "del", "repr", "update", "exit")

    while True:
        operation = input("Please enter the operation: ")
        if operation not in operations:
            print(f"Operation '{operation}' is not available\n")
            continue

        if operation == "repr":
            repr_players(team)
        elif operation == "add":
            user_data = input(
                "Enter new player information [name, age, number]: "
            )
            name, age, number = user_data.split(",")
            try:
                add_player(name=name, age=int(age), number=int(number))
            except ValueError:
                print("Age and number of player must be integers")
        elif operation == "del":
            number = int(input("Enter the player number you want to delete: "))
            del_player(number)
        elif operation == "update":
            user_data = input(
                "Enter player information to update [name, age, number]: "
            )
            name, age, number = user_data.split(",")
            try:
                update_player(name=name, age=int(age), number=int(number))
            except ValueError:
                print("Age and number of player must be integers")
        elif operation == "exit":
            break


if __name__ == "__main__":
    main()
