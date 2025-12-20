"""
魔法使いキャラクターの実装（アンチパターン版）
各キャラクターごとに別々のモジュールで実装しているため、コードが冗長になっています。
"""

def create_mage(name, hp, attack_power, magic_power):
    """魔法使いを作成する"""
    return {
        "name": name,
        "hp": hp,
        "max_hp": hp,
        "attack_power": attack_power,
        "magic_power": magic_power,
        "character_type": "mage"
    }


def mage_attack(mage, target):
    """魔法使いが攻撃する"""
    damage = mage["attack_power"]
    print(f"{mage['name']}が{target['name']}に{damage}のダメージを与えた！")
    target["hp"] -= damage
    if target["hp"] < 0:
        target["hp"] = 0
    return damage


def mage_cast_magic(mage, target):
    """魔法使いが魔法を唱える"""
    damage = mage["magic_power"]
    print(f"{mage['name']}が魔法を唱えた！{target['name']}に{damage}のダメージを与えた！")
    target["hp"] -= damage
    if target["hp"] < 0:
        target["hp"] = 0
    return damage


def mage_defend(mage):
    """魔法使いが防御する"""
    print(f"{mage['name']}は防御の構えを取った！")
    return mage["attack_power"] * 0.3  # 防御力は攻撃力の30%


def mage_take_damage(mage, damage):
    """魔法使いがダメージを受ける"""
    mage["hp"] -= damage
    if mage["hp"] < 0:
        mage["hp"] = 0
    print(f"{mage['name']}は{damage}のダメージを受けた！残りHP: {mage['hp']}")
    return mage["hp"] > 0


def mage_is_alive(mage):
    """魔法使いが生きているかチェック"""
    return mage["hp"] > 0


def mage_get_status(mage):
    """魔法使いのステータスを取得"""
    return f"{mage['name']} (魔法使い) - HP: {mage['hp']}/{mage['max_hp']}, 攻撃力: {mage['attack_power']}, 魔力: {mage['magic_power']}"

