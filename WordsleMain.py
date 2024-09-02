from urllib.request import urlopen
import urllib.error
import re
import time

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
    print("Would you like to start a game?")
    print("Yes/No\n")

    selection = input()

    match selection:
        case "Yes" | "yes" | "y" | "Y":
            
            puzzle_goal = get_word()
            
            print("Your word is {} letters long. Get ready to guess!\n".format(puzzle_goal[1]))



        case "No" | "no" | "N" | "n":
            print("Exiting game... Goodbye!")
            exit_game = True
