from ..data.data_for_assert import LOGIN_ERROR
from ..client.user_api import UserApi
from ..data.data_for_test import TestData
import allure


class TestLoginUser:
    @allure.title('Логин под существующим пользователем')
    def test_login(self, logout_user):
        payload = {'password': TestData.password,
                   'email': TestData.email}
        response = UserApi().post_login(payload)
        r = response.json()

        assert response.status_code == 200
        assert r['user']['email'] == TestData.email
        assert 'Bearer' in r['accessToken']
        token = r['refreshToken']
        payload = {'token': token}
        logout_user.update(payload)

    @allure.title('Логин с неверным логином и паролем')
    def test_login_with_fake_password_and_login(self):
        payload = {'password': TestData.fake_password,
                   'email': TestData.fake_email}
        response = UserApi().post_login(payload)
        r = response.json()

        assert response.status_code == 401
        assert r['message'] == LOGIN_ERROR
