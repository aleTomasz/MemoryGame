import random
import string
import time

import termcolor

from configuration import LEVELS
import os

emoji = True
emoji_chars = ['\U0001F427', "\U0001F43C", "\U0001F428", "\U0001F42D", "\U0001F418", "\U0001F42B", "\U0001F42E",
               "\U0001F436", "\U0001F42C", "\U0001F420", "\U0001F419", "\U0001F40C", "\U0001F41B", "\U0001F41E",
               "\U0001F33B", "\U0001F335", "\U0001F34D", "\U0001F356", "\U0001F359", "\U0001F369", "\U0001F378",
               "\U0001F37A", "\U0001F3E0", "\U0001F525", "\U0001F383", "\U0001F624"]

letter_to_emoji_mapping = dict(zip(string.ascii_uppercase, emoji_chars))

game = {
    'level': None,
    'masking_char': '()',
    'round_counter': 0,
    'board': None,
}

def console_clear():
    os.system('cls' if os.name == 'nt' else 'clear')


# def generate_empty_board():
def get_level_from_user():
    console_clear()
    print(f'Select level')
    for level in LEVELS:
        print(f"{level['key']}: {level['name']}")

    level_keys = [level['key'] for level in LEVELS]

    while True:
        user_level = input('Enter level key: ')
        if user_level.isnumeric() and int(user_level) in level_keys:
            break
        else:
            print(f'Invalid level try again')

    return [level for level in LEVELS if level['key'] == int(user_level)][0]


def get_random_letter(size):
    letters = random.sample(string.ascii_uppercase, size // 2) * 2
    random.shuffle(letters)
    return letters


def generate_board(level):
    # losowanie literek
    # literki musza byc parzyste (ABC) -> (ABCABC) -> (CABABC)
    # wysokosc / szerokosc
    # komroka trzyma konfigureacje (literka, widocznosc, widocznosc w rudzie)
    width = level['width']
    size = width * level['height']
    letters = get_random_letter(size)

    letter_board = [letters[index: index + width] for index in range(0, len(letters), width)]
    return [[{'visibility': False, 'round_visibility': False, 'letter': cell} for cell in row] for row in letter_board]

    # letter
    # visibility=False
    # round_visibility=False

    # 5x10 # skip = width = 5
    # letters[0:5]
    # letters[5:10]
    # letters[10:15]
    # letters[15:20]
    pass


def print_board(board, level):
    print(termcolor.colored("    " + "   ".join(string.ascii_uppercase[0: len(board[0])]), level['color']))
    for row_no, row in enumerate(board, 1):
        print(termcolor.colored(str(row_no), level['color']) + " ", end="  ")
        for cell in row:
            graphical_representation = letter_to_emoji_mapping[cell['letter']] if emoji else cell['letter']
            if cell['visibility']:
                print(graphical_representation + " ", end='  ')
                # print(letter_to_emoji_mapping[cell['letter']] if emoji else cell['letter'] + " ", end='  ')
            elif cell['round_visibility']:
                print(termcolor.colored(graphical_representation + " ", 'yellow'), end='  ')
                # print(letter_to_emoji_mapping[cell['letter']] if emoji else colored(cell['letter'] + " ", 'yellow'), end='  ')
            else:
                # print(game['masking_char'], end='  ')
                print(game['masking_char'], end='  ')
        print()


def get_field_position(board_height, board_width, counter):
    while True:
        raw_input = input(f"Gimme coord for round {counter}: ")
        if len(raw_input) in [2, 3] and (
                raw_input[0].upper() in string.ascii_uppercase[0:board_width] and raw_input[1:2].isnumeric() and int(
                raw_input[1:2]) <= board_height):
            break
        print("Incorrect input - try again!")

    return int(raw_input[1:2]) - 1, string.ascii_uppercase.index(raw_input[0].upper())


if __name__ == '__main__':
    level = game['level'] = get_level_from_user()
    board = game['board'] = generate_board(level)
    # print_board(board, level)

    # A1 -> [0,0]
    while True:
        game['round_counter'] += 1

        console_clear()
        print_board(board, level)
        first_coordinate = get_field_position(level['height'], level['width'], game['round_counter'])
        board[first_coordinate[0]][first_coordinate[1]]['round_visibility'] = True
        console_clear()
        print_board(board, level)

        second_coordinate = get_field_position(level['height'], level['width'], game['round_counter'])
        board[second_coordinate[0]][second_coordinate[1]]['round_visibility'] = True
        console_clear()
        print_board(board, level)

        letter_first_cord = board[first_coordinate[0]][first_coordinate[1]]['letter']
        letter_second_cord = letter_first_cord == board[second_coordinate[0]][second_coordinate[1]]['letter']

        if letter_second_cord == letter_first_cord:
            board[first_coordinate[0]][first_coordinate[1]]['visibility'] = True
            board[second_coordinate[0]][second_coordinate[1]]['visibility'] = True
        else:
            board[first_coordinate[0]][first_coordinate[1]]['round_visibility'] = False
            board[second_coordinate[0]][second_coordinate[1]]['round_visibility'] = False

        is_game_finished = True
        for row in board:
            for cell in row:
                if not cell['visibility']:
                    is_game_finished = False
                    break
            if is_game_finished:
                break

        if is_game_finished:
            print("WON!")

        input("Press enter to continue...")

        print(first_coordinate)
        # input -> pierwsza kordynata
        # console clear
        # print baard z okdkrytm polem
        # input -> druga koordynata
        # print -> dwa odkryte pola
        # czy literki sa takie same
        #   nie -> zakrywamy pola
        #   tak -> zostawiamy odkryte
        pass

    print("")
