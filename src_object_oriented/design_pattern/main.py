"""
クラス版のメインプログラム
クラスを使うことで、同じような処理を繰り返し書く必要がなくなり、
コードがシンプルで保守しやすくなりました。
"""

from warrior import Warrior
from mage import Mage
from archer import Archer


def main():
    print("=== クラス版：ゲームキャラクターの戦闘 ===\n")
    
    # キャラクターを作成（すべて同じようにインスタンス化できる）
    warrior = Warrior("アレックス", hp=100, attack_power=30)
    mage = Mage("ルナ", hp=60, attack_power=15, magic_power=40)
    archer = Archer("ロビン", hp=80, attack_power=25, accuracy=0.8)
    
    # ステータス表示（すべて同じメソッドを使える）
    print("【キャラクター作成】")
    print(warrior.get_status())
    print(mage.get_status())
    print(archer.get_status())
    print()
    
    # 戦闘シーン
    print("【戦闘開始】")
    print("-" * 50)
    
    # 戦士が魔法使いを攻撃
    warrior.attack(mage)
    print(mage.get_status())
    print()
    
    # 魔法使いが戦士に魔法を唱える
    mage.cast_magic(warrior)
    print(warrior.get_status())
    print()
    
    # 弓使いが戦士を攻撃
    archer.attack(warrior)
    print(warrior.get_status())
    print()
    
    # 戦士が弓使いを攻撃
    warrior.attack(archer)
    print(archer.get_status())
    print()
    
    print("【戦闘終了】")
    print("-" * 50)
    
    # 生存確認（すべて同じメソッドを使える）
    print("【生存状況】")
    characters = [warrior, mage, archer]
    for char in characters:
        status = "生存" if char.is_alive() else "戦闘不能"
        print(f"{char.name}: {status}")


if __name__ == "__main__":
    main()

