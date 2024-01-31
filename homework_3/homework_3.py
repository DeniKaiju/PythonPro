from typing import TextIO

def search_in_file(file: TextIO, search_string: str) -> int:
    total = 0

    for line in file:
        if search_string.lower() in line.lower():
            total += 1

    return total

def main():
    file_path = 'C:\\Users\\Yarik\\Desktop\\rockyou.txt'
    search_string = input("Enter the string to search for: ")

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        matches = search_in_file(file, search_string)

    print(f"Number of matches found: {matches}")

if __name__ == "__main__":
    main()
