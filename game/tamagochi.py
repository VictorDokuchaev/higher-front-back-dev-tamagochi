"""Модуль с интерфейсом и реализациями класса тамагочи"""

from abc import ABC, abstractmethod

from game.exceptions import (
    IncorrectEnergy,
    IncorrectHp,
    IncorrectHunger,
    TamagochiIsGone,
)
from game.models import Food, Medicine


class AbstractTamagochi(ABC):
    """Интерфейс логики тамагочи"""

    @abstractmethod
    def feed(self, food: Food) -> None:
        """
        Абстрактный метод для кормления тамагочи

        :param food: объект еды для кормления
        """
        raise NotImplementedError

    @abstractmethod
    def play(self) -> None:
        """Абстрактный метод для игры с тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def rest(self) -> None:
        """Абстрактный метод для отдыха тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def heal(self, medicine: Medicine) -> None:
        """
        Абстрактный метод для лечения тамагочи

        :param medicine: лекарство для лечения
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def status(self) -> dict[str, int]:
        """
        Абстрактное свойство для доступа ко всем состояниям тамагочи

        :return: словарь со всеми состояниями тамагочи
        """
        raise NotImplementedError

    @abstractmethod
    def is_alive(self) -> bool:
        """
        Абстрактный метод для проверки жив ли тамагочи

        :return: True если жив, иначе False
        """
        raise NotImplementedError

    @abstractmethod
    def is_sick(self) -> bool:
        """
        Абстрактный метод для проверки, не заболел ли тамагочи

        :return: True если тамагочи болеет, иначе False
        """
        raise NotImplementedError

    @abstractmethod
    def update(self) -> None:
        """
        Абстрактный метод для обновления состояний тамагочи.
        Должен использоваться после каждого взаимодействия с тамагочи
        """
        raise NotImplementedError


class CatTamagochi(AbstractTamagochi):
    """Кот тамагочи"""

    MIN_STAT = 0
    MAX_STAT = 100

    PLAY_HUNGER = 15
    PLAY_ENERGY = 10

    REST_ENERGY = 15
    SICK_REST_ENERGY = 5

    TICK_HUNGER = 3
    TICK_ENERGY = 2

    HP_LOSS = 1
    SICK_HP_LOSS = 3

    HUNGER_THRESHOLD = 50
    ENERGY_THRESHOLD = 20

    SICK_HUNGER = 70
    SICK_HP = 30

    def __init__(
        self,
        hp: int = MAX_STAT,
        energy: int = MAX_STAT,
        hunger: int = MIN_STAT,
    ) -> None:
        """Устанавливает начальные настройки тамагочи"""
        if self.MIN_STAT < hp <= self.MAX_STAT:
            self.hp = hp
        else:
            raise IncorrectHp(
                f'Need {self.MIN_STAT} < hp <= {self.MAX_STAT}'
            )

        if self.MIN_STAT <= energy <= self.MAX_STAT:
            self.energy = energy
        else:
            raise IncorrectEnergy(
                f'Need {self.MIN_STAT} <= energy <= {self.MAX_STAT}'
            )

        if self.MIN_STAT <= hunger <= self.MAX_STAT:
            self.hunger = hunger
        else:
            raise IncorrectHunger(
                f'Need {self.MIN_STAT} <= hunger <= {self.MAX_STAT}'
            )

        self._sick = False

    def feed(self, food: Food) -> None:
        """Кормит тамагочи"""
        self._change_attr("hunger", -food.satiety)

    def play(self) -> None:
        """Играет с тамагочи: растит голод и тратит энергию"""
        self._change_attr("hunger", self.PLAY_HUNGER)
        self._change_attr("energy", -self.PLAY_ENERGY)

    def rest(self) -> None:
        """Восстанавливает энергию, при болезни — слабее"""
        if self.is_sick():
            self._change_attr("energy", self.SICK_REST_ENERGY)
            return

        self._change_attr("energy", self.REST_ENERGY)

    def heal(self, medicine: Medicine) -> None:
        """Лечит здоровье и снимает болезнь"""
        self._change_attr("hp", medicine.heal_hp)
        self._sick = False

    @property
    def status(self) -> dict[str, int]:
        """Возвращает все состояния тамагочи"""
        return {
            "hp": self.hp,
            "energy": self.energy,
            "hunger": self.hunger,
        }

    def is_alive(self) -> bool:
        """Проверяет, жив ли тамагочи"""
        return self.hp > self.MIN_STAT

    def is_sick(self) -> bool:
        """Проверяет наличие болезней у тамагочи"""
        return self._sick

    def update(self) -> None:
        """Обновляет состояние тамагочи"""
        hp_loss = self.SICK_HP_LOSS if self.is_sick() else self.HP_LOSS
        if self.energy < self.ENERGY_THRESHOLD:
            self._change_attr("hp", -hp_loss)
        if self.hunger > self.HUNGER_THRESHOLD:
            self._change_attr("hp", -hp_loss)

        self._change_attr("hunger", self.TICK_HUNGER)
        self._change_attr("energy", -self.TICK_ENERGY)

        if self.hunger > self.SICK_HUNGER or self.hp < self.SICK_HP:
            self._sick = True

        if not self.is_alive():
            raise TamagochiIsGone("Тамагочи погиб")

    def _change_attr(self, attr: str, delta: int) -> None:
        """
        Изменить указанный атрибут на дельта
        с учётом ограничений
        """
        setattr(
            self,
            attr,
            (
                min(self.MAX_STAT, getattr(self, attr) + delta)
                if delta > 0
                else max(self.MIN_STAT, getattr(self, attr) + delta)
            ),
        )
