import keyword
from multiprocessing.connection import wait
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Hangman:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.mainWindow = QMainWindow()
        self.textBox = QLineEdit(self.mainWindow)
        self.possibleGuessesLabel = QLabel("Possible Guesses:", self.mainWindow)
        self.guessedLabel = QLabel("Guessed Letters:", self.mainWindow)
        self.wlLabel = QLabel(self.mainWindow)
        self.errorMessage = QMessageBox()
        self.hangmanPic = QLabel(self.mainWindow)
        self.wordLabel = QLabel(self.mainWindow)

        self.ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.possibleGuesses = []
        self.guessedLetters = []
        self.possibleGuesses.extend(self.ALPHABET)

        self. guessNum = int(0)
        self. maxGuesses = int(6)

        self.keyword = str()

        self.keywordArray = []
        self.KEYWORDARY = []
        self.displayedWord = []
        
        self.HANGMAN_PICS = ['''
            +---+
                |   
                |
                |
                |
                |
        =========''', '''
            +---+
            O   |   
                |
                |
                |
                |
        =========''', '''
            +---+
            O   |   
            |   |
                |
                |
                |
        =========''', '''
            +---+
            O   |   
           /|   |
                |
                |
                |
        =========''', '''
            +---+
            O   |   
           /|\  |
                |
                |
                |
        =========''', '''
            +---+
            O   |   
           /|\  |
           /    |
                |
                |
        =========''', '''
            +---+
            O   |   
           /|\  |
           / \  |
                |
                |
        =========''']

        self.showWindow()

    def showWindow(window):
        #set window properties
        window.mainWindow.setWindowTitle("Hangman Game") 
        window.mainWindow.resize(500, 500)
        window.mainWindow.setFont(QFont('Times', 8))

        #text input dialog for keyword
        window.keyword = QInputDialog.getText(window.mainWindow, "Enter Keyword", "Enter a keyword:")[0]
        window.keyword = window.keyword.upper()
        window.keywordArray = list(window.keyword)
        window.KEYWORDAR = list(window.keyword)
        window.displayedWord = ["_"] * len(window.keyword)

        #box to display hangman picture
        window.hangmanPic.setGeometry(QRect(10, 0, 100, 150))
        window.hangmanPic.setText(window.HANGMAN_PICS[0])

        #label to disply the keyword with blanks for unguessed letters
        window.wordLabel.setGeometry(QRect(110, -35, 100, 150))
        window.wordLabel.setText(' '.join(window.displayedWord))

        #Textbox to input guess
        window.textBox.move(20, 150)
        window.textBox.resize(100, 30)

        #Button to submit guess
        window.submitButton = QPushButton("Submit Guess", window.mainWindow)
        window.submitButton.move(20, 200)
        window.submitButton.resize(100, 30)
        window.submitButton.clicked.connect(lambda: window.submitGuess(window.textBox.text()))

        #Label to display possible guesses
        window.possibleGuessesLabel.move(20, 250)
        window.possibleGuessesLabel.resize(500, 30)
        window.possibleGuessesLabel.setText("Possible Guesses: " + ' '.join(window.possibleGuesses))

        #Label to display guessed letters
        window.guessedLabel.move(20, 300)
        window.guessedLabel.resize(500, 30)
        window.guessedLabel.setStyleSheet("QLabel { color: red; }")

        #Label to display winning/losing message
        window.wlLabel.move(20, 350)
        window.wlLabel.resize(500, 30)
        window.wlLabel.setFont(QFont('Times', 10))
        window.wlLabel.setStyleSheet("QLabel { color: blue; }")

        #Button to quit
        quitButton = QPushButton("Quit", window.mainWindow)
        quitButton.move(380, 20)
        quitButton.resize(100, 30)
        quitButton.clicked.connect(window.mainWindow.close)

        #error message popup
        window.errorMessage.setWindowTitle("You've activated my trap card!")
        window.errorMessage.setText("Please enter a valid letter :(")
        window.errorMessage.setStandardButtons(QMessageBox.Ok)

        window.mainWindow.show()
        sys.exit(window.app.exec_())

    def submitGuess(self, guess):
        guess = guess.upper()

        if guess not in self.possibleGuesses:
            #show error message
            self.errorMessage.exec_()
        else:
            if guess in self.keyword:
                self.removeLetter(guess)
                self.wlLabel.setText("Correct :)")
                if self.keywordArray == []:
                    self.win()
            else:
                self.removeLetter(guess)
                self.guessNum += 1
                self.wlLabel.setText("Incorrect :(")
                self.hangmanPic.setText(self.HANGMAN_PICS[self.guessNum])

                if(self.guessNum == self.maxGuesses):
                    self.lose()

        #clear textbox
        self.textBox.clear()
    
    def removeLetter(self, guess):
        if guess in self.keywordArray:
            self.keywordArray = self.rmVal(self.keywordArray, guess)

        #put a letter in the spot where the letter is in the keyword
        for i in range(len(self.KEYWORDAR)):
            if self.KEYWORDAR[i] == guess:
                self.displayedWord[i] = guess
        
        self.wordLabel.setText(' '.join(self.displayedWord))

        self.possibleGuesses.remove(guess)
        self.guessedLetters.append(guess)
        self.possibleGuessesLabel.setText("Possible Guesses: " + ' '.join(self.possibleGuesses))
        self.guessedLabel.setText("Guessed Letters: " + ' '.join(self.guessedLetters))

    def win(self):
        self.wlLabel.setText("You Win!")
        self.textBox.setEnabled(False)
        self.submitButton.setEnabled(False)
        self.hangmanPic.setText(self.HANGMAN_PICS[0])
        self.errorMessage.setText("The word was: " + self.keyword + ". Nice Guessing!")
        
    def lose(self):
        self.wlLabel.setText("You lose :(")
        self.textBox.setEnabled(False)
        self.submitButton.setEnabled(False)
        self.hangmanPic.setText(self.HANGMAN_PICS[0])
        self.errorMessage.setText("The word was: " + self.keyword + ". Better luck next time!")

    def rmVal(self, list, val):
        return [value for value in list if value != val]

hangman = Hangman()