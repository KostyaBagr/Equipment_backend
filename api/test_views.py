import pytest

from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse

from api.models import Equipment, EquipmentType


@pytest.fixture
def create_user():
    """Фикстура для создания пользователя."""
    username = "test_user"
    password = "12345678"

    return User.objects.create_user(username=username, password=password)


@pytest.fixture
def create_equipment_type():
    """Создание типа оборудования."""
    return EquipmentType.objects.create(name='Type1', 
                                        serial_number_mask='XXAAAAAXAA')


@pytest.fixture
def create_equipment_list(create_equipment_type):
    """Создание списка оборудования. Положительный кейс."""
    Equipment.objects.create(
        type=create_equipment_type,
        serial_number="A2BCDEF2GF",
        notation="test"
    )
    Equipment.objects.create(
        type=create_equipment_type,
        serial_number="A3BCDEF2GF",
        notation="test2"
    )


@pytest.fixture
def create_equipment(create_equipment_type):
    """Создание оборудования."""
    return Equipment.objects.create(
        type=create_equipment_type,
        serial_number="D3BCDEF2GF",
        notation="test_test"
    )


@pytest.mark.django_db
def test_get_equipment_list_positive(client, create_user, create_equipment_list):
    """Тестирование получение записи equipment. Положительный исход."""
    client.force_login(create_user)
    url = reverse('equipment-list') 
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data.get("count") == 2


@pytest.mark.django_db
def test_get_equipment_detail_positive(client, create_user, create_equipment):
    """Получение одного объекта Equipment. Положительный исход."""
    client.force_login(create_user)
    equipment_id = create_equipment.id
    url = reverse('equipment-detail', args=[equipment_id])

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_create_equipment_positive(client, create_user, create_equipment_type):
    """Тестирование создания записи equipment. Положительный исход."""
    client.force_login(create_user)
    url = reverse('equipment-list')
    data = {
        'serial_number': 'A8BDQEF2GF',
        'type': create_equipment_type.id,
        'notation': 'test'
    }
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert 'serial_number' in response.data


@pytest.mark.django_db
def test_create_equipment_negative(client, create_user, create_equipment_type):
    """Тестирование создания записи equipment. Негативный исход."""
    client.force_login(create_user)
    url = reverse('equipment-list')
    data = {
        'serial_number': '',
        'type': create_equipment_type.id,
        'notation': 'test'
    }
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_update_equipment_positive(client, create_user, create_equipment):
    """Тестирование изменения записи equipment. Положительный исход."""
    client.force_login(create_user)
    url = reverse('equipment-detail', args=[create_equipment.id])
    data = {
        'serial_number': 'A2BCDEF9GP',
        'type': create_equipment.type.id,
        'notation': 'updated notation'
    }
    response = client.put(url, data, content_type='application/json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['serial_number'] == 'A2BCDEF9GP'
    assert response.data['notation'] == 'updated notation'


@pytest.mark.django_db
def test_delete_equipment_positive(client, create_user, create_equipment):
    """Тестирование удаления записи equipment. Положительный исход."""
    client.force_login(create_user)
    url = reverse('equipment-detail', args=[create_equipment.id])
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Equipment.objects.filter(id=create_equipment.id).exists()


@pytest.mark.django_db
def test_get_equipment_type_list(client, create_user):
    """Тестирование получения списка EquipmentType. Положительный исход."""
    client.force_login(create_user)
    url = reverse('equipment-type-list')
    
    EquipmentType.objects.create(name="Type 1", serial_number_mask="SNM1")
    EquipmentType.objects.create(name="Type 2", serial_number_mask="SNM2")

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
