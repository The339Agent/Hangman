import json
import random


def read_json_file(filepath):
    """
    Read a file in the JSON format and parse it to a variable.
    :param filepath: The path to the JSON file to parse
    :return: A variable containing all the elements of the JSON file. If parsing failes, the exception is returned
    """
    try:
        return json.loads(open(filepath).read())
    except Exception as e:
        print(f"Exception in decoding JSON file: {e}")
        return e


def choose_rand(elements):
    """
    Selects a random element from a given array.
    :param elements: Array of elements to choose from
    :return: A random element from the array
    """
    return elements[random.randint(0, len(elements) - 1)]


def get_int(prompt, separator=": "):
    """
    Prompts the user with the given prompt, and returns the int the user enters. Returns false if the user doesn't enter an int.
    :param prompt: The prompt to give the user for the int.
    :param separator: The separator do use between the prompt and user feedback.
    :return: The int the user entered, or False if the user didn't enter an int.
    """
    try:
        return int(input(prompt + separator))
    except Exception as e:
        return False


def will_play():
    """
    If the user wants to play a game of hangman.
    :return: True if the user wants to play, false if not.
    """
    first = True
    while True:
        res = input("Play a new game of hangman? (Y)").upper()
        if not res:
            res = "Y"

        if res == "Y" or res == "YES" or first:
            first = False
            yield True

        yield False


def find_nth(haystack, needle, n):
    parts = haystack.split(needle, n+1)
    if len(parts) <= n+1:
        return -1
    return len(haystack)-len(parts[-1])-len(needle)


if __name__ == '__main__':
    word_list = read_json_file(
        r"vendor\dwyl\english-words\words_dictionary.json")
    # word_list = read_json_file(r"vendor\engineer-man\names\name-list.json")

    while will_play():
        """
        Container game loop. While the user wants to play the game, this loop loops.
        """
        guessed_letters = []
        correct_letters = []
        attempts = 0

        get_result = get_int(
            "How many guesses do you want? Please choose an integer")
        max_attempts = get_result if get_result != False else 10

        get_result = get_int(
            "How long can the word be? Please choose a max integer above 0")
        max_length = get_result if get_result != False else 1000
        while max_length <= 0:
            get_result = get_int(
                "How long can the word be? Please choose a max integer above 0")
            max_length = get_result if get_result != False else 1000

        last_guessed = ""

        word = choose_rand(word_list).upper()
        while len(word) > max_length:
            word = choose_rand(word_list).upper()

        print(f"The word is a {len(word)} letter word.")
        while True:
            """
            Main game loop. Game logic for each round is handled here.
            """
            last_guessed = input(
                "\nGuess a letter or the word you think it is: ").upper()
            if not last_guessed:
                print("You need to guess something.")
                continue

            attempts += 1

            if last_guessed == word:
                print(
                    f"Correct! The word is {word}! You took {attempts} attempts to guess it!")
                break

            if len(last_guessed) <= 1:
                if guessed_letters.__contains__(last_guessed[0]):
                    print("You have already guessed this letter.")
                    attempts -= 1
                    continue

                guessed_letters.append(last_guessed[0])
                if word.__contains__(last_guessed[0]):
                    print(f"The letter {last_guessed[0]} was in the word!")
                    for i in range(word.count(last_guessed[0])):
                        print(i, find_nth(word, last_guessed[0], i))
                        correct_letters.insert(
                            find_nth(word, last_guessed[0], i) - 1,
                            last_guessed[0])
                else:
                    print(f"The letter {last_guessed[0]} is not in the word.")

                print(f"Correct guesses so far: {', '.join(correct_letters)}")

            else:
                print(f"The word is not {last_guessed}.")
                print(f"Correct guesses so far: {', '.join(correct_letters)}")

            if attempts > max_attempts:
                print(
                    f"You used up all of your tries. The word was {word}. Better luck next time!")
                break
