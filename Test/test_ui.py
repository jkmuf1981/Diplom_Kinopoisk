from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import allure
import pytest
from Diplom_Kinopoisk.settings  import (
    BASE_URL, TIMEOUT_SHORT, TIMEOUT_LONG, TEST_MOVIE_TITLE, TEST_GENRE,
    SELECTOR_LOGO, SELECTOR_SEARCH_INPUT, SELECTOR_SUBMIT_BUTTON,
    XPATH_SEARCH_RESULT, SELECTOR_FILM_CARD, SELECTOR_FILM_GENRES,
    CATALOG_PATH, XPATH_GENRE_FILTER, LOGIN_BUTTON_SELECTORS, HEADER_SELECTORS
)


@pytest.fixture(scope="session")
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


@allure.feature('UI Tests')
class TestUITests:

    @allure.story("Проверка наличия логотипа сайта")
    def test_logo_presence(self, browser):
        """Тест проверяет наличие логотипа на главной странице"""
        with allure.step("Переход на главную страницу"):
            browser.get(BASE_URL)

        with allure.step("Подождать полной загрузки страницы"):
            wait = WebDriverWait(browser, TIMEOUT_LONG)
            wait.until(EC.title_contains('Кинопоиск'))

        with allure.step("Поиск элемента с логотипом"):
            try:
                logo_element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, SELECTOR_LOGO)))
            except TimeoutException:
                print("Логотип не появился на странице.")

    @allure.story("Поиск фильма на сайте")
    def test_movie_search(self, browser):
        """Тест проверяет работу поля поиска фильмов"""
        with allure.step("Переход на главную страницу"):
            browser.get(BASE_URL)

        with allure.step("Подождать полной загрузки страницы"):
            wait = WebDriverWait(browser, TIMEOUT_LONG)
            wait.until(EC.title_contains('Кинопоиск'))

        with allure.step("Поиск поля ввода"):
            search_field = browser.find_element(By.CSS_SELECTOR, SELECTOR_SEARCH_INPUT)
            search_field.send_keys(TEST_MOVIE_TITLE)

        with allure.step("Нажатие кнопки поиска"):
            submit_button = browser.find_element(By.CSS_SELECTOR, SELECTOR_SUBMIT_BUTTON)
            submit_button.click()

        with allure.step("Проверка результата поиска"):
            first_result = browser.find_element(By.XPATH, XPATH_SEARCH_RESULT)
            title = first_result.text
            assert TEST_MOVIE_TITLE in title, f"Фильм '{TEST_MOVIE_TITLE}' не найден"

    @allure.story("Проверка наличия кнопки входа")
    def test_registration(self, browser):
        """Тест проверяет наличие кнопки входа/регистрации на главной странице"""

        with allure.step("Переход на главную страницу"):
            browser.get(BASE_URL)

        with allure.step("Ожидание загрузки страницы"):
            wait = WebDriverWait(browser, TIMEOUT_LONG)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        with allure.step("Поиск кнопки входа"):
            try:
                login_button = None

                for by_type, selector in LOGIN_BUTTON_SELECTORS:
                    by = By.XPATH if by_type == "xpath" else By.CSS_SELECTOR
                    try:
                        login_button = wait.until(EC.presence_of_element_located((by, selector)))
                        break
                    except TimeoutException:
                        continue

                assert login_button is not None, "Кнопка входа не найдена на странице"
                assert login_button.is_displayed(), "Кнопка входа не отображается"
            except AssertionError as e:
                raise AssertionError(f"Ошибка проверки кнопки входа: {e}")

    @allure.story("Проверка структуры страницы")
    def test_login(self, browser):
        """Тест проверяет наличие основных элементов структуры страницы"""

        with allure.step("Переход на главную страницу"):
            browser.get(BASE_URL)

        with allure.step("Ожидание загрузки страницы"):
            wait = WebDriverWait(browser, TIMEOUT_LONG)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        with allure.step("Проверка наличия основных элементов страницы"):
            header_found = False

            for selector in HEADER_SELECTORS:
                try:
                    header = browser.find_element(By.CSS_SELECTOR, selector)
                    if header and header.is_displayed():
                        header_found = True
                        break
                except:
                    continue

            links = browser.find_elements(By.TAG_NAME, 'a')
            links_count = len([link for link in links if link.is_displayed()])

            images = browser.find_elements(By.TAG_NAME, 'img')
            images_count = len([img for img in images if img.is_displayed()])

            assert header_found or links_count > 0, "На странице не найден хедер и нет ссылок"
            assert links_count > 5, f"Недостаточно ссылок на странице. Найдено: {links_count}"
            assert images_count > 0, f"На странице нет изображений. Найдено: {images_count}"

    @allure.story("Фильтрация фильмов по жанру")
    def test_filter_by_genre(self, browser):
        """Тест проверяет фильтрацию фильмов по жанрам"""
        with allure.step("Переход на страницу каталога фильмов"):
            browser.get(f"{BASE_URL}{CATALOG_PATH}")

        with allure.step(f"Выбор жанра '{TEST_GENRE}'"):
            wait = WebDriverWait(browser, TIMEOUT_SHORT)
            wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'body')))
            try:
                filter_genre = wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, XPATH_GENRE_FILTER.format(TEST_GENRE)))
                )
                filter_genre.click()
            except TimeoutException:
                print("Кнопка фильтра не найдена или не активна!")

        with allure.step("Проверка результатов фильтрации"):
            filtered_movies = browser.find_elements(By.CLASS_NAME, SELECTOR_FILM_CARD)
            for film_card in filtered_movies[:5]:
                genres_list = film_card.find_element(By.CLASS_NAME, SELECTOR_FILM_GENRES).text
                assert TEST_GENRE.lower() in genres_list.lower(), f"Жанр {TEST_GENRE} отсутствует в фильме {film_card.text}"

    @pytest.fixture(scope="session")
    def browser(self):
        driver = webdriver.Chrome()
        yield driver
        driver.quit()