"""
戦士キャラクターの実装（アンチパターン版）
各キャラクターごとに別々のモジュールで実装しているため、コードが冗長になっています。
"""

def create_warrior(name, hp, attack_power):
    """戦士を作成する"""
    return {
        "name": name,
        "hp": hp,
        "max_hp": hp,
        "attack_power": attack_power,
        "character_type": "warrior"
    }


def warrior_attack(warrior, target):
    """戦士が攻撃する"""
    damage = warrior["attack_power"]
    print(f"{warrior['name']}が{target['name']}に{damage}のダメージを与えた！")
    target["hp"] -= damage
    if target["hp"] < 0:
        target["hp"] = 0
    return damage


def warrior_defend(warrior):
    """戦士が防御する"""
    print(f"{warrior['name']}は防御の構えを取った！")
    return warrior["attack_power"] * 0.5  # 防御力は攻撃力の半分


def warrior_take_damage(warrior, damage):
    """戦士がダメージを受ける"""
    warrior["hp"] -= damage
    if warrior["hp"] < 0:
        warrior["hp"] = 0
    print(f"{warrior['name']}は{damage}のダメージを受けた！残りHP: {warrior['hp']}")
    return warrior["hp"] > 0


def warrior_is_alive(warrior):
    """戦士が生きているかチェック"""
    return warrior["hp"] > 0


def warrior_get_status(warrior):
    """戦士のステータスを取得"""
    return f"{warrior['name']} (戦士) - HP: {warrior['hp']}/{warrior['max_hp']}, 攻撃力: {warrior['attack_power']}"

