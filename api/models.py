"""
Модуль таблиц оборудования в БД.
    EquipmentType: модель данных для хранения типа оборудования.
    Equipment: Модель данныз для хранения сведений о оборудовани.
"""

from django.db import models


class EquipmentType(models.Model):
    """Таблица для хранения типа оборудования."""
    name = models.CharField("Наименование", max_length=100)
    serial_number_mask = models.CharField("Маска серийного номера",
                                          max_length=100)

    def __str__(self) -> str:
        """Представление записи в админ-панели."""
        return f"Type: id {self.id}, name {self.name}."
    
    class Meta:
        """Представление таблицы в админ-панели."""
        verbose_name = 'Тип оборудования'
        verbose_name_plural = 'Типы оборудования'


class Equipment(models.Model):
    """Таблица для хранения оборудования."""
    type = models.ForeignKey(EquipmentType, on_delete=models.CASCADE,
                             verbose_name="Тип оборудования")
    serial_number = models.CharField("Серийный номер", max_length=200, unique=True) # noqa 
    notation = models.TextField("Примечание")

    def __str__(self) -> str:
        """Представление записи в админ-панели."""
        return f"Оборудование: id {self.id},type {self.type}, serial {self.serial_number}" # noqa 
    
    class Meta:
        """Представление таблицы в админ-панели."""
        verbose_name = 'Оборудование'
        verbose_name_plural = 'Оборудование'
        unique_together = (('type', 'serial_number'),)