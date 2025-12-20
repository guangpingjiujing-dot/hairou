"""
弓使いキャラクターの実装（クラス版）
基底クラスCharacterを継承し、弓使い特有の機能を追加しています。
"""

import random
from character import Character


class Archer(Character):
    """弓使いクラス"""
    
    def __init__(self, name, hp=80, attack_power=25, accuracy=0.8):
        """
        弓使いを初期化
        
        Args:
            name: 弓使いの名前
            hp: ヒットポイント（デフォルト: 80）
            attack_power: 攻撃力（デフォルト: 25）
            accuracy: 命中率（0.0〜1.0、デフォルト: 0.8）
        """
        super().__init__(name, hp, attack_power)
        self.accuracy = accuracy
        self.character_type = "archer"
    
    def attack(self, target):
        """
        攻撃する（オーバーライド）
        命中率に基づいて攻撃が当たるか判定します。
        
        Args:
            target: 攻撃対象のキャラクター
        
        Returns:
            与えたダメージ量（外れた場合は0）
        """
        if random.random() < self.accuracy:
            damage = self.attack_power
            print(f"{self.name}が{target.name}に{damage}のダメージを与えた！")
            target.take_damage(damage)
            return damage
        else:
            print(f"{self.name}の攻撃が外れた！")
            return 0
    
    def get_status(self):
        """弓使いのステータスを取得（オーバーライド）"""
        return f"{self.name} (弓使い) - HP: {self.hp}/{self.max_hp}, 攻撃力: {self.attack_power}, 命中率: {self.accuracy*100:.1f}%"
    
    def defend(self):
        """弓使いの防御（オーバーライド）"""
        print(f"{self.name}は防御の構えを取った！")
        return self.attack_power * 0.4  # 防御力は攻撃力の40%

