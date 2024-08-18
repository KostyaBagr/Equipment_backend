"""
Модуль хранит кастомные пути endpoint-ов.
"""
from django.urls import path

from api.views import EquipmentList, EquipmentDetail, EquipmentTypeList

urlpatterns = [
    path("equipment/", EquipmentList.as_view(), name='equipment-list'),
    path("equipment/<int:pk>/", EquipmentDetail.as_view(),
         name='equipment-detail'),
    path("equipment-type/", EquipmentTypeList.as_view(),
         name='equiopment-type-list')
]