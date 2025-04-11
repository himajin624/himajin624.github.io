# -*- coding:utf-8 -*-
import pygame
from ..utils.constants import BLOCK_WIDTH, BLOCK_HEIGHT, YELLOW

class MultihitBlock:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.width = BLOCK_WIDTH
        self.height = BLOCK_HEIGHT
        self.color = color
        self.rect = pygame.Rect(x, y, self.width, self.height)
    
    def draw(self, screen):
        pygame.draw.rect(screen, YELLOW, self.rect)