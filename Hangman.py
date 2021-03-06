from Player import Player
from Game import Game


def replace_str_index(text, index=0, replacement=''):
    return '%s%s%s' % (text[:index], replacement, text[index+1:])


def list_duplicates_of(seq, item):
    start = -1
    list_of_indexes = []
    while True:
        try:
            index = seq.index(item, start+1)
        except ValueError:
            break
        else:
            list_of_indexes.append(index)
            start = index
    return list_of_indexes


lengths = ["long", "medium", "short"]
difficulties = ["normal", "hard"]

def main():
    game = Game()
    word_length = input("What length of words? [Long/Medium/Short] ")
    if word_length.lower() not in lengths:
        print("Invalid length")
        return
    difficulty = input("What difficulty would you like to play at? [Normal/Hard] ")
    if difficulty.lower() not in difficulties:
        print("Invalid difficulty")
        return

    player = Player(word_length.lower(), difficulty.lower(), 0)
    secret_word = (''.join(e for e in game.get_random_word(word_length.lower()) if e.isalnum())).lower()
    censored_word = "_ " * len(secret_word)
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    total_letters_found = 0

    while player.mistakes < 8:
        guess = str(input("Guess a letter (Q to quit): "))
        while not guess.isalpha() or len(guess) > 1:
            guess = str(input("Please enter a single letter (Q to quit): "))
        if guess == "Q":
            break
        elif alphabet.count(guess) == 0:
            print("You already tried", guess)
        elif guess in secret_word:
            game.print_hangman(player.mistakes, player.difficulty)
            alphabet = alphabet.replace(guess, '')
            letters_found = secret_word.count(guess)
            total_letters_found += letters_found
            dupIndex = list_duplicates_of(secret_word, guess)
            for i in range(letters_found):
                censored_word = replace_str_index(censored_word, dupIndex[i] * 2, guess)
            print("The word contains", guess)
            print("Remaining letters: ", alphabet.upper())
            print(censored_word)
            if total_letters_found == len(secret_word):
                print("\nYou won!")
                break
        else:
            if player.difficulty == "hard":
                player.mistakes += 2
            else:
                player.mistakes += 1
            game.print_hangman(player.mistakes, player.difficulty)
            print("The word doesn't contain", guess)
            if player.mistakes != 8:
                alphabet = alphabet.replace(guess, '')
                print("Remaining letters: ", alphabet.upper())
                print(censored_word)


    print("\nThe word was", secret_word)


if __name__ == "__main__":
    yes_choices = ["yes", "y", "yea", "yeah", "yessir", "yep", "yup"]
    no_choices = ["no", "n", "nah", "nope", "no ma'am"]
    play = str(input("Ready to play hangman? "))
    while play in yes_choices:
        main()
        play = str(input("Play again? "))
        if play in no_choices:
            print("Goodbye!")
            break
