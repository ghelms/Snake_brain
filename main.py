import pygame
from pygame import mixer
import time
import pandas
import math
import random

# Intitializing game
pygame.init()

# Create the screen
screen = pygame.display.set_mode((960, 600))

# Background
background = pygame.image.load("snake_background.jpg")

# Background sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Title and icon
pygame.display.set_caption("Snake invaders")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

# Loosing image:
losingIMG = pygame.image.load("game-over.png")

# Making a snake
snake_img = pygame.image.load("brain.png")
snake_angle = 0
snakeX = 480
snakeY = 300
snakeX_change = 0
snakeY_change = 0

# making a tail
tail_img = pygame.image.load("neuron.png")
tail_x = 0
tail_y = 0
tail_angle = 0

# Making food
food_img = pygame.image.load("food.png")
food_x = random.randint(10, 944)
food_y = random.randint(10, 584)

# Making an empty dataframe for logging the coordinates with 18 rows of the start position
log = pandas.DataFrame(columns=["Count", "Snake_x", "Snake_y", "Snake_angle"])

# Making a counter
counter = 0
no_tails = 0

# Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
text_X = 10
text_y = 10


# Defining functions
def snake(x, y, angle):
    surf = pygame.transform.rotate(snake_img, angle)
    screen.blit(surf, (x, y))


def tail(x, y, angle):
    surf_tail = pygame.transform.rotate(tail_img, angle)
    screen.blit(surf_tail, (x, y))


def food(x, y):
    screen.blit(food_img, (x, y))


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def isCollision_food(snakeX, snakeY, foodX, foodY):
    distance = math.sqrt((math.pow(snakeX - foodX, 2)) + (math.pow(snakeY - foodY, 2)))
    if distance < 27:
        return True
    else:
        return False


def isCollision_tail(snakeX, snakeY, tailX, tailY):
    distance = math.sqrt((math.pow(snakeX - tailX, 2)) + (math.pow(snakeY - tailY, 2)))
    if distance < 10:
        return True
    else:
        return False


# Game loop
running = True
lose = False
win = False

while running:

    # RGB - (MAKING IT WHITE)
    screen.fill((255, 255, 255))

    # Adding background
    screen.blit(background, (0, 0))

    # Looping through events
    for event in pygame.event.get():

        # Making sure we can quit the game
        if event.type == pygame.QUIT:
            running = False

        # Making the snake move
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                snakeX_change = -2
                snakeY_change = 0
                snake_angle = 90
            if event.key == pygame.K_RIGHT:
                snakeX_change = 2
                snakeY_change = 0
                snake_angle = 270
            if event.key == pygame.K_UP:
                snakeY_change = -2
                snakeX_change = 0
                snake_angle = 0
            if event.key == pygame.K_DOWN:
                snakeY_change = 2
                snakeX_change = 0
                snake_angle = 180
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                running = False

    # Adding new coordinates to snakes position and counter
    snakeX += snakeX_change
    snakeY += snakeY_change
    counter += 1

    # Making a border:
    if snakeX <= 0:
        snakeX = 0
        lose = True
    elif snakeX >= 936:
        snakeX = 936
        lose = True
    if snakeY <= 0:
        snakeY = 0
        lose = True
    elif snakeY >= 576:
        snakeY = 576
        lose = True

    # Updating snake position
    snake(snakeX, snakeY, snake_angle)

    # Adding all the snake data to the logfile
    log = log.append({
        "Count": counter,
        "Snake_x": snakeX,
        "Snake_y": snakeY,
        "Snake_angle": snake_angle
    }, ignore_index=True)

    # Looping through number of tails and painting them all on the screen.
    for i in range(1, no_tails + 1):
        # The coordinates for the tail are the same as the ones for the snake 18 loops ago. This is done by indexing.
        tail_x = log["Snake_x"][log["Count"][counter - 18 * i]]
        tail_y = log["Snake_y"][log["Count"][counter - 18 * i]]
        tail_angle = log["Snake_angle"][log["Count"][counter - 18 * i]]
        tail(tail_x, tail_y, tail_angle)  # Painting a tail on the screen

        # Checking if the snake has collided with the tail
        collission_tail = isCollision_tail(snakeX, snakeY, tail_x, tail_y)
        if collission_tail:
            lose = True

    # Adding the food
    food(food_x, food_y)

    # Showing the score
    show_score(text_X, text_y)

    # Collision
    collision_food = isCollision_food(snakeX, snakeY, food_x, food_y)
    if collision_food:
        eating_sound = mixer.Sound("explosion.wav")
        eating_sound.play()
        no_tails += 1
        score_value += 1
        food_x = random.randint(10, 944)
        food_y = random.randint(10, 584)

    # Removing redundant lines in the logfile
    # length_log = len(log["Count"])
    # print(length_log)
    # if length_log > 100:
    #    print(len(log["Count"]))
    #   log = log.drop(log.index[:1])
    #  print(len(log["Count"]))

    # IF LOST - TEXT
    if lose:
        screen.blit(losingIMG, (224, 64))
        pygame.display.update()
        time.sleep(2)
        running = False

    # Update the screen
    pygame.display.update()

print(log)
print(score_value)