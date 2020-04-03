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
    parts= haystack.split(needle, n+1)
    if len(parts)<=n+1:
        return -1
    return len(haystack)-len(parts[-1])-len(needle)


if __name__ == '__main__':
    word_list = read_json_file(r"vendor\dwyl\english-words\words_dictionary.json")
    # word_list = read_json_file(r"vendor\engineer-man\names\name-list.json")

    while will_play():
        """
        Container game loop. While the user wants to play the game, this loop loops.
        """
        word = choose_rand(word_list)
        word = word.upper()
        guessed_letters = []
        correct_letters = []
        attempts = 0
        try:
            max_attempts = int(input("How many guesses do you want? Please choose an integer: "))
        except Exception as e:
            print("You cannot choose this number because it is not an integer. Defaulted to 10.")
            max_attempts = 10
        last_guessed = ""

        print(f"The word is a {len(word)} letter word.")
        while True:
            """
            Main game loop. Game logic for each round is handled here.
            """
            last_guessed = input("\nGuess a letter or the word you think it is: ").upper()
            if not last_guessed:
                print("You need to guess something.")
                continue

            attempts += 1

            if last_guessed == word:
                print(f"Correct! The word is {word}! You took {attempts} attempts to guess it!")
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
                        correct_letters.insert(find_nth(word, last_guessed[0], i), last_guessed[0])
                else:
                    print(f"The letter {last_guessed[0]} is not in the word.")

                print(f"Correct guesses so far: {', '.join(correct_letters)}")

            else:
                print(f"The word is not {last_guessed}.")
                print(f"Correct guesses so far: {', '.join(correct_letters)}")

            if attempts > max_attempts:
                print(f"You used up all of your tries. The word was {word}. Better luck next time!")
                break
