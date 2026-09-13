"""Модуль с интерфейсом и реализациями класса тамагочи"""

from abc import ABC, abstractmethod

from game.exceptions import IncorrectEnergy, IncorrectHp, IncorrectHunger
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
            raise IncorrectHp(f'Need {self.MIN_STAT} < hp <= {self.MAX_STAT}')
        
        if self.MIN_STAT <= energy <= self.MAX_STAT:
            self.energy = energy
        else:
            raise IncorrectEnergy(f'Need {self.MIN_STAT} <= energy <= {self.MAX_STAT}')
        
        if self.MIN_STAT <= hunger <= self.MAX_STAT:
            self.hunger = hunger
        else:
            raise IncorrectHunger(f'Need {self.MIN_STAT} <= hunger <= {self.MAX_STAT}')

    def feed(self, food: Food) -> None:
        """Кормит тамагочи"""
        self._change_attr("hunger", -food.satiety)

    def play(self) -> None:
        """
        Начинает игру с тамагочи.
        Отнимает 10 энергии
        Добавляет 15 голода
        """
        self._change_attr("hunger", 15)
        self._change_attr("energy", -10)

    def rest(self) -> None:
        """
        Отдых тамагочи,
        если здоров, то +15 энергии,
        если болен, то +5 энергии
        """
        if self.is_sick():
            self._change_attr("energy", 5)
            return

        self._change_attr("energy", 15)

    def heal(self, medicine: Medicine) -> None:
        """Использует медицину для лечения"""
        self._change_attr("hp", medicine.heal_hp)

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
        return self.hp > 0

    def is_sick(self) -> bool:
        """Проверяет наличие болезней у тамагочи"""
        if self.hunger > self.SICK_HUNGER or self.hp < self.SICK_HP:
            return True

        return False

    def update(self) -> None:
        """Обновляет состояние тамагочи"""
        if self.energy < self.ENERGY_THRESHOLD:
            if self.is_sick():
                self._change_attr("hp", -3)
            else:
                self._change_attr("hp", -1)
        if self.hunger > self.HUNGER_THRESHOLD:
            if self.is_sick():
                self._change_attr("hp", -3)
            else:
                self._change_attr("hp", -1)

        self._change_attr("hunger", 3)
        self._change_attr("energy", -2)
        
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
