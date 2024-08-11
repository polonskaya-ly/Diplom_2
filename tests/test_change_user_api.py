from ..data.data_for_assert import UNAUTHORISED_ERROR
from ..client.user_api import UserApi
from ..data.data_for_test import TestData
import pytest
import allure


class TestChangeUser:
    @allure.title('Изменение данных пользователя без авторизации')
    @pytest.mark.parametrize('payload', [{'name': TestData.new_name, 'email': TestData.email},
                                         {'name': TestData.name, 'email': TestData.new_email}])
    def test_change_unauthorised_user(self, payload):
        headers = {}
        response = UserApi().patch_change_user(payload, headers)
        r = response.json()

        assert response.status_code == 401
        assert r['message'] == UNAUTHORISED_ERROR

    @allure.title('Изменение email пользователя с авторизацией')
    def test_change_authorised_user_email(self, register_data, register_user, delete_user):
        payload = {'name': register_data[0],
                   'email': TestData.new_email}
        token = register_user
        headers = {'Authorization': token}
        response = UserApi().patch_change_user(payload, headers)
        r = response.json()

        assert response.status_code == 200
        assert r['user']['email'] == TestData.new_email
        assert r['user']['name'] == register_data[0]
        delete_user.update(headers)

    @allure.title('Изменение имени пользователя с авторизацией')
    def test_change_authorised_user_name(self, register_data, register_user, delete_user):
        payload = {'name': TestData.new_name,
                   'email': register_data[1]}
        token = register_user
        headers = {'Authorization': token}
        response = UserApi().patch_change_user(payload, headers)
        r = response.json()

        assert response.status_code == 200
        assert r['user']['email'] == register_data[1]
        assert r['user']['name'] == TestData.new_name
        delete_user.update(headers)
