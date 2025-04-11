# -*- coding:utf-8 -*-
import sys
import pygame
import os
from .constants import *

class Item:
    def __init__(self, name, description, cost, effect_type, effect_value):
        self.name = name
        self.description = description
        self.cost = cost
        self.effect_type = effect_type  # 'paddle_width', 'ball_speed', 'paddle_speed'
        self.effect_value = effect_value
        self.rect = pygame.Rect(0, 0, 200, 80)  # アイテムの表示領域
    
    def apply_effect(self, game):
        """アイテムの効果をゲームに適用"""
        if self.effect_type == 'paddle_width':
            # パドルの幅を変更（最小値は50、最大値は200）
            new_width = max(50, min(200, game.paddle.width + self.effect_value))
            game.paddle.width = new_width
            game.paddle.rect.width = new_width
        elif self.effect_type == 'ball_speed':
            # ボールの速度を変更
            game.ball.base_speed += self.effect_value
            game.ball.normalize_speed()
        elif self.effect_type == 'paddle_speed':
            # パドルの速度を変更
            game.paddle.speed += self.effect_value

class Shop:
    def __init__(self, game):
        self.game = game
        self.visible = False
        self.items = []
        self.selected_item = None
        self.coins = 0
        
        # 日本語フォントの設定
        # Windowsの場合、MS GothicやYu Gothicなどの日本語フォントを使用
        try:
            self.title_font = pygame.font.SysFont("yugothic", 48)
            self.item_font = pygame.font.SysFont("yugothic", 24)
            self.help_font = pygame.font.SysFont("yugothic", 20)
        except:
            # フォールバック
            self.title_font = pygame.font.SysFont("msgothic", 48)
            self.item_font = pygame.font.SysFont("msgothic", 24)
            self.help_font = pygame.font.SysFont("msgothic", 20)
        
        self.init_items()
    
    def init_items(self):
        """ショップのアイテムを初期化"""
        self.items = [
            Item("パドル拡大", "パドルの幅を10増やす", 100, 'paddle_width', 10),
            Item("パドル縮小", "パドルの幅を10減らす", 50, 'paddle_width', -10),
            Item("ボール加速", "ボールの速度を0.5増やす", 150, 'ball_speed', 0.5),
            Item("パドル加速", "パドルの移動速度を1増やす", 100, 'paddle_speed', 1),
        ]
    
    def show(self):
        """ショップを表示"""
        self.visible = True
        # アイテムの位置を設定
        for i, item in enumerate(self.items):
            item.rect.x = SCREEN_WIDTH // 2 - 100
            item.rect.y = 200 + i * 100
    
    def hide(self):
        """ショップを非表示"""
        self.visible = False
        self.selected_item = None
        # ステージクリアフラグをリセット
        self.game.stage_manager.stage_cleared = False
        self.game.reset_game()    
    def handle_click(self, pos):
        """マウスクリックの処理"""
        if not self.visible:
            return
        
        for item in self.items:
            if item.rect.collidepoint(pos):
                self.selected_item = item
                break
    
    def purchase_item(self):
        """選択したアイテムを購入"""
        if not self.visible or not self.selected_item:
            return
        
        if self.coins >= self.selected_item.cost:
            self.coins -= self.selected_item.cost
            self.selected_item.apply_effect(self.game)
            self.selected_item = None
    
    def add_coins(self, amount):
        """コインを追加"""
        self.coins += amount
    
    def draw(self, screen):
        """ショップを描画"""
        if not self.visible:
            return
        
        # 半透明の背景
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))
        
        # ショップのタイトル
        title = self.title_font.render("ショップ", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))
        
        # コインの表示
        coin_text = self.title_font.render(f"コイン: {self.coins}", True, YELLOW)
        screen.blit(coin_text, (SCREEN_WIDTH // 2 - coin_text.get_width() // 2, 100))
        
        # アイテムの表示
        for i, item in enumerate(self.items):
            # アイテムの背景
            color = (100, 100, 100) if item == self.selected_item else (50, 50, 50)
            pygame.draw.rect(screen, color, item.rect)
            pygame.draw.rect(screen, WHITE, item.rect, 2)
            
            # アイテム名
            name_text = self.item_font.render(item.name, True, WHITE)
            screen.blit(name_text, (item.rect.x + 10, item.rect.y + 10))
            
            # アイテムの説明
            desc_text = self.item_font.render(item.description, True, WHITE)
            screen.blit(desc_text, (item.rect.x + 10, item.rect.y + 30))
            
            # アイテムの価格
            cost_text = self.item_font.render(f"価格: {item.cost} コイン", True, YELLOW)
            screen.blit(cost_text, (item.rect.x + 10, item.rect.y + 50))
        
        # 操作説明
        help_text = self.help_font.render("クリック: アイテム選択 / Enter: 購入 / ESC: 閉じる", True, WHITE)
        screen.blit(help_text, (SCREEN_WIDTH // 2 - help_text.get_width() // 2, SCREEN_HEIGHT - 50))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and self.shop.visible:
                    self.shop.hide()