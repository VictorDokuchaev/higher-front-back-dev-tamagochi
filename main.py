import subprocess

from game.clicker import RandomClicker
from game.exceptions import TamagochiIsGone
from game.game import ConsoleGame
from game.models import Food, Medicine
from game.tamagochi import CatTamagochi

STATUS_TEMPLATE = (
    "Статус: голод {hunger}, здоровье {hp}, "
    "энергия {energy}, монет {coins}"
)
BAGS_TEMPLATE = (
    "Сумка с едой: {food}\n"
    "Сумка с лекарствами: {medicine}"
)
SICK_MESSAGE = "\n".join(
    (
        "=======Тамагочи болеет======",
        "=======Отдых действует менее эффективно=======",
    )
)
MENU = "\n".join(
    (
        "1. Пойти на работу",
        "2. Купить еду",
        "3. Купить лекарство",
        "4. Покормить",
        "5. Вылечить",
        "6. Играть",
        "7. Отдых",
        "0. Выход",
    )
)


def main() -> None:
    """Запускает консольный цикл тамагочи-кликера"""
    all_food = [
        Food(name='Бургер', satiety=20, price=40),
        Food(name='Салат', satiety=10, price=20),
        Food(name='Яблоко', satiety=10, price=15)
    ]

    all_medicine = [
        Medicine(name='Ибупрофен', price=30, heal_hp=20, number_of_uses=2)
    ]

    tamagochi = CatTamagochi()
    clicker = RandomClicker(10, 20)
    game = ConsoleGame(
        tamagochi,
        clicker,
        all_food=all_food,
        all_medicine=all_medicine
    )

    print("Добро пожаловать в Тамагочи-кликер!")
    output = ''

    while True:
        lines = [
            output,
            BAGS_TEMPLATE.format(food=game.food, medicine=game.medicine),
            "",
            STATUS_TEMPLATE.format(**game.get_status()),
            "",
        ]
        if game.tamagochi.is_sick():
            lines.append(SICK_MESSAGE)
        lines.append(MENU)
        print("\n".join(lines))

        action = input("Выберите действие: ")
        match action:
            case "1":
                income = game.work()
                output = f'Вы заработали {income} монет'
            case "2":
                game.buy_food()
            case "3":
                game.buy_medicine()
            case "4":
                game.feed_tamagochi()
            case "5":
                game.heal_tamagochi()
            case "6":
                game.play_with_tamagochi()
                output = 'Вы поиграли с питомцем'
            case "7":
                game.rest_tamagochi()
                output = 'Питомец отдохнул'
            case "0":
                break
            case _:
                output = "Неверная команда"

        if action in {"1", "6", "7"}:
            try:
                game.tamagochi.update()
            except TamagochiIsGone as error:
                print(error)
                break

        subprocess.run(["clear"], check=False)


if __name__ == "__main__":
    main()
