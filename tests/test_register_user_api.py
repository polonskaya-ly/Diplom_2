from ..data.data_for_assert import REGISTER_ERROR_USER, REGISTER_ERROR_FIELDS
from ..client.user_api import UserApi
from ..data.data_for_test import TestData
import pytest
import allure


class TestRegisterUser:
    @allure.title('Регистрация уникального пользователя')
    def test_registration(self, register_data, delete_user):
        payload = {'name': register_data[0],
                   'password': TestData.password,
                   'email': register_data[1]}
        response = UserApi().post_register(payload)
        r = response.json()

        assert response.status_code == 200
        assert 'Bearer' in r['accessToken']
        assert r['user']['email'] == register_data[1]
        token = r['accessToken']
        headers = {'Authorization': token}
        delete_user.update(headers)

    @allure.title('Регистрация пользователя, который уже зарегистрирован')
    def test_registration_user_already_registrated(self):
        payload = {'name': TestData.name,
                   'password': TestData.password,
                   'email': TestData.email}
        response = UserApi().post_register(payload)
        r = response.json()

        assert response.status_code == 403
        assert r['message'] == REGISTER_ERROR_USER

    @allure.title('Регистрация пользователя без заполнения одного из обязательных полей')
    @pytest.mark.parametrize('payload', [{'password': TestData.password,
                                          'email': TestData.email_2}, {'password': TestData.password,
                                                                       'name': TestData.name_2},
                                         {'name': TestData.name_2,
                                          'email': TestData.email_2}])
    def test_registration_without_required_field(self, payload):
        response = UserApi().post_register(payload)
        r = response.json()

        assert response.status_code == 403
        assert r['message'] == REGISTER_ERROR_FIELDS
