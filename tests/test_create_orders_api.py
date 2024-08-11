from ..client.order_api import OrderApi
from ..data.data_for_assert import INGREDIENTS_ERROR
import allure


class TestCreateOrder:
    @allure.title('Создание заказа неавторизованным пользователем')
    def test_create_order_unauthorised_user(self, get_ingredient):
        payload = {"ingredients": [get_ingredient[0], get_ingredient[1]]}
        headers = {}
        response = OrderApi().post_create_order(payload, headers)
        r = response.json()

        assert response.status_code == 200
        assert r['success'] is True
        assert r['order']['number'] > 0

    @allure.title('Создание заказа авторизованным пользователем')
    def test_create_order_authorised_user(self, get_ingredient, register_user, delete_user):
        payload = {"ingredients": [get_ingredient[0], get_ingredient[1]]}
        token = register_user
        headers = {'Authorization': token}
        response = OrderApi().post_create_order(payload, headers)
        r = response.json()

        assert response.status_code == 200
        assert r['success'] is True
        assert r['order']['number'] > 0
        delete_user.update(headers)

    @allure.title('Создание заказа без ингредиентов авторизованным пользователем')
    def test_create_order_authorised_user_without_ingredients(self, register_user, delete_user):
        payload = {}
        token = register_user
        headers = {'Authorization': token}
        response = OrderApi().post_create_order(payload, headers)
        r = response.json()

        assert response.status_code == 400
        assert r['message'] == INGREDIENTS_ERROR
        delete_user.update(headers)

    @allure.title('Создание заказа без ингредиентов неавторизованным пользователем')
    def test_create_order_unauthorised_user_without_ingredients(self):
        payload = {}
        headers = {}
        response = OrderApi().post_create_order(payload, headers)
        r = response.json()

        assert response.status_code == 400
        assert r['message'] == INGREDIENTS_ERROR

    @allure.title('Создание заказа с неверным хэшем ингредиентов авторизованным пользователем')
    def test_create_order_authorised_user_with_fake_hash(self, get_ingredient, register_user, delete_user):
        payload = {"ingredients": [get_ingredient[0] + 'a', get_ingredient[1]]}
        token = register_user
        headers = {'Authorization': token}
        response = OrderApi().post_create_order(payload, headers)

        assert response.status_code == 500
        delete_user.update(headers)

    @allure.title('Создание заказа с неверным хэшем ингредиентов неавторизованным пользователем')
    def test_create_order_unauthorised_user_with_fake_hash(self, get_ingredient):
        payload = {"ingredients": [get_ingredient[0] + 'a', get_ingredient[1]]}
        headers = {}
        response = OrderApi().post_create_order(payload, headers)

        assert response.status_code == 500
