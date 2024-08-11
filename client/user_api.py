import requests
from ..url_config import UrlConfig
import allure


url = UrlConfig.domain


class UserApi:
    @allure.step('Зарегистриовать пользователя')
    def post_register(self, payload):
        response = requests.post(url + UrlConfig.api_register, data=payload)
        return response

    @allure.step('Авторизоваться пользователем')
    def post_login(self, payload):
        response = requests.post(url + UrlConfig.api_login, data=payload)
        return response

    @allure.step('Выйти из личного кабинета пользователя')
    def post_logout(self, payload):
        response = requests.post(url + UrlConfig.api_logout, data=payload)
        return response

    @allure.step('Удалить пользователя')
    def delete_user(self, headers):
        response = requests.delete(url + UrlConfig.api_user, headers=headers)
        return response

    @allure.step('Изменить данные пользователя')
    def patch_change_user(self, payload, headers):
        response = requests.patch(url + UrlConfig.api_user, data=payload, headers=headers)
        return response
