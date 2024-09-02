from urllib.request import urlopen
import urllib.error
import re
import time
from colorama import Fore, Back, Style

wordnik_file = open("WordnikAPI.env", "r")

wordnik_key = wordnik_file.read()

wordnik_url = "http://api.wordnik.com/v4/words.json/randomWord?api_key=" + wordnik_key

def get_word():

    wordnik_response = 0

    while wordnik_response == 0:
        try:
            wordnik_response = urlopen(wordnik_url)
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

    word_tuple = (wordnik_response, len(wordnik_response))

    return word_tuple


exit_game = False

print("\n        ~ Welcome to Wordsle! ~")
print("------------------------------------------")

while exit_game == False:
    print("\nMain Menu:")
    print("1. Start Game")
    print("2. Instructions")
    print("3. Quit\n")

    selection = input()

    match selection:
        case "1":
            
            puzzle_goal = get_word()
            
            print("Your word is {} letters long. Get ready to guess!\n".format(puzzle_goal[1]))

            lost = False
            won = False
            letters_removed = []

            while lost == False and won == False:
                for el in range (0, puzzle_goal[1]):
                    print("-", end = "")

                print("")
                guess = ""
                while len(guess) != puzzle_goal[1]:
                    guess = input()

                print(guess)



                break




        case "3":
            print("Exiting game... Goodbye!")
            exit_game = True
