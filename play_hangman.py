import ctypes
import pygame as pg
import random

# pygame initialization////////////////////
user32 = ctypes.windll.user32
width, height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
pg.init()
screen = pg.display.set_mode((width, height))

my_font = pg.font.SysFont("Comic Sans MS", 60)
RED = (176, 0, 0)

tick = 0

# hangman preparations/////////////////////
bg = pg.image.load("textures/BG.png")
joke = my_font.render("Searching for man to hang...", False, RED)
screen.blit(bg, (-200, -300))
screen.blit(joke, (width // 2 - 200, height // 2))
pg.display.update()

word = ""
words = open("words.txt", encoding="utf-8")
for line in range(random.randint(0, 51301)):
    word = words.readline().replace("\n", "")
    random.randint(-10000, 100000)

for_endgame_word = word
mistakes = 0
word_to_show = ["*" for _ in word]
word_to_show[0], word_to_show[-1] = word[0], word[-1]
word = "*" + word[1:-1] + "*"
previous_guess = ""

man_zero_coord = (200, height - 600)
while mistakes != 6:

    # pygame drawing///////////////////////
    showing_word = my_font.render("".join(word_to_show), False, RED)
    showing_mistakes = my_font.render("mistakes: " + str(mistakes), False, RED)
    showing_previous_guess = my_font.render("your guess is: " + previous_guess, False, RED)
    man = pg.transform.scale(pg.image.load("textures/hangman_" + str(mistakes + 1) + ".png"), (500, 500))
    man.set_colorkey((255, 255, 255))

    screen.blit(bg, (-200, -300))
    screen.blit(showing_word, (width - 500, height//2 + 100))
    screen.blit(showing_mistakes, (width - 500, height//2 + 180))
    screen.blit(showing_previous_guess, (width - 500, height//2 + 20))
    screen.blit(man, man_zero_coord)
    pg.display.update()

    # pygame data collecting///////////////
    guess = ""
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            guess = event.unicode
            for_kill_game = pg.key.name(event.key)
            print(for_kill_game)
            # kill game////////////////////
            if guess == "escape":
                mistakes = 6
                tick = 500
                break
            # /////////////////////////////
            if len(guess) > 1:
                guess = ""
            previous_guess = guess

    # temp shit////////////////////////////
    if mistakes == 5:
        mistakes = 6

    # game data processing/////////////////
    temp = False
    tick = 0
    if guess != "":
        for letter in word:
            if guess == letter:
                word_to_show[tick], temp = guess, True

            tick += 1

        word = word.replace(guess, "*")
        if not temp:
            mistakes += 1

        print(word_to_show, mistakes, word, guess)

    # temp shit////////////////////////////
    elif word == "*" * (len(word) - 1) + "☼":
        break
    elif word == "*" * len(word):
        word += "☼"

# game results/////////////////////////////
if mistakes == 6:
    game_result = my_font.render("YOU LOST", False, RED)
    correct_word = my_font.render(for_endgame_word, False, RED)
    screen.blit(correct_word, (width//2 - 200, height//2 + 80))
    print("U LOST")
else:
    game_result = my_font.render("YOU WON", False, RED)
    print("U WON")

while tick != 500:
    tick += 1
    screen.blit(game_result, (width//2 - 200, height//2))
    pg.display.update()
