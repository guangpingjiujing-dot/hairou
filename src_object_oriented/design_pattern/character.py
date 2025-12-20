"""
キャラクターの基底クラス
共通の機能をここに定義することで、コードの重複を避けられます。
"""


class Character:
    """ゲームキャラクターの基底クラス"""
    
    def __init__(self, name, hp, attack_power):
        """
        キャラクターを初期化
        
        Args:
            name: キャラクター名
            hp: ヒットポイント（体力）
            attack_power: 攻撃力
        """
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack_power = attack_power
    
    def attack(self, target):
        """
        攻撃する
        
        Args:
            target: 攻撃対象のキャラクター
        
        Returns:
            与えたダメージ量
        """
        damage = self.attack_power
        print(f"{self.name}が{target.name}に{damage}のダメージを与えた！")
        target.take_damage(damage)
        return damage
    
    def defend(self):
        """
        防御する
        
        Returns:
            防御力
        """
        print(f"{self.name}は防御の構えを取った！")
        return self.attack_power * 0.5
    
    def take_damage(self, damage):
        """
        ダメージを受ける
        
        Args:
            damage: 受けるダメージ量
        
        Returns:
            生存しているかどうか（True/False）
        """
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0
        print(f"{self.name}は{damage}のダメージを受けた！残りHP: {self.hp}")
        return self.is_alive()
    
    def is_alive(self):
        """
        生存しているかチェック
        
        Returns:
            生存している場合True、そうでなければFalse
        """
        return self.hp > 0
    
    def get_status(self):
        """
        ステータスを取得
        
        Returns:
            ステータス文字列
        """
        return f"{self.name} - HP: {self.hp}/{self.max_hp}, 攻撃力: {self.attack_power}"

