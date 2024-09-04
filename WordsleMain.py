from urllib.request import urlopen
import urllib.error
import re
import time

wordnik_file = open("WordnikAPI.env", "r")

wordnik_key = wordnik_file.read()

wordnik_url = "http://api.wordnik.com/v4/words.json/randomWord?minCorpusCount=15&minLength=5&maxLength=5&api_key=" + wordnik_key

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

    wordnik_response = wordnik_response.upper()

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
            
            print("Input your guesses below:\n")

            lost = False
            won = False
            letters_wrong = []
            guesses = 5

            #print(puzzle_goal[0])

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

                    goal_checklist = []
                    guess_print = []
                    
                    for el in puzzle_goal[0]:
                        goal_checklist.append(el)

                    for i in range (0, puzzle_goal[1]):
                        if guess[i] == (puzzle_goal[0])[i]:
                            guess_print.append(("\033[1;32;40m", i))
                            goal_checklist.remove(guess[i])

                    for i in range (0, puzzle_goal[1]):
                        if guess[i] in goal_checklist and guess[i] != (puzzle_goal[0])[i] and guess[i] != (puzzle_goal[0])[i]:
                            guess_print.append(("\033[1;33;40m", i))
                            goal_checklist.remove(guess[i])

                    for i in range (0, puzzle_goal[1]):
                        if guess[i] not in goal_checklist and ("\033[1;33;40m", i) not in guess_print and ("\033[1;32;40m", i) not in guess_print:
                            guess_print.append(("\033[1;31;40m", i))

                    guess_print.sort(key=lambda tup:tup[1])

                    for el in guess_print:
                        print(el[0] + guess[el[1]], end="")

                    print("\033[0;37;40m")
                    print("")
                    

                if guesses < 1:
                    lost = True
                    print("\nUh Oh! You lose! The answer was {}.\n".format(puzzle_goal[0]))




        case "3":
            print("Exiting game... Goodbye!")
            exit_game = True
