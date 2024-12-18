from dataclasses import dataclass
from typing import List
from typing import Optional


@dataclass
class Spell:
    name: str
    cost: int
    duration: int = 0
    damage: int = 0
    healing: int = 0
    armor: int = 0
    mana: int = 0


@dataclass
class Player:
    hitpoints: int
    mana: int
    damage: int = 0
    armor: int = 0


@dataclass
class Effect:
    spell: Spell
    remaining_turns: int


def load_spells() -> List[Spell]:
    return [
        Spell("Magic Missile", 53, damage=4),
        Spell("Drain", 73, damage=2, healing=2),
        Spell("Shield", 113, duration=6, armor=7),
        Spell("Poison", 173, duration=6, damage=3),
        Spell("Recharge", 229, duration=5, mana=101),
    ]


def apply_effects(player: Player, boss: Player, effects: List[Effect]) -> None:
    player.armor = 0
    expired_effects = []

    for effect in effects:
        if effect.spell.armor > 0:
            player.armor = effect.spell.armor
        if effect.spell.damage > 0:
            boss.hitpoints -= effect.spell.damage
        if effect.spell.mana > 0:
            player.mana += effect.spell.mana

        effect.remaining_turns -= 1
        if effect.remaining_turns <= 0:
            expired_effects.append(effect)

    for effect in expired_effects:
        effects.remove(effect)


def simulate_turn(
    player: Player, boss: Player, spell: Spell, effects: List[Effect], mana_spent: int, hard_mode: bool
) -> Optional[int]:
    if hard_mode:
        player.hitpoints -= 1
        if player.hitpoints <= 0:
            return None

    # Player's turn: Apply effects and cast spell
    apply_effects(player, boss, effects)

    if boss.hitpoints <= 0:
        return mana_spent

    if spell.cost > player.mana:
        return None

    player.mana -= spell.cost
    mana_spent += spell.cost

    if spell.duration > 0:
        for effect in effects:
            if effect.spell.name == spell.name:
                return None
        effects.append(Effect(spell, spell.duration))
    else:
        boss.hitpoints -= spell.damage
        player.hitpoints += spell.healing

    if boss.hitpoints <= 0:
        return mana_spent

    # Boss's turn: Apply effects and attack
    apply_effects(player, boss, effects)

    if boss.hitpoints <= 0:
        return mana_spent

    damage = max(1, boss.damage - player.armor)
    player.hitpoints -= damage

    if player.hitpoints <= 0:
        return None

    return mana_spent


def find_least_mana_to_win(player: Player, boss: Player, spells: List[Spell], *, hard_mode: bool) -> int:
    min_mana = 1_000_000_000

    def dfs(player: Player, boss: Player, effects: List[Effect], mana_spent: int) -> None:
        nonlocal min_mana

        if mana_spent >= min_mana:
            return

        for spell in spells:
            new_player = Player(player.hitpoints, player.mana, player.damage, player.armor)
            new_boss = Player(boss.hitpoints, boss.mana, boss.damage, boss.armor)
            new_effects = [Effect(effect.spell, effect.remaining_turns) for effect in effects]

            result = simulate_turn(new_player, new_boss, spell, new_effects, mana_spent, hard_mode)

            if result is not None:
                if new_boss.hitpoints <= 0:
                    min_mana = min(min_mana, result)
                else:
                    dfs(new_player, new_boss, new_effects, result)

    dfs(player, boss, [], 0)

    return min_mana


def main() -> None:
    spells = load_spells()
    player = Player(hitpoints=50, mana=500)
    boss = Player(hitpoints=58, mana=0, damage=9)

    least_mana = find_least_mana_to_win(player, boss, spells, hard_mode=False)
    print(f"The least amount of mana to win the fight is: {least_mana}")

    least_mana = find_least_mana_to_win(player, boss, spells, hard_mode=True)
    print(f"The least amount of mana to win the fight in hard mode is: {least_mana}")


if __name__ == "__main__":
    main()
