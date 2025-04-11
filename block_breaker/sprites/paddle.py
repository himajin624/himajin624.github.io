# -*- coding:utf-8 -*-
import pygame
from pygame.locals import *
from ..utils.constants import PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_SPEED, SCREEN_WIDTH, BLUE

class Paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.speed = PADDLE_SPEED
        self.rect = pygame.Rect(x, y, self.width, self.height)
    
    def move_left(self):
        if self.x > 0:
            self.x -= self.speed
            self.rect.x = self.x
    
    def move_right(self):
        if self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed
            self.rect.x = self.x
    
    def update(self):
        """パドルの状態を更新"""
        # キー入力処理
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] or keys[K_a]:
            self.move_left()
        if keys[K_RIGHT] or keys[K_d]:
            self.move_right()
    
    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, self.rect) 