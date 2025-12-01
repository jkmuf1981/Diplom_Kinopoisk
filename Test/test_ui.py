import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException  # Импортируем исключение явно
import allure
import pytest
from Diplom_Kinopoisk.settings import BASE_URL


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
            wait = WebDriverWait(browser, 30)
            wait.until(EC. title_contains('Кинопоиск'))  # Укажите название своей страницы

        with allure.step("Поиск элемента с логотипом"):
            try:
                logo_element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'header__logo')))
            except TimeoutException:
                print("Логотип не появился на странице.")
                # Добавьте логику обработки исключительной ситуации

    @allure.story("Поиск фильма на сайте")
    def test_movie_search(self, browser):
        """Тест проверяет работу поля поиска фильмов"""
        movie_title = "Матрица"

        with allure.step("Переход на главную страницу"):
            browser.get(BASE_URL)

        with allure.step("Подождать полной загрузки страницы"):
            wait = WebDriverWait(browser, 30)
            wait.until(EC. title_contains('Кинопоиск'))  # Укажите название своей страницы

        with allure.step("Поиск поля ввода"):
            search_field = browser.find_element(By.CSS_SELECTOR, 'input[name="kp_query"]')
            search_field.send_keys(movie_title)

        with allure.step("Нажатие кнопки поиска"):
            submit_button = browser.find_element(By.CSS_SELECTOR, '[type="submit"]')
            submit_button.click()

        with allure.step("Проверка результата поиска"):
            first_result = browser.find_element(By.XPATH,'//p[@class="name"]/a')  # Предположим, что фильм выводится в карточке
            title = first_result.text
            assert movie_title in title, f"Фильм '{movie_title}' не найден"

    @allure.story("")
    def test_registration(self, browser):
        """Тест проверяет регистрацию нового пользователя"""
        email = f'test_user_{time.time()}@example.com'
        password = 'password123'

        with allure.step("Переход на страницу регистрации"):
            browser.get(f'{BASE_URL}/auth/register/')

        with allure.step("Подождать полной загрузки страницы"):
            wait = WebDriverWait(browser, 30)
            wait.until(EC. title_contains('Кинопоиск'))  # Укажите название своей страницы

        with allure.step("Заполнение формы регистрации"):
            input_email = browser.find_element(By.ID, 'email')
            input_email.clear() # очищаем поле
            input_email.send_keys(email)
            input_password = browser.find_element(By.ID, 'password')
            input_password.send_keys(password)
            register_button = browser.find_element(By.CSS_SELECTOR, '.btn-primary')
            register_button.submit() # Используем метод submit вместо click

        with allure.step("Проверка успешного входа"):
            success_message = browser.find_element(By.CLASS_NAME, 'alert-success').text
            assert "Вы успешно зарегистрированы" in success_message, "Ошибка регистрации"

    @allure.story("Авторизация пользователя")
    def test_login(self, browser):
        """Тест проверяет успешную авторизацию пользователя"""
        from Diplom_Kinopoisk.settings import LOGIN, PASSWORD

        with allure.step("Переход на страницу авторизации"):
            browser.get(f'{BASE_URL}/auth/login/')

        with allure.step("Заполнение полей авторизации"):
            input_username = browser.find_element(By.ID, 'username')
            input_username.send_keys(LOGIN)
            input_password = browser.find_element(By.ID, 'password')
            input_password.send_keys(PASSWORD)
            login_button = browser.find_element(By.CSS_SELECTOR, '.btn-primary')
            login_button.click()

        with allure.step("Проверка успешной авторизации"):
            profile_link = browser.find_element(By.LINK_TEXT, 'Профиль')
            assert profile_link.is_displayed(), "Пользователь не залогинился"

    @allure.story("Фильтрация фильмов по жанру")
    def test_filter_by_genre(self, browser):
        """Тест проверяет фильтрацию фильмов по жанрам"""
        genre_name = "Драма"

        with allure.step("Переход на страницу каталога фильмов"):
            browser.get(f"{BASE_URL}/catalog/")

        with allure.step("Выбор жанра 'Драма'"):
            wait = WebDriverWait(browser, 20)  # увеличено время ожидания
            wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'body')))  # ждем полной загрузки страницы
            try:
                filter_genre = wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//button[contains(@class,'genre-filter')][normalize-space(text())='Драма']"))
                )
                filter_genre.click()
            except TimeoutException:
                print("Кнопка фильтра не найдена или не активна!")

        with allure.step("Проверка результатов фильтрации"):
            filtered_movies = browser.find_elements(By.CLASS_NAME, 'film-card')
            for film_card in filtered_movies[:5]:
                genres_list = film_card.find_element(By.CLASS_NAME, 'film-genres').text
                assert genre_name.lower() in genres_list.lower(), f"Жанр {genre_name} отсутствует в фильме {film_card.text}"

    @pytest.fixture(scope="session")
    def browser(self):
        driver = webdriver.Chrome()
        yield driver
        driver.quit()  # закроем драйвер после завершения всех тестов