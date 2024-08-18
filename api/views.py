"""
Представления для сущности Equipment.
    EquipmentList: Создание и получение объектов Equipment.
    EquipmentDetail: Детальная обработка объектов Equipment.
    EquipmentTypeList: Получения списка объектов EquipmentType.
"""

from rest_framework import filters
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from api.models import Equipment, EquipmentType
from api.serializers import (EquipmentSerializer, EquipmentTypeSerializer, 
                             EquipmentGetSerializer)


class EquipmentList(generics.ListCreateAPIView):
    """
    Представление для вывода и создания объектов Equipment.
    
    args:
        - ListCreateAPIView: Представление для перечисления набора запросов 
        или создания экземпляра модели.
    """
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['type__name', 'serial_number']
    
    def get_serializer_class(self):
        """Метод заменят сериалайзер в зависимости от метода HTTP."""
        if self.request.method == 'GET':
            return EquipmentGetSerializer
        elif self.request.method in ['POST', 'PUT', 'PATCH']:
            return EquipmentSerializer
        return super().get_serializer_class()
    
    def get_serializer(self, instance=None, data=None, many=False, partial=False): # noqa  
        """
        Метод используется для перепределния функций сериалайзера.
        """
        if data:
            return super().get_serializer(instance=instance,
                                          data=data,
                                          many=True,
                                          partial=partial)
        return super().get_serializer(instance=instance,
                                      many=True,
                                      partial=partial)
  

class EquipmentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Представление для работы с объектом Equipment.

    args:
        - RetrieveAPIView: Представление для получения, обновления или
        удаления экземпляра модели.
    """
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [IsAuthenticated]


class EquipmentTypeList(generics.ListAPIView):
    """
    Представление для вывода списка объектов EquipmentType.
    
    args:
        - ListAPIView: Представление для перечисления набора запросов.
    """
    queryset = EquipmentType.objects.all()
    serializer_class = EquipmentTypeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'serial_number_mask']
