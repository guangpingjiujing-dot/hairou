"""
アンチパターン版のメインプログラム
各キャラクタータイプごとに別々のモジュールを使っているため、
同じような処理を繰り返し書く必要があります。
"""

from warrior import create_warrior, warrior_attack, warrior_take_damage, warrior_is_alive, warrior_get_status
from mage import create_mage, mage_attack, mage_cast_magic, mage_take_damage, mage_is_alive, mage_get_status
from archer import create_archer, archer_attack, archer_take_damage, archer_is_alive, archer_get_status


def main():
    print("=== アンチパターン版：ゲームキャラクターの戦闘 ===\n")
    
    # キャラクターを作成（各タイプごとに異なる関数を使う必要がある）
    warrior = create_warrior("アレックス", hp=100, attack_power=30)
    mage = create_mage("ルナ", hp=60, attack_power=15, magic_power=40)
    archer = create_archer("ロビン", hp=80, attack_power=25, accuracy=0.8)
    
    # ステータス表示（各タイプごとに異なる関数を使う必要がある）
    print("【キャラクター作成】")
    print(warrior_get_status(warrior))
    print(mage_get_status(mage))
    print(archer_get_status(archer))
    print()
    
    # 戦闘シーン
    print("【戦闘開始】")
    print("-" * 50)
    
    # 戦士が魔法使いを攻撃
    warrior_attack(warrior, mage)
    print(mage_get_status(mage))
    print()
    
    # 魔法使いが戦士に魔法を唱える
    mage_cast_magic(mage, warrior)
    print(warrior_get_status(warrior))
    print()
    
    # 弓使いが戦士を攻撃
    archer_attack(archer, warrior)
    print(warrior_get_status(warrior))
    print()
    
    # 戦士が弓使いを攻撃
    warrior_attack(warrior, archer)
    print(archer_get_status(archer))
    print()
    
    print("【戦闘終了】")
    print("-" * 50)
    
    # 生存確認（各タイプごとに異なる関数を使う必要がある）
    print("【生存状況】")
    print(f"{warrior['name']}: {'生存' if warrior_is_alive(warrior) else '戦闘不能'}")
    print(f"{mage['name']}: {'生存' if mage_is_alive(mage) else '戦闘不能'}")
    print(f"{archer['name']}: {'生存' if archer_is_alive(archer) else '戦闘不能'}")


if __name__ == "__main__":
    main()

