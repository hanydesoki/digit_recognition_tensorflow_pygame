from sys import exit
import pygame
from game import Game

#initialize the pygame
pygame.init()

screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption('Reconnaissance nombre')
clock = pygame.time.Clock()

game = Game(screen_width, screen_height, screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    game.update()

    pygame.display.update()
    clock.tick(60)

