
"""
Модуль для хранения классов сериалайзеров.

    EquipmentSerializser: сериалайзер для работы с объектами Equipment.
    EquipmentGetSerializer: сериалайзер для работы с объектами Equipment(чтение). # noqa
    EquipmentTypeSerializser: сериалайзер для работы с объектами EquipmentTypeSerializser. # noqa
"""
import re

from rest_framework import serializers

from api.models import Equipment, EquipmentType


class EquipmentTypeSerializer(serializers.ModelSerializer):
    """Сериалайзер для вывода списка EquipmentType."""
    class Meta:
        model = EquipmentType
        fields = "__all__"
   

class EquipmentGetSerializer(serializers.ModelSerializer):
    """Сериайлайзер для получения списка Equipment."""
    type = EquipmentTypeSerializer(read_only=True)

    class Meta:
        model = Equipment
        fields = "__all__"


class EquipmentSerializer(serializers.ModelSerializer):
    """Сериалайзер для таблицы Equipment."""
    class Meta:
        model = Equipment
        fields = "__all__"

    def validate(self, data) -> dict:
        """Метод для валидации объекта Equipment."""
        serial = data.get("serial_number")
        equipment_type = data.get("type")

        if equipment_type:
            mask = equipment_type.serial_number_mask
            if not self._validate_serial_number(serial, mask):
                raise serializers.ValidationError(f"Serial number '{serial}' does not match the mask '{mask}'.") # noqa
        return data
    
    def _validate_serial_number(self, serial_number: str, mask: str) -> bool:
        """
        Сравнение серийного номера и маски.

        args:
            serial_number: Серийный номер для сравнения.
            mask: Маска в regex формате для сравнения.
        """
        regex = self._numbers_to_mask(mask)
        if re.fullmatch(regex, serial_number):
            return True

    def _numbers_to_mask(self, mask: str) -> str:
        """
        Перевод маски в regex.
        
        args:
            mask: маска для перевода в regex.
        """
        if not mask:
            return ''
        conversion = { 
            'N': r'\d',
            'A': r'[A-Z]',
            'a': r'[a-z]',
            'X': r'[A-Z0-9]',
            'Z': r'[-_@]',
        }
        regex = ''.join(conversion.get(i, re.escape(i)) for i in mask)
        return f'^{regex}$'



    