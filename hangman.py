import pygame
import requests
import random


pygame.init()
window = pygame.display.set_mode((650, 500))
pygame.display.set_caption("Hangman")
arial = pygame.font.SysFont("Arial", 30)
arialBig = pygame.font.SysFont("Arial", 60)

# Main Game Logic
class Hangman():
    def __init__(self, answer):
        self._answer = answer.upper()
        self.problem = [(self._answer[i], False)
                        for i in range(len(self._answer))]
        self.tries = 6

    def getProblemList(self):
        problem = list(map(lambda x: x[0] if x[1] else '_', self.problem))
        return problem

    def getSolution(self):
        return self._answer

    def checkGuess(self, guess):
        guess = guess.upper()
        letterExists = False
        for i in range(len(self.problem)):
            if (guess == self.problem[i][0]) and (not self.problem[i][1]):
                self.problem[i] = (self.problem[i][0], True)
                letterExists = True

        if not letterExists:
            self.tries -= 1
            return False

        return True

    def checkSolved(self):
        solvedPart = list(filter(lambda x: x[1], self.problem))
        if solvedPart == self.problem:
            return True
        else:
            return False


class LetterButton():
    width = 40
    height = 40

    def __init__(self, letterNumber, letter):
        self.x = (letterNumber % 13) * 50
        self.y = 150 if letterNumber < 13 else 200
        self.letter = letter
        self.letterWidth = arial.size(letter)[0]
        self.xPosition = (50 - self.letterWidth) // 2

    def draw(self, window):
        pygame.draw.rect(window, (252, 158, 79), (self.x + 5,
                                                   self.y + 5, self.width, self.height), 4)
        letter = arial.render(self.letter, True, (252, 158, 79))
        window.blit(letter, (self.x + self.xPosition, self.y + 9))


class Tries():
    def __init__(self):
        self.tries = 6
        self.x = 125
        self.y = 300
        self.message = 'Tries :'

    def reduceTries(self):
        self.tries -= 1

    def draw(self, window):
        if self.tries > 0 and self.message == 'Tries :':
            text = arial.render(self.message, True, (244, 68, 46))
            window.blit(text, (self.x, self.y))

            for i in range(self.tries):
                number = arial.render(str(i + 1), True, (244, 68, 46))
                window.blit(number, (self.x + 100 + (i * 50), self.y))
        else:
            xPosition = self.x - 45
            if self.tries == 0:
                self.message = 'You have no more tries left'
                xPosition = self.x + 25
            text = arial.render(self.message, True, (244, 68, 46))
            window.blit(text, (xPosition, self.y))

            RestartButton.draw(window)
            NewGameButton.draw(window)


class Problem():
    def __init__(self, problemList):
        self.problemList = problemList
        self.x = 50
        self.width = 550 / len(problemList)
        self.y = 450

    def refreshProblem(self, problemList):
        self.problemList = problemList

    def draw(self, window):
        for i, char in enumerate(self.problemList):
            letter = arial.render(char, True, (242, 243, 174))
            xPosition = int(((i * self.width) + ((i+1) * self.width)) / 2 - 10)
            window.blit(letter, (self.x + xPosition, self.y))


class RestartButton():
    @staticmethod
    def draw(window):
        pygame.draw.rect(window, (237, 211, 130), (84, 350, 200, 50), 4)
        text = arial.render('Restart !', True, (237, 211, 130))
        window.blit(text, (131, 358))


class NewGameButton():
    @staticmethod
    def draw(window):
        pygame.draw.rect(window, (237, 211, 130), (368, 350, 200, 50), 4)
        text = arial.render('New Game', True, (237, 211, 130))
        window.blit(text, (400, 358))


def createGame(word):
    global hangman, problem, tries, letterButtons

    hangman = Hangman(word)
    problem = Problem(hangman.getProblemList())
    tries = Tries()

    letterButtons = []
    char = 'A'
    index = 0
    while char <= 'Z':
        letterButtons.append(LetterButton(index, char))
        index += 1
        char = chr(ord(char) + 1)


def getWord():
    global word

    offlineWords = ['hello', 'material', 'python', 'infinity', 'guitar', 'workspace', 'mobile', 'dinosaur', 'keyboard', 'office']
    url = 'https://random-word-api.herokuapp.com/word?number=1'

    try:
        response = requests.get(url)
        word = response.json()[0]
    except :
        word = random.choice(offlineWords)    
    
    print(word)


def getButtonIndex(x, y):
    for i, button in enumerate(letterButtons):
        if ((button.x + 5) <= x <= (button.x + 45)) and ((button.y + 5) <= y <= (button.y + 45)):
            return i

    return False


def processGuess(i):
    guess = letterButtons[i].letter
    letterButtons.pop(i)

    guessResult = hangman.checkGuess(guess)
    problem.refreshProblem(hangman.getProblemList())

    if not guessResult:
        tries.reduceTries()


def checkHangman():
    global gameActive

    if hangman.checkSolved():
        tries.message = "Congratulations. You have solved it !!"
        gameActive = False

    if hangman.tries == 0:
        gameActive = False



def redrawWindow():
    window.fill((2, 1, 34))

    gameName = arialBig.render('Hangman', True, (242, 243, 174))
    window.blit(gameName, (200, 35))

    for button in letterButtons:
        button.draw(window)

    tries.draw(window)

    problem.draw(window)

    pygame.display.update()


getWord()
createGame(word)
gameActive = True
run = True
while run:
    checkHangman()
    redrawWindow()

    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            buttonIndex = getButtonIndex(mouse[0], mouse[1])

            if type(buttonIndex) == int and gameActive:
                processGuess(buttonIndex)

            if not gameActive:
                if 84 <= mouse[0] <= 284 and 350 <= mouse[1] <= 400:
                    createGame(word)
                    gameActive = True
                elif 368 <= mouse[0] <= 568 and 350 <= mouse[1] <= 400:
                    getWord()
                    createGame(word)
                    gameActive = True


pygame.quit()
