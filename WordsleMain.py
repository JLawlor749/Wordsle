from urllib.request import urlopen
import re

wordnik_file = open("WordnikAPI.env", "r")

wordnik_key = wordnik_file.read()

wordnik_url = "http://api.wordnik.com/v4/words.json/randomWord?api_key=" + wordnik_key

def get_word():
    wordnik_response = urlopen(wordnik_url)

    wordnik_response = wordnik_response.read()

    wordnik_response = wordnik_response.decode("utf-8")

    wordnik_response = re.sub("{\"word\":\"", "", wordnik_response)

    wordnik_response = re.sub("\",\"id\":0}", "", wordnik_response)

    return wordnik_response


exit_game = False

print("\n        ~ Welcome to Wordsle! ~")
print("------------------------------------------")

while exit_game == False:
    print("Would you like to start a game?")
    print("Yes/No\n")

    selection = input()

    match selection:
        case "Yes" | "yes" | "y" | "Y":
            pass

        case "No" | "no" | "N" | "n":
            print("Exiting game... Goodbye!")
            exit_game = True
