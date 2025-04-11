# -*- coding:utf-8 -*-
import pygame
from ..utils.constants import BLOCK_WIDTH, BLOCK_HEIGHT, RED

class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = BLOCK_WIDTH
        self.height = BLOCK_HEIGHT
        self.rect = pygame.Rect(x, y, self.width, self.height)
    
    def draw(self, screen):
        pygame.draw.rect(screen, RED, self.rect) 