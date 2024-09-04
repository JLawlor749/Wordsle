from urllib.request import urlopen
import urllib.error
import re
import time

wordnik_file = open("WordnikAPI.env", "r")

wordnik_key = wordnik_file.read()

def get_word(link_address:str):
    """
    This function retrieves a word from the Wordnik API based on the URL provided.
    It returns a tuple containing the word, and its length.
    """

    wordnik_response = 0

    while wordnik_response == 0:
        try:
            wordnik_response = urlopen(link_address)
        except:
            print("\nAn error has occured. Please wait...\n")
            time.sleep(12)

    #Uncomment to get response header information on word requests.
    #print(wordnik_response.info())

    #urllib.error.HTTPError: HTTP Error 429: Too Many Requests

    wordnik_response = wordnik_response.read()

    wordnik_response = wordnik_response.decode("utf-8")

    wordnik_response = re.sub("{\"word\":\"", "", wordnik_response)

    wordnik_response = re.sub("\",\"id\":0}", "", wordnik_response)

    wordnik_response = wordnik_response.upper()

    word_tuple = (wordnik_response, len(wordnik_response))

    return word_tuple


def check_word(word:str, target_word:tuple[str, int]):
    """
    This function checks each letter in the guessed word against the target.
    It prints each letter of the guess in a different colour based on correctness.
    \nGREEN = Correct letter in the correct space.
    \nYELLOW = Correct letter in the wrong space.
    \nRED = Wrong letter.
    """

    goal_checklist = []
    guess_print = []
                    
    for el in target_word[0]:
        goal_checklist.append(el)

    for i in range (0, target_word[1]):
        if word[i] == (target_word[0])[i]:
            guess_print.append(("\033[1;32;40m", i))
            goal_checklist.remove(word[i])

    for i in range (0, target_word[1]):
        if word[i] in goal_checklist and word[i] != (target_word[0])[i] and word[i] != (target_word[0])[i]:
            guess_print.append(("\033[1;33;40m", i))
            goal_checklist.remove(word[i])

    for i in range (0, target_word[1]):
        if word[i] not in goal_checklist and ("\033[1;33;40m", i) not in guess_print and ("\033[1;32;40m", i) not in guess_print:
            guess_print.append(("\033[1;31;40m", i))

    guess_print.sort(key=lambda tup:tup[1])

    for el in guess_print:
        print(el[0] + word[el[1]], end="")

    print("\033[0;37;40m")
    print("")



exit_game = False

print("\n        ~ Welcome to Wordsle! ~")
print("------------------------------------------")

while exit_game == False:
    print("\nMain Menu:")
    print("1. Start Game")
    print("2. Instructions")
    print("3. Quit\n")

    selection = input()
    print("")

    match selection:
        case "1":

            print("Please input the length of the word you want to guess:")
            desired_length = int(input())
            print("")
            
            wordnik_url = "http://api.wordnik.com/v4/words.json/randomWord?minCorpusCount=20&minLength=" + str(desired_length) + "&maxLength=" + str(desired_length) + "&api_key=" + wordnik_key
            puzzle_goal = get_word(wordnik_url)
            
            print("Input your guesses below:")

            lost = False
            won = False
            letters_wrong = []
            guesses = puzzle_goal[1] + 1

            while lost == False and won == False:
                for i in range (0, puzzle_goal[1]):
                    print("-", end = "")

                print("")

                guess = ""
                while len(guess) != puzzle_goal[1]:
                    guess = input()

                guess = guess.upper()

                if guess == puzzle_goal[0]:
                    print("\033[1;32;40m" + "{}".format(guess))
                    print("\033[0;37;40m")
                    won = True
                    print("You Win!")

                else:
                    guesses -= 1
                    check_word(guess, puzzle_goal)
                    print(str(guesses) + " guesses remaining.")

                    
                if guesses < 1:
                    lost = True
                    print("\nUh Oh! You lose! The answer was {}.\n".format(puzzle_goal[0]))


        case "3":
            print("Exiting game... Goodbye!")
            exit_game = True
