import pygame


class Point:
    def __init__(self, x, y, surface, colors, coordinates):
        self.x = x
        self.y = y
        self.colors = colors
        self.surface = surface
        self.coordinates = coordinates

    def draw(self):
        if len(self.coordinates) > 2:
            pygame.draw.lines(self.surface, self.colors, False, self.coordinates, 2)