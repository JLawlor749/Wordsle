from urllib.request import urlopen
from urllib.error import HTTPError
import re
import time



wordnik_file = open("WordnikAPI.env", "r")
wordnik_key = wordnik_file.read()



def get_word(word_length:int):
    """
    This function retrieves a word of the length provided from the Wordnik API.
    It returns a tuple containing the word, and its length.
    """

    wordnik_url = "http://api.wordnik.com/v4/words.json/randomWord?hasDictionaryDef=true&minCorpusCount=10&minLength=" + str(word_length) + "&maxLength=" + str(word_length) + "&api_key=" + wordnik_key

    wordnik_response = 0

    while wordnik_response == 0:
        try:
            wordnik_response = urlopen(wordnik_url)
        except HTTPError as e:
            if e.code == 429:
                print("\nToo many requests. Please wait...\n")
                time.sleep(12)
            else:
                return -1

    #Uncomment to get response header information on word requests.
    #print(wordnik_response.info())

    wordnik_response = wordnik_response.read()

    wordnik_response = wordnik_response.decode("utf-8")

    wordnik_response = re.sub("{\"word\":\"", "", wordnik_response)

    wordnik_response = re.sub("\",\"id\":0}", "", wordnik_response)

    wordnik_response = wordnik_response.upper()

    return wordnik_response



def check_word(word:str, target_word:str, word_length:int):
    """
    This function checks each letter in the guessed word against the target.
    It prints each letter of the guess in a different colour based on correctness.
    \nGREEN = Correct letter in the correct space.
    \nYELLOW = Correct letter in the wrong space.
    \nRED = Wrong letter.
    """

    goal_checklist = []
    guess_print = []
                    
    for el in target_word:
        goal_checklist.append(el)

    for i in range (0, word_length):
        if word[i] == (target_word)[i]:
            guess_print.append(("\033[1;32;40m", i))
            goal_checklist.remove(word[i])

    for i in range (0, word_length):
        if word[i] in goal_checklist and word[i] != (target_word)[i] and word[i] != (target_word)[i]:
            guess_print.append(("\033[1;33;40m", i))
            goal_checklist.remove(word[i])

    for i in range (0, word_length):
        if word[i] not in goal_checklist and ("\033[1;33;40m", i) not in guess_print and ("\033[1;32;40m", i) not in guess_print:
            guess_print.append(("\033[1;31;40m", i))

    guess_print.sort(key=lambda tup:tup[1])

    for el in guess_print:
        print(el[0] + word[el[1]], end="")

    print("\033[0;37;40m")
    print("")



def check_dictionary(word:str):
    """
    This function checks if a given word is present in the Wordnik dictionary.
    """
    wordnik_url = "ttps://api.wordnik.com/v4/words.json/search/word?caseSensitive=false&limit=1&api_key=" + wordnik_key

    wordnik_response = 0

    while wordnik_response == 0:
        try:
            wordnik_response = urlopen(wordnik_url)
        except HTTPError as e:
            if e.code == 429:
                print("\nToo many requests. Please wait...\n")
                time.sleep(12)
            else:
                return -1
            
    wordnik_response = wordnik_response.read()

    wordnik_response = wordnik_response.decode("utf-8")

    wordnik_response = re.sub("{\"word\":\"", "", wordnik_response)

    wordnik_response = re.sub("\",\"id\":0}", "", wordnik_response)




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
            
            
            puzzle_goal = get_word(desired_length)

            if puzzle_goal == -1:
                print("A catastrophic error has occured. Please try again.")
                continue
            
            print("Input your guesses below:")

            lost = False
            won = False
            letters_wrong = []
            guesses = desired_length + 1

            while lost == False and won == False:
                for i in range (0, desired_length):
                    print("-", end = "")

                print("")

                guess = ""

                while len(guess) != desired_length:
                    guess = input()

                guess = guess.upper()

                if guess == puzzle_goal:
                    print("\033[1;32;40m" + "{}".format(guess))
                    print("\033[0;37;40m")
                    won = True
                    print("You Win!")

                else:
                    guesses -= 1
                    check_word(guess, puzzle_goal, desired_length)
                    print(str(guesses) + " guesses remaining.")

                    
                if guesses < 1:
                    lost = True
                    print("\nUh Oh! You lose! The answer was {}.\n".format(puzzle_goal))


        case "3":
            print("Exiting game... Goodbye!")
            exit_game = True
