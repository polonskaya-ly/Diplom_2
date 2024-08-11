import random
import pytest
import allure

from .client.order_api import OrderApi
from .data.data_for_test import TestData
from .client.user_api import UserApi


@pytest.fixture
def register_data():
    name = f"Любовь{random.randint(1000, 9999)}"
    email = f"polonskaya{random.randint(1000, 9999)}@yandex.ru"
    return name, email


@pytest.fixture
@allure.title("Регистрация уникального пользователя")
def register_user(register_data):
    payload = {'name': register_data[0],
               'password': TestData.password,
               'email': register_data[1]}
    response = UserApi().post_register(payload)
    r = response.json()
    headers = r['accessToken']
    return headers


@pytest.fixture(scope='function')
@allure.title("Удаление пользователя после выполнения теста")
def delete_user():
    headers = {}
    yield headers
    UserApi().delete_user(headers)


@pytest.fixture()
@allure.title("Создание заказа без авторизации")
def create_order_unauthorised(get_ingredient):
    payload = {"ingredients": [get_ingredient[0], get_ingredient[1]]}
    headers = {}
    OrderApi().post_create_order(payload, headers)


@pytest.fixture()
@allure.title("Создание заказа уникальным авторизованным пользователем")
def create_order_authorised(get_ingredient, register_user):
    payload = {"ingredients": [get_ingredient[0], get_ingredient[1]]}
    token = register_user
    headers = {'Authorization': token}
    OrderApi().post_create_order(payload, headers)
    return token


@pytest.fixture(scope='function')
@allure.title("Выход из ЛК пользователя")
def logout_user():
    payload = {}
    yield payload
    UserApi().post_logout(payload)


@pytest.fixture()
@allure.title("Получение списка ингредиентов")
def get_ingredient():
    response = OrderApi().get_ingredients()
    r = response.json()
    id_1 = r['data'][0]['_id']
    id_2 = r['data'][1]['_id']
    return id_1, id_2
