"""
弓使いキャラクターの実装（アンチパターン版）
各キャラクターごとに別々のモジュールで実装しているため、コードが冗長になっています。
"""

def create_archer(name, hp, attack_power, accuracy):
    """弓使いを作成する"""
    return {
        "name": name,
        "hp": hp,
        "max_hp": hp,
        "attack_power": attack_power,
        "accuracy": accuracy,
        "character_type": "archer"
    }


def archer_attack(archer, target):
    """弓使いが攻撃する"""
    import random
    # 命中率に基づいて攻撃が当たるか判定
    if random.random() < archer["accuracy"]:
        damage = archer["attack_power"]
        print(f"{archer['name']}が{target['name']}に{damage}のダメージを与えた！")
        target["hp"] -= damage
        if target["hp"] < 0:
            target["hp"] = 0
        return damage
    else:
        print(f"{archer['name']}の攻撃が外れた！")
        return 0


def archer_defend(archer):
    """弓使いが防御する"""
    print(f"{archer['name']}は防御の構えを取った！")
    return archer["attack_power"] * 0.4  # 防御力は攻撃力の40%


def archer_take_damage(archer, damage):
    """弓使いがダメージを受ける"""
    archer["hp"] -= damage
    if archer["hp"] < 0:
        archer["hp"] = 0
    print(f"{archer['name']}は{damage}のダメージを受けた！残りHP: {archer['hp']}")
    return archer["hp"] > 0


def archer_is_alive(archer):
    """弓使いが生きているかチェック"""
    return archer["hp"] > 0


def archer_get_status(archer):
    """弓使いのステータスを取得"""
    return f"{archer['name']} (弓使い) - HP: {archer['hp']}/{archer['max_hp']}, 攻撃力: {archer['attack_power']}, 命中率: {archer['accuracy']*100:.1f}%"

