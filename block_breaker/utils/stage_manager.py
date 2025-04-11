# -*- coding:utf-8 -*-
from .constants import *

class StageManager:
    def __init__(self):
        self.current_stage = 1
        self.max_stage = 10
        self.stage_cleared = False
        
        # 難易度調整の設定
        self.difficulty_settings = {
            'increase_ball_speed': True,  # ボールの速度を上げる
            'decrease_paddle_width': False,  # パドルの幅を小さくする（現在は無効）
            'increase_block_rows': True,  # ブロックの行数を増やす
            'increase_block_cols': True   # ブロックの列数を増やす
        }
    
    def get_stage_params(self):
        """現在のステージに応じたパラメータを返す"""
        # 基本パラメータ
        params = {
            'block_rows': BLOCK_ROWS,
            'block_cols': BLOCK_COLS,
            'block_width': BLOCK_WIDTH,
            'block_height': BLOCK_HEIGHT,
            'block_padding': BLOCK_PADDING,
            'ball_speed_x': BALL_SPEED_X,
            'ball_speed_y': BALL_SPEED_Y,
            'paddle_speed': PADDLE_SPEED,
            'paddle_width': PADDLE_WIDTH
        }
        
        # ステージごとに難易度を調整
        if self.current_stage > 1:
            # ステージ2以降は徐々に難しくなる
            speed_increase = 0.2 * (self.current_stage - 1)  # 速度増加率
            paddle_decrease = 5 * (self.current_stage - 1)   # パドル幅減少
            
            # ボールの速度を上げる（設定が有効な場合）
            if self.difficulty_settings['increase_ball_speed']:
                params['ball_speed_x'] = BALL_SPEED_X * (1 + speed_increase)
                params['ball_speed_y'] = BALL_SPEED_Y * (1 + speed_increase)
            
            # パドルの幅を小さくする（設定が有効な場合）
            if self.difficulty_settings['decrease_paddle_width']:
                params['paddle_width'] = max(50, PADDLE_WIDTH - paddle_decrease)
            
            # ステージ3以降はブロックの行数を増やす（設定が有効な場合）
            if self.current_stage >= 3 and self.difficulty_settings['increase_block_rows']:
                params['block_rows'] = BLOCK_ROWS + (self.current_stage - 2)
            
            # ステージ5以降はブロックの列数も増やす（設定が有効な場合）
            if self.current_stage >= 5 and self.difficulty_settings['increase_block_cols']:
                params['block_cols'] = BLOCK_COLS + (self.current_stage - 4)
        
        return params
    
    def next_stage(self):
        """次のステージに進む"""
        if self.current_stage < self.max_stage:
            self.current_stage += 1
            self.stage_cleared = False
            return True
        return False
    
    def reset_stage(self):
        """現在のステージをリセット"""
        self.stage_cleared = False
    
    def clear_stage(self):
        """現在のステージをクリア"""
        self.stage_cleared = True
    
    def toggle_difficulty_setting(self, setting_name):
        """難易度設定の有効/無効を切り替える"""
        if setting_name in self.difficulty_settings:
            self.difficulty_settings[setting_name] = not self.difficulty_settings[setting_name]
            return True
        return False

    def get_stage_blocks(self):
        """現在のステージのブロックを生成"""
        from ..sprites.block import Block
        blocks = []
        params = self.get_stage_params()
        
        # ブロック全体の幅を計算
        total_block_width = (params['block_width'] + params['block_padding']) * params['block_cols'] - params['block_padding']
        
        # 左右対称になるように左側のオフセットを計算
        block_offset_x = (SCREEN_WIDTH - total_block_width) / 2
        
        # ブロックを配置
        for row in range(params['block_rows']):
            for col in range(params['block_cols']):
                x = block_offset_x + col * (params['block_width'] + params['block_padding'])
                y = BLOCK_OFFSET_Y + row * (params['block_height'] + params['block_padding'])
                blocks.append(Block(x, y))
        
        return blocks 