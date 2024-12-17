from collections.abc import Generator
from dataclasses import dataclass
from enum import IntEnum
from enum import unique
from itertools import combinations
from typing import Self


@unique
class ItemType(IntEnum):
    WEAPON = 0
    ARMOR = 1
    RING = 2


@dataclass(frozen=True)
class Item:
    name: str
    type: ItemType
    cost: int
    damage: int = 0
    armor: int = 0

    @classmethod
    def make_weapon(cls, name: str, *, cost: int, damage: int) -> Self:
        return cls(name, ItemType.WEAPON, cost, damage, 0)

    @classmethod
    def make_armor(cls, name: str, *, cost: int, armor: int) -> Self:
        return cls(name, ItemType.ARMOR, cost, 0, armor)

    @classmethod
    def make_ring(cls, name: str, *, cost: int, damage: int, armor: int) -> Self:
        return cls(name, ItemType.RING, cost, damage, armor)


@dataclass
class Player:
    name: str
    hitpoints: int
    damage: int
    armor: int

    @classmethod
    def make_player(
        cls, name: str, *, hitpoints: int, base_damage: int, base_armor: int, items: list[Item] | None = None
    ) -> Self:
        player = cls(name, hitpoints, base_damage, base_armor)
        if items:
            for item in items:
                player.damage += item.damage
                player.armor += item.armor
        return player

    def hit(self, target: Self) -> None:
        damage = max(self.damage - target.armor, 1)
        target.hitpoints -= damage


def load_shop() -> dict[ItemType, list[Item]]:
    return {
        ItemType.WEAPON: [
            Item.make_weapon("Dagger", cost=8, damage=4),
            Item.make_weapon("Shortsword", cost=10, damage=5),
            Item.make_weapon("Warhammer", cost=25, damage=6),
            Item.make_weapon("Longsword", cost=40, damage=7),
            Item.make_weapon("Greataxe", cost=74, damage=8),
        ],
        ItemType.ARMOR: [
            Item.make_armor("Leather", cost=13, armor=1),
            Item.make_armor("Chainmail", cost=31, armor=2),
            Item.make_armor("Splintmail", cost=53, armor=3),
            Item.make_armor("Bandedmail", cost=75, armor=4),
            Item.make_armor("Platemail", cost=102, armor=5),
        ],
        ItemType.RING: [
            Item.make_ring("Damage +1", cost=25, damage=1, armor=0),
            Item.make_ring("Damage +2", cost=50, damage=2, armor=0),
            Item.make_ring("Damage +3", cost=100, damage=3, armor=0),
            Item.make_ring("Defense +1", cost=20, damage=0, armor=1),
            Item.make_ring("Defense +2", cost=40, damage=0, armor=2),
            Item.make_ring("Defense +3", cost=80, damage=0, armor=3),
        ],
    }


def fight(player: Player, boss: Player) -> bool:
    while player.hitpoints > 0:
        player.hit(boss)
        if boss.hitpoints <= 0:
            return True
        boss.hit(player)

    return False


def generate_item_combinations(shop: dict[ItemType, list[Item]]) -> Generator[list[Item], None, None]:
    weapons = shop[ItemType.WEAPON]
    armor = shop[ItemType.ARMOR]
    rings = shop[ItemType.RING]

    # generate all possible combinations of items
    for weapon in weapons:
        for arm in [None] + list(armor):  # no armor or one armor
            for ring_combo in combinations(rings, 2):  # two rings
                yield [weapon] + ([arm] if arm else []) + list(ring_combo)
            for ring in rings:  # one ring
                yield [weapon] + ([arm] if arm else []) + [ring]
            yield [weapon] + ([arm] if arm else [])  # no rings


def find_minimum_gold_to_win(boss: Player, shop: dict[ItemType, list[Item]]) -> int:
    min_gold = 1_000_000_000
    for items in generate_item_combinations(shop):
        total_cost = sum(item.cost for item in items)
        player = Player.make_player("Hero", hitpoints=100, base_damage=0, base_armor=0, items=items)
        if fight(player, Player("Boss", boss.hitpoints, boss.damage, boss.armor)):
            min_gold = min(min_gold, total_cost)
    return min_gold


def find_maximum_gold_to_lose(boss: Player, shop: dict[ItemType, list[Item]]) -> int:
    max_gold = 0
    for items in generate_item_combinations(shop):
        total_cost = sum(item.cost for item in items)
        player = Player.make_player("Hero", hitpoints=100, base_damage=0, base_armor=0, items=items)
        if not fight(player, Player("Boss", boss.hitpoints, boss.damage, boss.armor)):
            max_gold = max(max_gold, total_cost)
    return max_gold


def main() -> None:
    shop = load_shop()

    boss = Player.make_player("Boss", hitpoints=103, base_damage=9, base_armor=2)
    minimum_cost = find_minimum_gold_to_win(boss, shop)
    print(f"The least amount of gold to win the fight is: {minimum_cost}")

    maximum_cost = find_maximum_gold_to_lose(boss, shop)
    print(f"The most amount of gold you can spend and still lose is: {maximum_cost}")


if __name__ == "__main__":
    main()
