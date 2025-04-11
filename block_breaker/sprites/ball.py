# -*- coding:utf-8 -*-
import pygame
import math
from ..utils.constants import BALL_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BALL_SPEED_X, BALL_SPEED_Y

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = BALL_SIZE
        self.dx = BALL_SPEED_X
        self.dy = BALL_SPEED_Y
        self.base_speed = (BALL_SPEED_X ** 2 + BALL_SPEED_Y ** 2) ** 0.5
        self.rect = pygame.Rect(x, y, self.size, self.size)
        # 前回の位置を保存
        self.prev_x = x
        self.prev_y = y
    
    def update(self):
        # 前回の位置を保存
        self.prev_x = self.x
        self.prev_y = self.y
        
        # 位置を更新
        self.x += self.dx
        self.y += self.dy
        self.rect.x = self.x
        self.rect.y = self.y
        
        # 壁との衝突判定
        if self.x <= 0:
            self.x = 0
            self.dx = abs(self.dx)  # 必ず右向きにする
        elif self.x >= SCREEN_WIDTH - self.size:
            self.x = SCREEN_WIDTH - self.size
            self.dx = -abs(self.dx)  # 必ず左向きにする
            
        if self.y <= 0:
            self.y = 0
            self.dy = abs(self.dy)  # 必ず下向きにする
        
        # 速度の大きさを一定に保つ
        self.normalize_speed()
    
    def normalize_speed(self):
        # 現在の速度の大きさを計算
        current_speed = (self.dx ** 2 + self.dy ** 2) ** 0.5
        if current_speed > 0:
            # 速度ベクトルを正規化してから基本速度を掛ける
            self.dx = (self.dx / current_speed) * self.base_speed
            self.dy = (self.dy / current_speed) * self.base_speed
    
    def bounce_off_paddle(self, paddle):
        # パドルのどの位置に当たったかを計算
        relative_intersect_x = (paddle.x + (paddle.width / 2)) - self.x
        normalized_relative_intersect = relative_intersect_x / (paddle.width / 2)
        
        # 反射角度を計算（-60度から60度の範囲）
        bounce_angle = normalized_relative_intersect * 60
        
        # 角度から速度ベクトルを計算
        self.dx = -self.base_speed * math.sin(math.radians(bounce_angle))
        self.dy = -self.base_speed * math.cos(math.radians(bounce_angle))
    
    def bounce_off_block(self):
        # ブロックに当たった時の反射（Y軸方向のみ反転）
        self.dy *= -2
        # 速度の大きさを一定に保つ
        self.normalize_speed()
    
    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.size // 2) 