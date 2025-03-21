import os
import random
import string
import time

import termcolor
from termcolor import colored

emoji = True
simulation = True

emoji_chars = ['\U0001F427', "\U0001F43C", "\U0001F428", "\U0001F42D", "\U0001F418", "\U0001F42B", "\U0001F42E",
               "\U0001F436", "\U0001F42C", "\U0001F420", "\U0001F419", "\U0001F40C", "\U0001F41B", "\U0001F41E",
               "\U0001F33B", "\U0001F335", "\U0001F34D", "\U0001F356", "\U0001F359", "\U0001F369", "\U0001F378",
               "\U0001F37A", "\U0001F3E0", "\U0001F525", "\U0001F383", "\U0001F624"]

letter_to_emoji_mapping = dict(zip(string.ascii_uppercase, emoji_chars))

levels = [
    {
        "name": "Easy",
        "height": 5,
        "width": 4,
        "color": "green",
        "key": 1
    },
    {
        "name": "Medium",
        "height": 5,
        "width": 6,
        "color": "magenta",
        "key": 2
    },
    {
        "name": "Hard",
        "height": 5,
        "width": 10,
        "color": "red",
        "key": 3
    }]

game = {
    "level": None,
    "game_state": None,
    'masking_char': "()" if emoji else "# ",
    "steps": 0
}


# clears the screen
def console_clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def generate_board(height, width):
    number_of_letters = height * width
    if number_of_letters % 2 != 0:
        raise ValueError

    chosen_letters = random.sample(list(string.ascii_uppercase), number_of_letters // 2) * 2
    random.shuffle(chosen_letters)

    return [chosen_letters[index:index + height] for index in range(0, len(chosen_letters), height)]


def transform_to_game_state_board(board):
    return [[{"hidden": True, "temporary_visible": False, "letter": cell} for cell in row] for row in board]


def print_board(board):
    print(termcolor.colored("    " + "   ".join(string.ascii_uppercase[0: len(board[0])]), game['level']['color']))
    for row_no, row in enumerate(board, 1):
        print(termcolor.colored(str(row_no), game['level']['color']) + " ", end="  ")
        for cell in row:
            if not cell['hidden']:
                print(letter_to_emoji_mapping[cell['letter']] if emoji else cell['letter'] + " ", end='  ')
            elif cell['temporary_visible']:
                print(letter_to_emoji_mapping[cell['letter']] if emoji else colored(cell['letter'] + " ", 'yellow'),
                      end='  ')
            else:
                print(game['masking_char'], end='  ')
        print()


def get_user_input(board_height, board_width):
    while True:
        raw_input = input("Gimme cords: ")
        if all(
                [len(raw_input) in [2, 3],
                 (raw_input[0].upper() in string.ascii_uppercase[0:board_width + 1]),
                 (raw_input[1:2].isnumeric()),
                 int(raw_input[1:2]) <= board_height
                 ]):
            break
        print("Incorrect input, try again!")

    return int(raw_input[1]) - 1, string.ascii_uppercase.index(raw_input[0].upper())


def simulated_user_input():
    board = game['board']

    hidden_fields = []
    for row_index, row in enumerate(board):
        for column_index, cell in enumerate(row):
            if cell['hidden'] and not cell['temporary_visible']:
                hidden_fields.append((row_index, column_index))

    return random.choice(hidden_fields)


def get_level_from_user():
    console_clear()
    print("Choose difficulty level!")

    for level in levels:
        print(f"{level['key']}: {level['name']}")

    while True:
        selected_level = input("How brave are you? ")
        if selected_level.isnumeric() \
                and int(selected_level) in [level['key'] for level in levels]:
            break
        console_clear()
        print("Incorrect level, try again")

    return [level for level in levels if level['key'] == int(selected_level)][0]


if __name__ == "__main__":
    print("Welcome to Memory Game!")
    game['level'] = get_level_from_user()
    letter_board = generate_board(game['level']['height'], game['level']['width'])
    game['board'] = transform_to_game_state_board(letter_board)
    g = game['board']
    console_clear()
    print_board(game['board'])

    while True:
        game['steps'] += 1

        first_coordinates = simulated_user_input() if simulation else get_user_input(game['level']['height'],
                                                                                     game['level']['width'])
        first_cell = game['board'][first_coordinates[0]][first_coordinates[1]]
        first_cell['temporary_visible'] = True
        fist_char = first_cell['letter']

        console_clear()
        print_board(game['board'])

        second_coordinates = simulated_user_input() if simulation else get_user_input(game['level']['height'],
                                                                                      game['level']['width'])
        second_cell = game['board'][second_coordinates[0]][second_coordinates[1]]
        second_cell['temporary_visible'] = True
        second_char = second_cell['letter']

        console_clear()
        print_board(game['board'])

        if not simulation:
            time.sleep(1)

        if fist_char == second_char and first_coordinates != second_coordinates:
            first_cell['hidden'] = False
            second_cell['hidden'] = False

        first_cell['temporary_visible'] = False
        second_cell['temporary_visible'] = False

        if simulation:
            time.sleep(0.1)

        console_clear()
        print_board(game['board'])

        if fist_char == second_char:
            print("BRAWO! MATCH!")

        if all([not cell['hidden'] for row in game['board'] for cell in row]):
            print(f"WON! Finished in {game['steps']} steps")
            break
