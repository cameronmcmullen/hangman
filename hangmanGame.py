import json
import pygame
import random
pygame.init()

pygame.display.set_caption("Hangman") # caption fromt the display class

# Load images
person = [pygame.image.load('images/person1.png'), pygame.image.load('images/person2.png'), pygame.image.load('images/person3.png'), pygame.image.load('images/person4.png'), pygame.image.load('images/person5.png'), pygame.image.load('images/person6.png'), pygame.image.load('images/person7.png')]
hangPole = pygame.image.load('images/hangman_pole.png')

# read file
with open('words.json', 'r') as myfile:
    data=myfile.read()

# parse file
obj = json.loads(data)
wordBank = obj['data']

LETTER_XSTART = 280
LETTER_XEND = 800
LETTER_YHEIGHT = 220



class Letter:
    def __init__(self, letter, x, y, radius, color, borderColor, borderWidth=5):
        self.letter = letter
        self.x = x
        self.y = y
        self.radius = radius
        self.guessed = False
        self.color = color
        self.borderWidth = borderWidth
        self.borderColor = borderColor

    def isclicked(self, x, y):
        if (x - self.x) ** 2 + (y - self.y) ** 2 <= self.radius ** 2:
            return True
        return False

    def draw(self, surface):
        if not self.guessed:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
            pygame.draw.ellipse(surface, self.borderColor, (self.x - self.radius, self.y - self.radius, 2 * self.radius, 2 * self.radius), self.borderWidth)

            font = pygame.font.SysFont('comicsans', 50, True)
            text = font.render(self.letter, 1, (0, 0, 0))
            win.blit(text, ((self.x - text.get_width() / 2), self.y - text.get_height() / 2))

    def clicked(self):
        self.guessed = True


class Blank:

    defaultWidth = 40
    heightSpacing = 5

    def __init__(self, letter, x, y, width, visible, height=3):
        self.letter = letter
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.visible = visible

    def showLetter(self):
        self.visible = True

    def draw(self, surface):
        global blankWidth
        pygame.draw.rect(surface, (0, 0, 0), (self.x, self.y, self.width, self.height))

        font = pygame.font.SysFont('comicsans', blankWidth, True)
        if self.visible:
            text = font.render(self.letter, 1, (0, 0, 0))
            win.blit(text, (self.x + (blankWidth / 2 - text.get_width() / 2), self.y - self.height - text.get_height()))



def redrawWindow(surface, blanks, letters):
    surface.fill((255, 255, 255))
    win.blit(hangPole, (10, 0))
    if mistakes > 0:
        win.blit(person[mistakes - 1], (140, 10))

    for blank in blanks:
        blank.draw(surface)

    for letter in letters:
        letter.draw(surface)
    pygame.display.update()

def determineBlankWidth(word, spacing, defaultWidth):
    global LETTER_XSTART, LETTER_XEND
    distance = LETTER_XEND - LETTER_XSTART
    numChar = len(word)
    if distance > spacing * defaultWidth * numChar:
        return defaultWidth
    else:
        charWidth = distance / numChar
        charWidth = int(charWidth // spacing)
        return charWidth

def createBlanks(spacing, word, blankWidth):
    blanks = []
    specialCharacters = ['-', '?', "'"]
    for i in range(len(word)):
        if word[i] != " ":
            if word[i] not in specialCharacters:
                blanks.append(Blank(word[i], i * spacing * blankWidth + LETTER_XSTART, LETTER_YHEIGHT, blankWidth, False))
            else:
                blanks.append(
                    Blank(word[i], i * spacing * blankWidth + LETTER_XSTART, LETTER_YHEIGHT, blankWidth, True))
    return blanks

def createLetters(spacing, yStart, color, borderCol):
    alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    rows = 2
    lettersPerRow = 13

    radius = int((800 - spacing) / (2 * lettersPerRow))
    space = (spacing + 800 - spacing - 2 * radius * lettersPerRow) / (lettersPerRow + 1)

    letters = []

    letterIndex = 0
    for i in range(rows):
        for j in range(lettersPerRow):
            letters.append(Letter(alphabet[letterIndex], j * (2 * radius + space) + space + radius, yStart + i * (3 * radius + space), radius, color, borderCol))
            letterIndex += 1
    return letters

def updateBlanks(char):
    global letterBlanks
    for blank in letterBlanks:
        if char == blank.letter or char.lower() == blank.letter:
            blank.showLetter()

def updateMistakes(char):
    global letterBlanks, mistakes
    char = char.lower()
    if char not in [blank.letter for blank in letterBlanks]:
        mistakes += 1

def gameWon():
    global letterBlanks
    for blank in letterBlanks:
        if not blank.visible:
            return False
    return True

def gameLost():
    global mistakes, personm, numLives
    if mistakes == numLives:
        return True
    return False


# maiin Loop
win = pygame.display.set_mode((800, 500)) # creates window (width, height)
word = random.choice(wordBank)
spacingMultiplier = 1.2
blankWidth = determineBlankWidth(word, spacingMultiplier, Blank.defaultWidth)
letterBlanks = createBlanks(spacingMultiplier, word, blankWidth)
letters = createLetters(100, 325, (178, 249, 252), (15, 2, 193))
mistakes = 0
numLives = len(person)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            for letter in letters:
                if letter.isclicked(pos[0], pos[1]):
                    letter.clicked()
                    updateBlanks(letter.letter)
                    updateMistakes(letter.letter)

    redrawWindow(win, letterBlanks, letters)

    if gameWon():
        run = False
        pygame.time.delay(1000)

    if gameLost():
        for blank in letterBlanks:
            blank.showLetter()
        redrawWindow(win, letterBlanks, letters)
        pygame.time.delay(1000)
        run = False
pygame.quit()



