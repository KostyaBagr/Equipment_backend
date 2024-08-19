
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
    """Сериалайзер для получения списка Equipment с нужными полями."""
    type = EquipmentTypeSerializer(read_only=True)
    serial_numbers = serializers.SerializerMethodField()

    class Meta:
        model = Equipment
        fields = ['id', 'serial_numbers', 'type', 'notation']

    def get_serial_numbers(self, obj):
        """Получить все серийные номера для данного типа и примечания."""
        related_serial_numbers = Equipment.objects.filter(type=obj.type,
                                                          notation=obj.notation).values_list('serial_number', flat=True) #
        return list(related_serial_numbers)


class EquipmentSerializer(serializers.ModelSerializer):
    """Сериалайзер для таблицы Equipment."""
    serial_number = serializers.ListField(child=serializers.CharField(),
                                          write_only=True)

    class Meta:
        model = Equipment
        fields = ["id", "serial_number", "type", "notation"]

    def validate(self, data: dict) -> dict:
        """
        Метод для валидации объекта Equipment.

        args:
            data: данные от клиента.
        """
        serial_numbers = data.get("serial_number")
        equipment_type = data.get("type")
        errors = {}

        if equipment_type:
            mask = equipment_type.serial_number_mask
            for serial in serial_numbers:
                if not self._validate_serial_number(serial, mask):
                    errors[serial] = f"Serial number '{serial}' does not match the mask '{mask}'."  # noqa 
                elif Equipment.objects.filter(serial_number=serial).exists():
                    errors[serial] = f"Serial number '{serial}' already exists."  # noqa  

        if errors:
            raise serializers.ValidationError(errors)

        return data

    def create(self, validated_data: dict):
        """
        Переопределение метода create для работы с массивом серийных номеров.
        
        args:
            validated_data: данные от клиента.
        """  # noqa  
        serial_numbers = validated_data.pop("serial_number")
        equipment_list = []
        for serial in serial_numbers:
            equipment = Equipment.objects.create(serial_number=serial, **validated_data) # noqa 
            equipment_list.append(equipment)
        return equipment_list

    def _validate_serial_number(self, serial_number: str, mask: str) -> bool:
        """
        Сравнение серийного номера и маски.

        args:
            serial_number: Серийный номер для сравнения.
            mask: Маска в regex формате для сравнения.
        """
        regex = self._numbers_to_mask(mask)
        return re.fullmatch(regex, serial_number) is not None

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



    