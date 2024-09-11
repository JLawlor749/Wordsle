# Wordsle
A variant of the game "Wordle".

![The official Wordle game.](https://i.imgur.com/TutK3Fk.png)

![My own version, Wordsle, written in Python.](https://i.imgur.com/D9xwVr9.png)

Wordsle copies the basic interface and gameplay of Wordle in the console using Python.

It also has added functionality in that, rather than being set to a 5 letter word like Wordle, Wordsle allows the player to specify a length for the word they want to guess.

Wordsle uses the Wordnik API to request a random word of the specified length, and then uses ANSI escape sequences to display each letter the user guesses, depending on the correctness of each one.
