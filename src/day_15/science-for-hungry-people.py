from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import List
from typing import Tuple


@dataclass(frozen=True)
class Ingredient:
    name: str
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int

    @classmethod
    def from_str(cls, record: str) -> "Ingredient":
        """
        Parse a string into an Ingredient object.
        Example:
        "Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3"
        """
        name, _, properties = record.partition(": ")
        props = {key: int(value) for key, value in (prop.split(" ") for prop in properties.split(", "))}
        return cls(
            name=name,
            capacity=props["capacity"],
            durability=props["durability"],
            flavor=props["flavor"],
            texture=props["texture"],
            calories=props["calories"],
        )


def load_ingredients(file_path: Path) -> List[Ingredient]:
    with file_path.open("r", encoding="utf-8") as file:
        return [Ingredient.from_str(record.strip()) for record in file]


def make_proportion_generator(ingredient_count: int, total_amount: int) -> Iterator[Tuple[int, ...]]:
    """
    Generate all combinations of proportions that sum to `total_amount` for `ingredient_count` ingredients.
    """
    if ingredient_count == 1:
        yield (total_amount,)
        return

    for i in range(total_amount + 1):
        for sub_combination in make_proportion_generator(ingredient_count - 1, total_amount - i):
            yield (i,) + sub_combination


def find_best_cookie_score(ingredients: List[Ingredient], teaspoons: int) -> int:
    best_score = 0
    for proportions in make_proportion_generator(len(ingredients), teaspoons):
        capacity = sum(ingredients[i].capacity * proportions[i] for i in range(len(ingredients)))
        durability = sum(ingredients[i].durability * proportions[i] for i in range(len(ingredients)))
        flavor = sum(ingredients[i].flavor * proportions[i] for i in range(len(ingredients)))
        texture = sum(ingredients[i].texture * proportions[i] for i in range(len(ingredients)))

        # Clamp negative values to zero
        capacity = max(0, capacity)
        durability = max(0, durability)
        flavor = max(0, flavor)
        texture = max(0, texture)

        # Compute the total score
        score = capacity * durability * flavor * texture
        best_score = max(best_score, score)

    return best_score


def main() -> None:
    file_path = Path("input.data")
    ingredients = load_ingredients(file_path)
    print("Ingredients:")
    print(*ingredients, sep="\n")

    teaspoons = 100
    best_cookie_score = find_best_cookie_score(ingredients, teaspoons)
    print(f"The highest cookie score is {best_cookie_score}")


if __name__ == "__main__":
    main()
