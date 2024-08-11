import requests
from ..url_config import UrlConfig
import allure


url = UrlConfig.domain


class OrderApi:
    @allure.step('Получить ингредиенты')
    def get_ingredients(self):
        response = requests.get(url + UrlConfig.api_ingredients)
        return response

    @allure.step('Создать заказ')
    def post_create_order(self, data, headers):
        response = requests.post(url + UrlConfig.api_orders, data=data, headers=headers)
        return response

    @allure.step('Получить заказы пользователя')
    def get_orders(self, headers):
        response = requests.get(url + UrlConfig.api_orders, headers=headers)
        return response
