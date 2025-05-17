from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure

class SearchPage:
    def __init__(self, driver):
        """Инициализация класса SearchPage с драйвером и временем ожидания.

        Args:
            driver (WebDriver): Драйвер Selenium для управления браузером.
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 60)

    @allure.step("поиск элемента по селектору `{selector}` с ожиданием появления его на странице")
    def find_element(self, method, selector):
        """
        Поиск первого на странице элемента по селектору с ожиданием
        Args:
            method: способ поиска (например By.CSS_SELECTOR)
            selector: строка для поиска (например `.my-selector`)
        """
        return self.wait.until(EC.visibility_of_element_located((method, selector)))

    @allure.step("Ожидание загрузки каталога")
    def wait_for_catalog(self):
        """Явное ожидание появления блока каталога на странице."""
        return self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'app-catalog__content')))

    @allure.step("Ожидание загрузки каталога")
    def wait_for_catalog_stub(self):
        """Явное ожидание появления блока с ошибкой поиска на странице."""
        return self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'catalog-stub')))

    @allure.step("Открытие URL")
    def open(self, url):
        """Открыть указанную URL-адрес в браузере.

        Args:
            url (str): URL-адрес для открытия.
        """
        self.driver.get(url)

    @allure.step("Ввод поискового запроса книги '{query}'")
    def enter_search_query(self, query: str):
        """Вводить текстовое сообщение в поле поиска.

        Args:
            query (str): Запрос для поиска.
        """
        input = self.find_element(By.CLASS_NAME, 'search-form__input')
        input.click()
        input.send_keys(query)

    @allure.step("Нажатие кнопки поиска")
    def click_search_button(self):
        """Нажать на кнопку поиска."""
        search_button = self.find_element(By.CLASS_NAME, "search-form__button-search")
        search_button.click()

    @allure.step("Получение названий книг")
    def get_book_titles(self):
        """Получить названия всех продуктов на странице результатов поиска.

        Returns:
            list: Список названий продуктов.
        """

        # ожидаем пока загрузится каталог
        self.wait_for_catalog()

        catalog = self.find_element(By.CLASS_NAME, 'app-catalog__content')
        product_titels = catalog.find_elements(By.CLASS_NAME, "product-card__title")

        return [title.text.strip().lower() for title in product_titels]

    @allure.step("Получение названий авторов")
    def get_author_titles(self):
        """Получить имена всех авторов на странице результатов поиска.

        Returns:
            list: Список имен авторов.
        """
        # ожидаем пока загрузится каталог
        self.wait_for_catalog()

        catalog = self.find_element(By.CLASS_NAME, 'app-catalog__content')
        author_titels = catalog.find_elements(By.CLASS_NAME, "product-card__subtitle")
        return [author.text.strip().lower() for author in author_titels]

    @allure.step("Проверка сообщения об отсутствии результатов")
    def get_no_results_message(self):
        """Проверить и вернуть сообщение об отсутствии результатов поиска.

        Returns:
            str: Сообщение об отсутствии результатов.
        """
        # ожидаем загрузки блока с ошибкой поиска
        self.wait_for_catalog_stub()

        no_result_text = self.driver.find_element(By.CLASS_NAME, "catalog-stub__title")
        return no_result_text.text.strip().lower()
    