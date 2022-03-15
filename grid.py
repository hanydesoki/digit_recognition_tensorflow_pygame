import pygame
import numpy as np
import prediction

def get_coord(pos, tile_size):
    x, y = pos
    return int(x/tile_size), int(y/tile_size)


class Grid:

    def __init__(self, screen_width, screen_height, screen, n=28):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = screen
        self.n = n
        self.grid = np.zeros((self.n, self.n))

        self.sub_screen_width = self.screen_width*0.8
        self.sub_screen_height = self.screen_height*0.8

        self.surf = pygame.Surface((self.sub_screen_width, self.sub_screen_height))
        self.surf.fill((0,0,0))

        self.offset = (int((self.screen_width - self.sub_screen_width)/2),
                       int((self.screen_height - self.sub_screen_height)/2))

        self.tile_size = int(self.sub_screen_width/self.n)

        self.black_tile = pygame.Surface((self.tile_size, self.tile_size))
        self.black_tile.fill((0, 0, 0))
        self.white_tile = pygame.Surface((self.tile_size, self.tile_size))
        self.white_tile.fill((255, 255, 255))
        self.gray_tile = pygame.Surface((self.tile_size, self.tile_size))
        self.gray_tile.fill((100, 100, 100))
        self.prediction = None
        self.pred_font = pygame.font.Font(self.prediction, 50)
        self.number_font = pygame.font.Font(self.prediction, 50)

        self.disp_probs = False


    def draw(self):
        self.screen.blit(self.surf, self.offset)

        if self.prediction is not None:
            self.pred_surf = self.pred_font.render(f'Prediction: {self.prediction}', True, 'white')
            self.pred_rect = self.pred_surf.get_rect(center=(self.screen_width // 2, 30))
            self.screen.blit(self.pred_surf, self.pred_rect)

        for i in range(self.n):
            for j in range(self.n):
                if self.grid[i, j]:
                    if self.grid[i, j] == 1.0:
                        self.screen.blit(self.white_tile,
                                    (i*self.tile_size + self.offset[0], j * self.tile_size + self.offset[1]))
                    else:
                        self.screen.blit(self.gray_tile,
                                         (i * self.tile_size + self.offset[0], j * self.tile_size + self.offset[1]))
    def input(self):
        mouse_pos = pygame.mouse.get_pos()

        if (self.offset[0] < mouse_pos[0] < self.screen_width - self.offset[0])\
                and (self.offset[1] < mouse_pos[1] < self.screen_height - self.offset[1]):
            pygame.draw.circle(self.screen, (255, 255, 255), mouse_pos, self.tile_size*3/2)
            if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]:

                pos = (mouse_pos[0] - self.offset[0], mouse_pos[1] - self.offset[1])
                i, j = get_coord(pos, self.tile_size)

                if pygame.mouse.get_pressed()[0]:
                    if i in range(self.n) and j in range(self.n):
                        self.grid[i, j] = 1.0
                        if i + 1 <= self.n - 1:
                            self.grid[i + 1, j] = 0.8 if self.grid[i + 1, j] == 0 else 1
                        if j + 1 <= self.n - 1:
                            self.grid[i, j + 1] = 0.8 if self.grid[i, j + 1] == 0 else 1
                        if i - 1 >= 0:
                            self.grid[i - 1, j] = 0.8 if self.grid[i - 1, j] == 0 else 1
                        if j - 1 >= 0:
                            self.grid[i, j - 1] = 0.8 if self.grid[i, j - 1] == 0 else 1


                elif pygame.mouse.get_pressed()[2]:
                    if i in (k for k in range(self.n)) and j in (k for k in range(self.n)):
                        self.grid[i, j] = 0.0
                        if i + 1 <= self.n - 1:
                            self.grid[i + 1, j] = 0.0
                        if j + 1 <= self.n - 1:
                            self.grid[i, j + 1] = 0.0
                        if i - 1 >= 0:
                            self.grid[i - 1, j] = 0.0
                        if j - 1 >= 0:
                            self.grid[i, j - 1] = 0.0

    def predict_value(self):
        X = self.grid.reshape((1, 28, 28, 1)).T
        self.preds = prediction.predict(X)
        pred = np.argmax(self.preds, axis=-1)[0]
        self.prediction = pred
        self.disp_probs = True

    def disp_numbers(self):
        if self.disp_probs:
            for i in range(10):
                color = (int(self.preds[0][i]*255), 0, int(self.preds[0][i]*255))
                self.number_surf = self.number_font.render(f'{i}', True, color)
                self.number_rect = self.number_surf.get_rect(center=(self.screen_width - 30,
                                                                     self.offset[1]*2 + i*40))
                self.screen.blit(self.number_surf, self.number_rect)


    def clear(self):
        self.grid = np.zeros((self.n, self.n))


    def update(self):
        self.draw()
        self.disp_numbers()
        self.input()