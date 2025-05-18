import requests
import pytest
import config


class Page:
    def __init__(self):
        """ Инициализация класса Page. 
        Настройка заголовков 
        HTTP-запросов и получение токена авторизации. """
        self._headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "application/json"
        }
        self._headers["Authorization"] = f"Bearer {self._get_auth_token()}"

    def _get_auth_token(self):
        """ Получение токена авторизации от сервера. 
        Возвращает токен, используемый для аутентификации запросов. 
        Если токен не найден или произошла ошибка — 
        тест считается проваленным. """
        try:
            response = requests.get(config.BASE_URL, headers=self._headers)
            raw_token = response.cookies.get('access-token')
            token = raw_token[9:] if raw_token and len(raw_token) > 9 else None

            if not token:
                pytest.fail("Не удалось получить токен авторизации")

            return token
        except Exception as e:
            pytest.fail(f"Ошибка получения токена: {e}")

    def add_product_to_cart(self, product_id):
        """ Добавляет товар в корзину. :param product_id: 
        идентификатор товара. :return: 
        объект Response с результатом POST-запроса. """
        try:
            url = f"{config.API_URL}{config.PRODUCT}"
            json = {
                "id": product_id,
                "adData": {
                    "item_list_name": "product-page"
                }
            }
            return requests.post(url, json=json, headers=self._headers)
        except Exception as e:
            pytest.fail(f"Ошибка добавления товара: {e}")

    def delete_product(self, product_id):
        """ Удаляет товар из корзины. 
        :param product_id: идентификатор товара. 
        :return: объект Response с результатом DELETE-запроса. """
        try:
            url = f"{config.API_URL}{config.PRODUCT}/{product_id}"
            return requests.delete(url, headers=self._headers)
        except Exception as e:
            pytest.fail(f"Ошибка удаления товара: {e}")

    def restore_product(self, product_id):
        """ Восстанавливает ранее удалённый товар обратно в корзину. 
        :param product_id: идентификатор товара. 
        :return: объект Response с результатом POST-запроса. """
        try:
            url = f"{config.API_URL}{config.PRODUCT_RESTORE}"
            json = {
                "productId": product_id
            }
            return requests.post(url, headers=self._headers, json=json)
        except Exception as e:
            pytest.fail(f"Ошибка восстановления товара: {e}")

    def get_cart(self):
        """ Запрашивает содержимое корзины товаров. 
        :return: объект Response с результатами GET-запроса. """
        try:
            url = f"{config.API_URL}{config.CART}"
            return requests.get(url, headers=self._headers)
        except Exception as e:
            pytest.fail(f"Ошибка получения корзины: {e}")

    def get_cart_product_id(self, product_id):
        """ Ищет продукт в корзине по его каталоговому ID 
        и возвращает внутренний ID продукта в корзине. 
        :param product_id: внешний идентификатор товара. 
        :return: внутренний ID товара в корзине 
        либо None, если не найден. """
        products = self.get_cart().json().get("products", [])
        product = next((product for product in products if product["goodsId"] == product_id), None)

        return product['id'] if product else None

    def clear_cart(self):
        """ Очищает всю корзину товаров. 
        :return: объект Response с результатом DELETE-запроса. """
        try:
            url = f"{config.API_URL}{config.CART}"
            return requests.delete(url, headers=self._headers)
        except Exception as e:
            pytest.fail(f"Ошибка очистки корзины: {e}")
