"""
戦士キャラクターの実装（クラス版）
基底クラスCharacterを継承することで、共通の機能を再利用しています。
"""

from character import Character


class Warrior(Character):
    """戦士クラス"""
    
    def __init__(self, name, hp=100, attack_power=30):
        """
        戦士を初期化
        
        Args:
            name: 戦士の名前
            hp: ヒットポイント（デフォルト: 100）
            attack_power: 攻撃力（デフォルト: 30）
        """
        super().__init__(name, hp, attack_power)
        self.character_type = "warrior"
    
    def get_status(self):
        """戦士のステータスを取得（オーバーライド）"""
        return f"{self.name} (戦士) - HP: {self.hp}/{self.max_hp}, 攻撃力: {self.attack_power}"
    
    def defend(self):
        """戦士の防御（オーバーライド）"""
        print(f"{self.name}は防御の構えを取った！")
        return self.attack_power * 0.5  # 防御力は攻撃力の半分

