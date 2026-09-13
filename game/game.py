"""Модуль с интерфейсом и реализацией класса игры"""

from abc import ABC, abstractmethod
import copy
from typing import Any

from game.clicker import AbstractClicker
from game.models import Food, Medicine
from game.tamagochi import AbstractTamagochi


class AbstractGame(ABC):
    """Интерфейс для логики игры"""

    @abstractmethod
    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine]
    ):
        """
        Абстрактный метод инициализации класса игры

        :param tamagochi: экземпляр тамагочи
        :param clicker: экземпляр кликера
        :param all_food: все доступные варианты еды
        :param all_medicine: все доступные варианты лекарств
        """
        raise NotImplementedError

    @abstractmethod
    def work(self) -> int:
        """
        Абстрактный метод для логики действия "работа

        :return: количество заработанных монет
        """
        raise NotImplementedError

    @abstractmethod
    def buy_food(self) -> None:
        """Абстрактный метод для покупки еды"""
        raise NotImplementedError

    @abstractmethod
    def buy_medicine(self) -> None:
        """Абстрактный метод для покупки лекарства"""
        raise NotImplementedError

    @abstractmethod
    def feed_tamagochi(self) -> None:
        """Абстрактный метод для кормления тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def heal_tamagochi(self) -> None:
        """Абстрактный метод для лечения тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def rest_tamagochi(self):
        """Абстрактный метод для отдыха тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def play_with_tamagochi(self):
        """Абстрактный метод для игры с тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def get_status(self) -> dict[str, Any]:
        """
        Абстрактный метод для получения статуса (всех характеристик) тамагочи

        :return: словарь со всеми характеристиками тамагочи
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def food(self) -> list[Food]:
        """
        Абстрактное свойство для доступа к сумке с едой

        :return: список с имеющимися (купленными) объектами еды
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def medicine(self) -> list[Medicine]:
        """
        Абстрактное свойство для доступа к сумке с лекарствами

        :return: список с имеющимися (купленными) объектами лекарств
        """
        raise NotImplementedError


class ConsoleGame(AbstractGame):
    """Игра через консоль"""

    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine],
    ) -> None:
        self.tamagochi = tamagochi
        self.clicker = clicker
        self.all_food = all_food
        self.all_medicine = all_medicine
        self._food: list[Food] = []
        self._medicine: list[Medicine] = []
        self.coins = 0

    @property
    def food(self) -> list[Food]:
        """Сумка с купленной едой"""
        return self._food

    @property
    def medicine(self) -> list[Medicine]:
        """Сумка с купленными лекарствами"""
        return self._medicine

    def work(self) -> int:
        """Работа для заработка монет"""
        self.clicker.click()
        income = self.clicker.income_per_click
        self.coins += income
        return income

    def buy_food(self) -> None:
        """Купить еду"""
        self._show_catalog(self.all_food)
        self._buy(self._food, self.all_food)

    def buy_medicine(self) -> None:
        """Купить лекарства"""
        self._show_catalog(self.all_medicine)
        self._buy(self._medicine, self.all_medicine)

    def feed_tamagochi(self) -> None:
        """Покормить тамагочи"""

    def heal_tamagochi(self) -> None:
        """Лечить тамагочи"""

    def rest_tamagochi(self):
        """Дать отдых тамагочи"""

    def play_with_tamagochi(self):
        """Играть с тамагочи"""

    def get_status(self) -> dict[str, Any]:
        """Получить все характеристики тамагочи"""
        return {
            **self.tamagochi.status,
            "coins": self.coins
        }

    def _show_catalog(self, catalog: list[Food] | list[Medicine]) -> None:
        for index, product in enumerate(catalog):
            print(f"{index + 1}: {product}")

    def _get_number(self) -> int:
        while True:
            number = input("Введите: ")
            if number.isdigit():
                return int(number)

    def _buy(
        self,
        bag: list[Food] | list[Medicine],
        catalog: list[Food] | list[Medicine],
    ) -> None:
        while True:
            number = self._get_number()
            if number == 0:
                print("Покупка отменена")
                return

            product_index = number - 1
            if len(catalog) <= product_index:
                print("Неверный номер")
                continue

            product = copy.copy(catalog[product_index])
            if self.coins < product.price:
                print("Недостаточно средств для покупки")
                continue

            self.coins -= product.price
            bag.append(product)
            print(f"Куплен {product.name}. На балансе: {self.coins}")
            return
