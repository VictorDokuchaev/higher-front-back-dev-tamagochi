"""Модуль с интерфейсом и реализацией класса игры."""

from abc import ABC, abstractmethod
import copy
from typing import Any

from game.clicker import AbstractClicker
from game.exceptions import NotEnoughMoney
from game.models import Food, Medicine
from game.tamagochi import AbstractTamagochi


class AbstractGame(ABC):
    """Интерфейс для логики игры."""

    @abstractmethod
    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine]
    ):
        """Абстрактный метод инициализации класса игры.

        :param tamagochi: экземпляр тамагочи.
        :param clicker: экземпляр кликера.
        :param all_food: все доступные варианты еды.
        :param all_medicine: все доступные варианты лекарств.
        """
        raise NotImplementedError

    @abstractmethod
    def work(self) -> int:
        """Абстрактный метод для логики действия "работа".

        :return: количество заработанных монет.
        """
        raise NotImplementedError

    @abstractmethod
    def buy_food(self) -> None:
        """Абстрактный метод для покупки еды."""
        raise NotImplementedError

    @abstractmethod
    def buy_medicine(self) -> None:
        """Абстрактный метод для покупки лекарства."""
        raise NotImplementedError

    @abstractmethod
    def feed_tamagochi(self) -> None:
        """Абстрактный метод для кормления тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def heal_tamagochi(self) -> None:
        """Абстрактный метод для лечения тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def rest_tamagochi(self) -> None:
        """Абстрактный метод для отдыха тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def play_with_tamagochi(self) -> None:
        """Абстрактный метод для игры с тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def get_status(self) -> dict[str, Any]:
        """Абстрактный метод для получения статуса тамагочи.

        :return: словарь со всеми характеристиками тамагочи.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def food(self) -> list[Food]:
        """Абстрактное свойство для доступа к сумке с едой.

        :return: список с имеющимися (купленными) объектами еды.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def medicine(self) -> list[Medicine]:
        """Абстрактное свойство для доступа к сумке с лекарствами.

        :return: список с имеющимися (купленными) объектами лекарств.
        """
        raise NotImplementedError


class ConsoleGame(AbstractGame):
    """Игра через консоль."""

    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine],
    ) -> None:
        """Инициализирует игру, витрину, сумки и кошелёк.

        :param tamagochi: экземпляр тамагочи.
        :param clicker: экземпляр кликера.
        :param all_food: витрина еды.
        :param all_medicine: витрина лекарств.
        :return: None.
        """
        self.tamagochi = tamagochi
        self.clicker = clicker
        self.all_food = all_food
        self.all_medicine = all_medicine
        self._food: list[Food] = []
        self._medicine: list[Medicine] = []
        self.coins = 0

    @property
    def food(self) -> list[Food]:
        """Сумка с купленной едой.

        :return: список купленной еды.
        """
        return self._food

    @property
    def medicine(self) -> list[Medicine]:
        """Сумка с купленными лекарствами.

        :return: список купленных лекарств.
        """
        return self._medicine

    def work(self) -> int:
        """Зарабатывает монеты через кликер.

        :return: количество заработанных монет.
        """
        self.clicker.click()
        income = self.clicker.income_per_click
        self.coins += income
        return income

    def buy_food(self) -> None:
        """Покупает еду с витрины и кладёт её в сумку.

        :return: None.
        """
        self._show_catalog(self.all_food, "Еды нет")
        self._buy(self._food, self.all_food)

    def buy_medicine(self) -> None:
        """Покупает лекарство с витрины и кладёт его в сумку.

        :return: None.
        """
        self._show_catalog(self.all_medicine, "Лекарств нет")
        self._buy(self._medicine, self.all_medicine)

    def feed_tamagochi(self) -> None:
        """Кормит тамагочи едой из сумки.

        :return: None.
        """
        self._show_catalog(self._food, "Еды нет")
        index = self._ask_index(self._food)
        if index is None:
            return

        food = self._food.pop(index)
        self.tamagochi.feed(food)

    def heal_tamagochi(self) -> None:
        """Лечит тамагочи лекарством из сумки.

        :return: None.
        """
        self._show_catalog(self._medicine, "Лекарств нет")
        index = self._ask_index(self._medicine)
        if index is None:
            return

        medicine = self._medicine[index]
        self.tamagochi.heal(medicine)
        medicine.uses += 1
        if medicine.is_empty():
            self._medicine.pop(index)

    def rest_tamagochi(self) -> None:
        """Даёт тамагочи отдохнуть.

        :return: None.
        """
        self.tamagochi.rest()

    def play_with_tamagochi(self) -> None:
        """Играет с тамагочи.

        :return: None.
        """
        self.tamagochi.play()

    def get_status(self) -> dict[str, Any]:
        """Возвращает характеристики тамагочи и число монет.

        :return: словарь с hunger, hp, energy и coins.
        """
        return {
            **self.tamagochi.status,
            "coins": self.coins
        }

    def _show_catalog(
        self,
        catalog: list[Food] | list[Medicine],
        empty_message: str,
    ) -> None:
        """Печатает каталог или сообщение, если он пуст.

        :param catalog: список товаров для показа.
        :param empty_message: текст, если список пустой.
        :return: None.
        """
        if catalog:
            for index, product in enumerate(catalog):
                print(f"{index + 1}: {product}")
        else:
            print(empty_message)
        print("0: Выход")

    def _buy(
        self,
        bag: list[Food] | list[Medicine],
        catalog: list[Food] | list[Medicine],
    ) -> None:
        """Покупает товар с витрины и кладёт глубокую копию в сумку.

        :param bag: сумка игрока.
        :param catalog: витрина товаров.
        :return: None.
        :raises NotEnoughMoney: если не хватает монет, ошибка ловится внутри.
        """
        while True:
            product_index = self._ask_index(catalog)
            if product_index is None:
                print("Покупка отменена")
                return

            product = copy.deepcopy(catalog[product_index])
            try:
                if self.coins < product.price:
                    raise NotEnoughMoney(
                        "Недостаточно средств для покупки"
                    )
            except NotEnoughMoney as error:
                print(error)
                continue

            self.coins -= product.price
            bag.append(product)
            print(f"Куплен {product.name}. На балансе: {self.coins}")
            return

    def _ask_index(self, catalog: list[Food] | list[Medicine]) -> int | None:
        """Спрашивает номер товара в каталоге.

        :param catalog: список, из которого выбирают.
        :return: индекс товара или None при отмене.
        """
        while True:
            number = self._get_number()

            if number == 0:
                return None

            index = number - 1
            if len(catalog) <= index:
                print("Неверный номер")
                continue

            return index

    def _get_number(self) -> int:
        """Читает неотрицательное целое число из ввода.

        :return: введённое число.
        """
        while True:
            number = input("Введите: ")
            if number.isdigit():
                return int(number)
