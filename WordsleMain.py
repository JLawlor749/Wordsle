from urllib.request import urlopen
from urllib.error import HTTPError
import re
import time

# Open environment variable file, read in API key.
wordnik_file = open("WordnikAPI.env", "r")
wordnik_key = wordnik_file.read()
wordnik_file.close()


def get_word(word_length:int):
    """
    This function retrieves a word of the length provided from the Wordnik API.
    It returns a tuple containing the word, and its length.
    """

    # Setting variable for API request, restricting the word to the desired length the corpus count to 10.
    wordnik_url = "http://api.wordnik.com/v4/words.json/randomWord?hasDictionaryDef=true&minCorpusCount=10&minLength=" + str(word_length) + "&maxLength=" + str(word_length) + "&api_key=" + wordnik_key

    wordnik_response = 0

    # Error handling: if the API returns the code for too many requests, wait until we have more. Otherwise return an error.
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

    # Reading and decoding API response, isolating the word itself using regular expressions and returning only it.
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

    # Create a list containing every letter in the word.  
    for el in target_word:
        goal_checklist.append(el)

    # Iterate over the word, checking for correct letters in the correct spot.
    for i in range (0, word_length):
        if word[i] == (target_word)[i]:
            
            # When a letter in the correct spot is found, a tuple with the green colour code AND the letter's index in the word to the guess, and remove the letter from the checklist.
            guess_print.append(("\033[1;32;40m", i))
            goal_checklist.remove(word[i])

    # Iterate again, check for correct letters in the wrong spot.
    for i in range (0, word_length):
        if word[i] in goal_checklist and word[i] != (target_word)[i] and word[i] != (target_word)[i]:

            #When found, add a tuple with the yellow colour code AND the letter's index, and remove that letter from the checklist.
            guess_print.append(("\033[1;33;40m", i))
            goal_checklist.remove(word[i])

    # If the letter isn't found in the word at all, we add a tuple with the red colour code to the guess list. Also add the letter to the list of incorrect letters.
    for i in range (0, word_length):
        if word[i] not in goal_checklist and ("\033[1;33;40m", i) not in guess_print and ("\033[1;32;40m", i) not in guess_print:
            guess_print.append(("\033[1;31;40m", i))
            
            if word[i] not in letters_wrong and word[i] not in target_word:
                letters_wrong.append(word[i])

    # Now, use a lamba (small anonymous function) and sort the guess list by the second tuple element, i.e. the letters' indexes.
    guess_print.sort(key=lambda tup:tup[1])

    # Print out the guess, with the letters coloured appropriately.
    for el in guess_print:
        print(el[0] + word[el[1]], end="")

    # Reset console colour.
    print("\033[0;37;40m")
    print("")



# This function is currently non-functional - the search feature of the Wordnik API does not currently work.
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

# Start the main loop for the game. This will re-enter the main menu after the completion of every game.
while exit_game == False:
    print("\nMain Menu:")
    print("1. Start Game")
    print("2. Instructions")
    print("3. Quit\n")

    # Uses a while loop to keep prompting for a selection as long as something other than an integer is being entered.
    selection = ""
    while type(selection) != int:
        try:
            selection = int(input())
            print("")
        except ValueError:
            print("Not a valid selection!\n")

    # Switch statement to enter the different options depending on what the user entered.
    match selection:
        case 1:

            # Uses a while loop to keep prompting for a selection as long as something other than an integer is being entered.
            desired_length = ""
            while type(desired_length) != int:
                print("Please input the length of the word you want to guess:")

                try:
                    desired_length = int(input())
                    print("")
                except ValueError:
                    print("That isn't a valid number!\n")
            
            # Call get_word() user-input length.
            puzzle_goal = get_word(desired_length)

            # If the API is for some reason unable to return a word, print an error message and skip the rest of this loop iteration, essentialy go back to main menu.
            if puzzle_goal == -1:
                print("A catastrophic error has occured. Please try again.")
                continue
            
            print("Input your guesses below:")

            lost = False
            won = False
            letters_wrong = []
            guesses = desired_length + 1

            # Enter the game loop, continues until either win or loss.
            while lost == False and won == False:

                # Print the list of letters already guessed that aren't in the word.
                print("Letters eliminated: ", end="")
                print(letters_wrong)
                print("")

                for i in range (0, desired_length):
                    print("-", end = "")

                print("")

                # Take input for the guess: continue prompting for input as long as the guess is the incorrect length or contains eliminated letters.
                guess = ""
                while len(guess) != desired_length:
                    guess = input()
                    guess = guess.upper()

                    # Iterate through the word looking for incorrect letters. If one is found, print error message and set guess to "", making it the wrong length and restarting the loop.
                    for el in letters_wrong:
                        if el in guess:
                            guess = ""
                            print("{} has already been guessed!".format(el))


                # Check if the guessed word is identical to the target without calling the function. If so, the game is won, print victory and end loop.
                if guess == puzzle_goal:
                    print("\033[1;32;40m" + "{}".format(guess))
                    print("\033[0;37;40m")
                    won = True
                    print("You Win!")

                # If the input word doesn't match the target, we call the function to check which letters are right, and take away a guess.
                else:
                    guesses -= 1
                    check_word(guess, puzzle_goal, desired_length)
                    print(str(guesses) + " guesses remaining.")

                # If our number of guesses falls below 1, we lose, print message and restart.
                if guesses < 1:
                    lost = True
                    print("\nUh Oh! You lose! The answer was {}.\n".format(puzzle_goal))



        # Exit gracefully, end the main loop, and the program.
        case 3:
            print("Exiting game... Goodbye!")
            exit_game = True
