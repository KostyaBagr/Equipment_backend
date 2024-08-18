
"""
Отображение моделей оборудования.
    EquipmentAdmin: класс для отображения сущности Equipment.
    EquipmentTypeAdmin: класс для отображения сущности EquipmentType.
"""
from django.contrib import admin

from api.models import Equipment, EquipmentType


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    """Отображение таблицы Equipment."""
    pass 


@admin.register(EquipmentType)
class EquipmentTypeAdmin(admin.ModelAdmin):
    """Отображение таблицы EquipmentType."""
    pass 
