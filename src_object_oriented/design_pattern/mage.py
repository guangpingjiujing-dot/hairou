"""
魔法使いキャラクターの実装（クラス版）
基底クラスCharacterを継承し、魔法使い特有の機能を追加しています。
"""

from character import Character


class Mage(Character):
    """魔法使いクラス"""
    
    def __init__(self, name, hp=60, attack_power=15, magic_power=40):
        """
        魔法使いを初期化
        
        Args:
            name: 魔法使いの名前
            hp: ヒットポイント（デフォルト: 60）
            attack_power: 攻撃力（デフォルト: 15）
            magic_power: 魔力（デフォルト: 40）
        """
        super().__init__(name, hp, attack_power)
        self.magic_power = magic_power
        self.character_type = "mage"
    
    def cast_magic(self, target):
        """
        魔法を唱える（魔法使い特有のメソッド）
        
        Args:
            target: 攻撃対象のキャラクター
        
        Returns:
            与えたダメージ量
        """
        damage = self.magic_power
        print(f"{self.name}が魔法を唱えた！{target.name}に{damage}のダメージを与えた！")
        target.take_damage(damage)
        return damage
    
    def get_status(self):
        """魔法使いのステータスを取得（オーバーライド）"""
        return f"{self.name} (魔法使い) - HP: {self.hp}/{self.max_hp}, 攻撃力: {self.attack_power}, 魔力: {self.magic_power}"
    
    def defend(self):
        """魔法使いの防御（オーバーライド）"""
        print(f"{self.name}は防御の構えを取った！")
        return self.attack_power * 0.3  

