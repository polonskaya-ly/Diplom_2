from ..client.order_api import OrderApi
from ..data.data_for_assert import UNAUTHORISED_ERROR
import allure


class TestGetUserOrders:
    @allure.title('Получение заказов неавторизованного пользователя')
    def test_get_user_orders_unauthorised_user(self, create_order_unauthorised):
        headers = {}
        response = OrderApi().get_orders(headers)
        r = response.json()

        assert response.status_code == 401
        assert r['message'] == UNAUTHORISED_ERROR

    @allure.title('Получение заказов авторизованного пользователя')
    def test_get_user_orders_authorised_user(self, create_order_authorised, delete_user):
        token = create_order_authorised
        headers = {'Authorization': token}
        response = OrderApi().get_orders(headers)
        r = response.json()

        assert response.status_code == 200
        assert len(r['orders']) > 0
        delete_user.update(headers)
