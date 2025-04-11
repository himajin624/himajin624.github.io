# -*- coding:utf-8 -*-
import sys
import pygame
from pygame.locals import *

# 画面サイズ
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# パドルの設定
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
PADDLE_SPEED = 7

# ボールの設定
BALL_SIZE = 10
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

# ブロックの設定
BLOCK_WIDTH = 80
BLOCK_HEIGHT = 30
BLOCK_ROWS = 5
BLOCK_COLS = 10
BLOCK_PADDING = 5

class BlockBreaker:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("ブロック崩し")
        self.clock = pygame.time.Clock()
        
        # パドルの初期位置
        self.paddle_x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
        self.paddle_y = SCREEN_HEIGHT - PADDLE_HEIGHT - 10
        
        # ボールの初期位置
        self.ball_x = SCREEN_WIDTH // 2
        self.ball_y = SCREEN_HEIGHT // 2
        self.ball_dx = BALL_SPEED_X
        self.ball_dy = BALL_SPEED_Y
        
        # ブロックの初期化
        self.blocks = []
        self.init_blocks()
        
    def init_blocks(self):
        for row in range(BLOCK_ROWS):
            for col in range(BLOCK_COLS):
                x = col * (BLOCK_WIDTH + BLOCK_PADDING) + BLOCK_PADDING
                y = row * (BLOCK_HEIGHT + BLOCK_PADDING) + BLOCK_PADDING
                self.blocks.append(pygame.Rect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        # キー入力処理
        keys = pygame.key.get_pressed()
        if (keys[K_LEFT] or keys[K_a]) and self.paddle_x > 0:
            self.paddle_x -= PADDLE_SPEED
        if (keys[K_RIGHT] or keys[K_d]) and self.paddle_x < SCREEN_WIDTH - PADDLE_WIDTH:
            self.paddle_x += PADDLE_SPEED
    
    def update(self):
        # ボールの移動
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy
        
        # 壁との衝突判定
        if self.ball_x <= 0 or self.ball_x >= SCREEN_WIDTH - BALL_SIZE:
            self.ball_dx *= -1
        if self.ball_y <= 0:
            self.ball_dy *= -1
        
        # パドルとの衝突判定
        paddle_rect = pygame.Rect(self.paddle_x, self.paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT)
        ball_rect = pygame.Rect(self.ball_x, self.ball_y, BALL_SIZE, BALL_SIZE)
        if ball_rect.colliderect(paddle_rect):
            self.ball_dy *= -1
        
        # ブロックとの衝突判定
        for block in self.blocks[:]:
            if ball_rect.colliderect(block):
                self.blocks.remove(block)
                self.ball_dy *= -1
                break
        
        # ゲームオーバー判定
        if self.ball_y >= SCREEN_HEIGHT:
            self.reset_game()
    
    def reset_game(self):
        self.ball_x = SCREEN_WIDTH // 2
        self.ball_y = SCREEN_HEIGHT // 2
        self.ball_dx = BALL_SPEED_X
        self.ball_dy = BALL_SPEED_Y
        self.paddle_x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
        self.blocks.clear()
        self.init_blocks()
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # パドルの描画
        pygame.draw.rect(self.screen, BLUE, (self.paddle_x, self.paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
        
        # ボールの描画
        pygame.draw.circle(self.screen, WHITE, (int(self.ball_x), int(self.ball_y)), BALL_SIZE)
        
        # ブロックの描画
        for block in self.blocks:
            pygame.draw.rect(self.screen, RED, block)
        
        pygame.display.flip()
    
    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

if __name__ == "__main__":
    game = BlockBreaker()
    game.run() 