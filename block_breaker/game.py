# -*- coding:utf-8 -*-
import sys
import pygame
import os
from pygame.locals import *
from .utils.constants import *
from .sprites import Paddle, Ball, Block
from .utils.stage_manager import StageManager
from .utils.shop import Shop
import math

class BlockBreaker:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("ブロック崩し")
        self.clock = pygame.time.Clock()
        
        # 日本語フォントの設定
        # Windowsの場合、MS GothicやYu Gothicなどの日本語フォントを使用
        try:
            self.font = pygame.font.SysFont("yugothic", 36)
            self.small_font = pygame.font.SysFont("yugothic", 24)
        except:
            # フォールバック
            self.font = pygame.font.SysFont("msgothic", 36)
            self.small_font = pygame.font.SysFont("msgothic", 24)
        
        # ステージマネージャーの初期化
        self.stage_manager = StageManager()
        
        # ショップの初期化
        self.shop = Shop(self)
        
        # ゲームの初期化
        self.init_game()
        
        # コイン獲得数
        self.coins_per_block = 10
    
    def init_game(self):
        """ゲームの初期化"""
        # パドルの初期化
        self.paddle = Paddle(SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, SCREEN_HEIGHT - 50)
        
        # ボールの初期化
        self.ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        
        # ブロックの初期化
        self.blocks = self.stage_manager.get_stage_blocks()
        
        # 衝突フラグをリセット
        self.collision_occurred = False
    
    def handle_events(self):
        """イベントの処理"""
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == KEYDOWN:
                if event.key == K_1:
                    self.stage_manager.toggle_difficulty_setting('increase_ball_speed')
                elif event.key == K_2:
                    self.stage_manager.toggle_difficulty_setting('decrease_paddle_width')
                elif event.key == K_3:
                    self.stage_manager.toggle_difficulty_setting('increase_block_rows')
                elif event.key == K_4:
                    self.stage_manager.toggle_difficulty_setting('increase_block_columns')
                elif event.key == K_RETURN and self.shop.visible:
                    self.shop.purchase_item()
                elif event.key == K_ESCAPE and self.shop.visible:
                    self.shop.hide()
            
            if event.type == MOUSEBUTTONDOWN and self.shop.visible:
                self.shop.handle_click(event.pos)
    
    def update(self):
        """ゲームの状態を更新"""
        #if self.shop.visible:
        #    return
        
        # 衝突フラグをリセット
        self.collision_occurred = False
        
        # パドルの更新
        self.paddle.update()
        
        # ボールの更新
        self.ball.update()
        
        # パドルとの衝突判定
        if not self.collision_occurred and self.ball.rect.colliderect(self.paddle.rect):
            self.ball.bounce_off_paddle(self.paddle)
            self.collision_occurred = True
        
        # ブロックとの衝突判定
        for block in self.blocks[:]:
            if not self.collision_occurred and self.ball.rect.colliderect(block.rect):
                self.ball.bounce_off_block()
                self.blocks.remove(block)
                self.collision_occurred = True
                # コインを追加
                self.shop.add_coins(self.coins_per_block)
                break
        
        # ゲームオーバー判定
        if self.ball.y >= SCREEN_HEIGHT:
            self.reset_game()
        
        # ステージクリア判定
        if len(self.blocks) == 0:
            self.stage_manager.stage_cleared = True
            print("ステージクリア！")  # 追加
            # ステージクリア時にショップを表示
            self.shop.show()
            
            # 最終ステージの場合はゲームクリア
            if self.stage_manager.current_stage == self.stage_manager.max_stage:
                print("最終ステージ！")  # 追加
                self.game_clear()
            else:
                # 次のステージへ
                self.stage_manager.next_stage()
    
    def reset_game(self):
        """ゲームをリセット"""
        print("reset_game メソッドが呼び出されました")  # 追加
        # ステージパラメータの取得
        params = self.stage_manager.get_stage_params()
        
        # パドルとボールの位置をリセット
        self.paddle.x = SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2
        self.paddle.rect.x = self.paddle.x
        self.ball.x = SCREEN_WIDTH // 2
        self.ball.y = SCREEN_HEIGHT - 70  # パドルにより近い位置に調整
        self.ball.speed_x = params['ball_speed_x']
        self.ball.speed_y = params['ball_speed_y']
        self.ball.base_speed = math.sqrt(params['ball_speed_x'] ** 2 + params['ball_speed_y'] ** 2)
        
        # ブロックを再生成
        self.blocks = self.stage_manager.get_stage_blocks()
    
    def game_clear(self):
        """全ステージクリア"""
        print("game_clear メソッドが呼び出されました")  # 追加
        # ここにゲームクリア時の処理を追加
        print("おめでとう！全ステージクリア！")
        # ゲームを終了
        pygame.quit()
        sys.exit()
    
    def draw(self):
        """ゲーム画面の描画"""
        self.screen.fill(BLACK)
        
        # パドルの描画
        self.paddle.draw(self.screen)
        
        # ボールの描画
        self.ball.draw(self.screen)
        
        # ブロックの描画
        for block in self.blocks:
            block.draw(self.screen)
        
        # ステージ情報の表示
        stage_text = self.font.render(f"ステージ: {self.stage_manager.current_stage}", True, WHITE)
        self.screen.blit(stage_text, (10, 10))
        
        # コイン情報の表示
        coin_text = self.font.render(f"コイン: {self.shop.coins}", True, YELLOW)
        self.screen.blit(coin_text, (10, 50))
        
        # 難易度設定の表示
        y_pos = 90
        for setting, enabled in self.stage_manager.difficulty_settings.items():
            color = GREEN if enabled else RED
            setting_text = self.small_font.render(f"{setting}: {'ON' if enabled else 'OFF'}", True, color)
            self.screen.blit(setting_text, (10, y_pos))
            y_pos += 25
        
        # ショップの描画
        self.shop.draw(self.screen)
        
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