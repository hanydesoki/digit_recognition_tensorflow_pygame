import pygame
from grid import Grid


class Game:

    def __init__(self, screen_width, screen_height, screen):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = screen
        self.grid = Grid(self.screen_width, self.screen_height, self.screen)
        self.backgroung = pygame.Surface((self.screen_width, self.screen_height))
        self.backgroung.fill((50, 50, 50))

        self.bouton_nettoyer_surf = pygame.image.load(('bouton_nettoyer.png')).convert_alpha()
        self.bouton_nettoyer_surf = pygame.transform.scale(self.bouton_nettoyer_surf, (30, 30))
        self.bouton_nettoyer_rect = self.bouton_nettoyer_surf.get_rect(topleft=(100, 10))

        self.bouton_nettoyer_enf_surf = pygame.image.load(('bouton_nettoyer_enf.png')).convert_alpha()
        self.bouton_nettoyer_enf_surf = pygame.transform.scale(self.bouton_nettoyer_enf_surf, (30, 30))
        self.bouton_nettoyer_enf_rect = self.bouton_nettoyer_enf_surf.get_rect(topleft=(100, 10))

    def input(self):
        self.screen.blit(self.bouton_nettoyer_surf, self.bouton_nettoyer_rect)

        if self.bouton_nettoyer_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            self.screen.blit(self.bouton_nettoyer_enf_surf, self.bouton_nettoyer_rect)
            self.grid.clear()

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.grid.predict_value()

    def update(self):
        self.screen.blit(self.backgroung, (0, 0))
        self.input()
        self.grid.update()