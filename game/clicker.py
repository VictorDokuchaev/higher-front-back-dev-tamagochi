"""Модуль с интерфейсом и реализацией кликера"""
import random
from abc import ABC, abstractmethod


class AbstractClicker(ABC):
    """Интерфейс для кликера"""

    @abstractmethod
    def __init__(self) -> None:
        """Абстрактный метод инициализации"""
        raise NotImplementedError

    @abstractmethod
    def click(self) -> None:
        """Абстрактный метод клика для накапливания монет"""
        raise NotImplementedError

    @property
    @abstractmethod
    def income_per_click(self) -> int:
        """Абстрактное свойство для доступа к количеству монет за клик"""
        raise NotImplementedError


class RandomClicker(AbstractClicker):
    """Случайный кликер"""

    def __init__(self, min_per_click: int, max_per_click: int) -> None:
        """Сохраняет диапазон дохода и стартовое значение за клик"""
        self.min_per_click = min_per_click
        self.max_per_click = max_per_click
        self._last_income = min_per_click

    def click(self) -> None:
        """Бросает случайный доход в заданном диапазоне"""
        self._last_income = random.randint(self.min_per_click, self.max_per_click)

    @property
    def income_per_click(self) -> int:
        """Доход за последний клик"""
        return self._last_income
