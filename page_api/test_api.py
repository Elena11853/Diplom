import pytest
import allure
from page import Page


page = Page()

# id товара в каталоге
@pytest.fixture
def product_id():
    """Фикстура возвращает фиксированный ID товара."""
    return 2968841

# Фикстура добавляет товар в корзину и возвращает его id в корзине (не тот что в каталоге)
@pytest.fixture
def cart_product_id(product_id):
    """ Фикстура сначала добавляет товар в корзину, 
    затем находит его внутренний ID в корзине 
    по внешнему ID. 
    Используется во многих последующих тестах. """
    # добавляем товар
    page.add_product_to_cart(product_id)
    # Находим id товара в корзине по его id из каталога
    return page.get_cart_product_id(product_id)

@allure.epic("API Тестирование")
@allure.feature("Корзина товаров")
@allure.story("Добавление товара в корзину")
@allure.title("Успешное добавление товара в корзину")
@allure.description("Проверка, что товар добавляется в корзину без ошибок.")
def test_add_product(product_id):
    """ Тест проверяет успешное добавление товара в корзину. 
    Сначала убеждается, что товара ещё нет в корзине, 
    затем добавляет его и снова проверяет наличие. """
    with allure.step("Проверяем, что товара в корзине нет"):
        test_cart_product_id = page.get_cart_product_id(product_id)
        assert test_cart_product_id is None, 'Товар уже есть в корзине'

    with allure.step("Добавляем товар в корзину"):
        response = page.add_product_to_cart(product_id)
        assert response.status_code == 200, 'Ошибка запроса'
    
    with allure.step("Проверяем, что товар появился в корзине"):
        test_cart_product_id = page.get_cart_product_id(product_id)
        assert test_cart_product_id is not None, 'Товар не появился в корзине'

@allure.epic("API Тестирование")
@allure.feature("Корзина товаров")
@allure.story("Удаление товара из корзины")
@allure.title("Успешное удаление товара из корзины")
@allure.description("Проверка возможности удалить товар из корзины.")
def test_delete_product(product_id, cart_product_id):
    """ Тест проверяет возможность успешного 
    удаления товара из корзины. Сначала убеждается, 
    что товар присутствует в корзине, 
    затем удаляет его и проверяет отсутствие. """
    with allure.step("Проверяем, что товар доступен в корзине"):
        test_cart_product_id = page.get_cart_product_id(product_id)
        assert test_cart_product_id is not None, 'Товара нет в корзине'

    with allure.step("Удаляем товар из корзины"):
        response = page.delete_product(cart_product_id)
        assert response.status_code >= 200 and response.status_code < 300, 'Ошибка запроса'

    with allure.step("Проверяем, что товара больше нет в корзине"):
        test_cart_product_id = page.get_cart_product_id(product_id)
        assert test_cart_product_id is None, 'Товар всё ещё находится в корзине'

@allure.epic("API Тестирование")
@allure.feature("Корзина товаров")
@allure.story("Восстановление товара в корзине")
@allure.title("Успешное восстановление удалённого товара")
@allure.description("Проверка возможности восстановить удаленный товар в корзину.")
def test_restore_product(product_id, cart_product_id):
    """ Тест проверяет успешность восстановления 
    удаленного товара в корзину. Сначала удаляется товар, 
    затем восстанавливается и проверяется его присутствие. """
    with allure.step("Удаляем товар из корзины"):
        page.delete_product(cart_product_id)

    with allure.step("Проверяем, что товара больше нет в корзине"):
        test_cart_product_id = page.get_cart_product_id(product_id)
        assert test_cart_product_id is None, 'Товар всё ещё находится в корзине'

    with allure.step("Восстанавливаем товар в корзину"):
        response = page.restore_product(cart_product_id)
        assert response.status_code >= 200 and response.status_code < 300, 'Ошибка запроса'

    with allure.step("Проверяем, что товар восстановлен в корзине"):
        test_cart_product_id = page.get_cart_product_id(product_id)
        assert test_cart_product_id is not None, 'Товар не восстановился в корзине'

@allure.epic("API Тестирование")
@allure.feature("Корзина товаров")
@allure.story("Просмотр содержимого корзины")
@allure.title("Успешное получение содержимого корзины")
@allure.description("Проверка правильности отображения содержимого корзины.")
def test_get_cart():
    """ Тест проверяет успешное получение содержимого корзины. 
    Убедимся, что запрос выполнен успешно 
    и данные возвращаются в виде массива продуктов. """
    with allure.step("Запрашиваем содержимое корзины"):
        response = page.get_cart()
        assert response.status_code >= 200 and response.status_code < 300, 'Ошибка запроса'

    with allure.step("Проверяем структуру полученных данных"):
        products = response.json()['products']
        assert isinstance(products, list), 'Данные пришли некорректно'

@allure.epic("API Тестирование")
@allure.feature("Корзина товаров")
@allure.story("Очистка корзины")
@allure.title("Успешная очистка корзины")
@allure.description("Проверка полного удаления всех товаров из корзины.")
def test_clear_cart(cart_product_id):
    """ Тест проверяет успешность полной очистки корзины. 
    Сначала убеждаемся, что в корзине есть хотя бы один товар, 
    затем очищаем её и проверяем пустоту. """
    with allure.step("Проверяем, что в корзине есть товар"):
        assert cart_product_id is not None, "Товара нет в корзине"

    with allure.step("Очищаем корзину"):
        response = page.clear_cart()
        assert response.status_code >= 200 and response.status_code < 300, 'Ошибка запроса'

    with allure.step("Проверяем, что корзина стала пустой"):
        cart_response = page.get_cart()
        assert len(cart_response.json()['products']) == 0, 'Товары остались в корзине'
