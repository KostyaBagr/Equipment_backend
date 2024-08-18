"""
Представления для сущности Equipment.
    EquipmentList: Создание и получение объектов Equipment.
    EquipmentDetail: Детальная обработка объектов Equipment.
    EquipmentTypeList: Получения списка объектов EquipmentType.
"""

from rest_framework import filters
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

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
        """Метод заменяет сериалайзер в зависимости от метода HTTP."""
        if self.request.method == 'GET':
            return EquipmentGetSerializer
        return EquipmentSerializer
    
    def post(self, request, *args, **kwargs):
        """Переопределение метода post для создание одного или несольких инстансов.""" # noqa
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, 
                        headers=headers)


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
