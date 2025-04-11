# -*- coding: utf-8 -*-
import pygame

# 画面サイズ
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (100, 0, 0)
GREEN = (0, 100, 0)
BLUE = (0, 0, 100)
YELLOW = (200, 200, 0)

# パドルの設定
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
PADDLE_SPEED = 7

# ボールの設定
BALL_SIZE = 10
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

# ブロックの設定
BLOCK_WIDTH = 85
BLOCK_HEIGHT = 30
BLOCK_PADDING = 5

BLOCK_ROWS = 2  # 初期値
BLOCK_COLS = 4 # 初期値

# ブロック全体の幅を計算
total_block_width = (BLOCK_WIDTH + BLOCK_PADDING) * BLOCK_COLS - BLOCK_PADDING

# 左右対称になるように BLOCK_OFFSET_X を計算
BLOCK_OFFSET_X = (SCREEN_WIDTH - total_block_width) / 2

BLOCK_OFFSET_Y = 25  # 画面上端からのオフセット

MAX_BLOCK_ROWS = 10  # ブロックの最大行数
MAX_BLOCK_COLS = 15  # ブロックの最大列数

def recalculate_block_offset_x():
    """BLOCK_OFFSET_X を再計算する"""
    global BLOCK_OFFSET_X, BLOCK_WIDTH, BLOCK_PADDING, BLOCK_COLS, SCREEN_WIDTH  # グローバル変数を明示的に指定
    total_block_width = (BLOCK_WIDTH + BLOCK_PADDING) * BLOCK_COLS - BLOCK_PADDING
    BLOCK_OFFSET_X = (SCREEN_WIDTH - total_block_width) / 2
