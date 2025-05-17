import pytest
from selenium import webdriver
import allure
from search_page_ui import SearchPage


@pytest.fixture(scope="session")
def browser():
    driver = webdriver.Chrome()  # Укажите драйвер
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def search_page(browser):
    page = SearchPage(browser)
    page.open("https://www.chitai-gorod.ru/")
    return page


@allure.epic("UI Тестирование")
@allure.feature("Поиск книжной информации")
@allure.title("Поиск книги по заголовку")
@allure.description(
    "Тест проверяет возможность поиска книги по заголовку 'Айвенго'.")
def test_search_book_by_title(search_page):
    query = 'айвенго'
    search_page.enter_search_query(query)
    search_page.click_search_button()
    product_titles = search_page.get_book_titles()

    with allure.step("Проверяем что результаты поиска на странице есть"):
        assert len(product_titles) > 0, "Нет результатов поиска"
    with allure.step("проверяем что поиск успешно работает"):
        assert any(query in title for title in product_titles
                   ), "Название книги не найдено в списке продуктов"
    
@allure.epic("UI Тестирование")
@allure.feature("Поиск книжной информации")
@allure.title("Поиск книги с дефисом")
@allure.description(
    "Тест проверяет возможность поиска книги 'Конек-горбунок'.")
def test_search_book_with_hyphen(search_page):
    query = 'Конек-горбунок'
    search_page.enter_search_query(query)
    search_page.click_search_button()
    product_titles = search_page.get_book_titles()
    
    with allure.step("Проверяем что результаты поиска на странице есть"):
        assert len(product_titles) > 0, "Нет результатов поиска"
    with allure.step(
        "Проверяем что поиск работает при наличии спец. символов в названии"
        ):
        assert any(query.lower() in title for title in product_titles
                   ), "Название книги не найдено в списке продуктов"
    
@allure.epic("UI Тестирование")
@allure.feature("Поиск книжной информации")
@allure.title("Поиск по заголовку с использованием числительных")
@allure.description(
    "Тест проверяет возможность поиска книги по заголовку '12 стульев'.")
def test_search_for_a_book_with_numbers_in_the_title(search_page):
    query = '12 стульев'
    search_page.enter_search_query(query)
    search_page.click_search_button()
    product_titles = search_page.get_book_titles()
    
    with allure.step("Проверяем что результаты поиска на странице есть"):
        assert len(product_titles) > 0, "Нет результатов поиска"
    with allure.step("Проверяем что поиск успешен с числом в названии"):
        assert any(query.lower() in title for title in product_titles
                   ), "Название книги не найдено в списке продуктов"

@allure.epic("UI Тестирование")
@allure.feature("Поиск книжной информации")
@allure.title("Поиск автора")
@allure.description(
    "Тест проверяет возможность поиска автора 'Gregory Roberts'.")
def test_search_author_in_english(search_page):
    query = 'Gregory Roberts'
    search_page.enter_search_query(query)
    search_page.click_search_button()
    author_titles = search_page.get_author_titles()
    
    with allure.step("Проверяем что результаты поиска на странице есть"):
        assert len(author_titles) > 0, "Нет результатов поиска"
    with allure.step("Проверяем что успешно ищет автора введенного латиницей"):
        assert any(query.lower() in title for title in author_titles
                   ), "Имя автора не отображается на странице результатов"
    


@allure.epic("UI Тестирование")
@allure.feature("Поиск книжной информации")
@allure.title("Поиск автора по части фамилии")
@allure.description(
    "Тест проверяет поиск автора по части фамилии 'Достоевский'.")
def test_search_author_partial_surname(search_page):
    search_page.enter_search_query('Досто')
    search_page.click_search_button()
    author_titles = search_page.get_author_titles()
    
    with allure.step("Проверяем что результаты поиска на странице есть"):
        assert len(author_titles) > 0, "Нет результатов поиска для автора"
    with allure.step("Проверяем что успешно найден автор по части фамилии"):
        assert any('достоевский' in title for title in author_titles
                   ), "Фамилия автора не отображается на странице результатов"



@allure.epic("UI Тестирование")
@allure.feature("Поиск книжной информации")
@allure.title("Поиск с использованием только знаков препинания")
@allure.description("Тест проверяет обработку поиска, "
                    "состоящего только из знаков препинания.")
def test_search_punctuation_only(search_page):
    search_page.enter_search_query(",,,….!!!")
    search_page.click_search_button()
    message = search_page.get_no_results_message()
    
    with allure.step("Проверка заведомо неуспешного поиска"):
        assert ("похоже, у нас такого нет" in message
                ), "Сообщение об отсутствии результатов не отображается."
    