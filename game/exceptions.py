"""Модуль с исключениями"""


class TamagochiIsGone(Exception):
    """Ошибка при смерти тамагочи"""


class NotEnoughMoney(Exception):
    """Ошибка когда не хватает монет для покупки"""


class IncorrectHp(Exception):
    """Ошибка когда указано неверное количество здоровья"""


class IncorrectEnergy(Exception):
    """Ошибка когда указано неверное количество энергии"""


class IncorrectHunger(Exception):
    """Ошибка когда указан неверный голод"""
