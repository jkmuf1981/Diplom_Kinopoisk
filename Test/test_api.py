import requests
import allure
import pytest
from Diplom_Kinopoisk.settings  import (
    API_URL, TOKEN, INVALID_TOKEN,
    API_ENDPOINT_RANDOM_MOVIE, API_ENDPOINT_MOVIE, API_ENDPOINT_PERSON,
    TEST_MOVIE_ID, TEST_PERSON_ID, EXPECTED_MOVIE_NAME, EXPECTED_PERSON_NAME,
    API_HEADER_KEY, API_RESPONSE_NAMES_KEY, API_RESPONSE_NAME_KEY
)



@pytest.fixture(scope="module")
def api_client():
    return requests.Session()



@allure.feature('API Tests')
class TestAPITests:


    @allure.story("Получение списка фильмов")
    def test_get_films_list(self, api_client):
        """Тест проверяет получение списка фильмов"""
        response = api_client.get(API_URL + API_ENDPOINT_RANDOM_MOVIE, headers={API_HEADER_KEY: TOKEN})
        data = response.json()
        assert response.status_code == 200, f"Ошибка HTTP: {response.status_code}, Текст: {response.text}"
        assert len(data[API_RESPONSE_NAMES_KEY]) > 0, "Список фильмов пуст"


    @allure.story("Получение рандомного списка фильмов ")
    def test_get_films_list_notoken(self, api_client):
        """Тест проверяет получение списка фильмов"""
        response = api_client.get(API_URL + API_ENDPOINT_RANDOM_MOVIE)
        assert response.status_code == 401, f"Ошибка HTTP: {response.status_code}, Текст: {response.text}"


    @allure.story("Получение одного фильма")
    def test_get_film(self, api_client):
        """Тест проверяет получение списка фильмов"""
        response = api_client.get(API_URL + API_ENDPOINT_MOVIE.format(TEST_MOVIE_ID), headers={API_HEADER_KEY: TOKEN})
        data = response.json()
        assert response.status_code == 200, f"Ошибка HTTP: {response.status_code}, Текст: {response.text}"
        assert data[API_RESPONSE_NAME_KEY] == EXPECTED_MOVIE_NAME, "Другое название фильма"


    @allure.story("Получение одного фильма c невалидным  токеном")
    def test_get_film_invalidtoken(self, api_client):
        """Тест проверяет получение списка фильмов"""
        response = api_client.get(API_URL + API_ENDPOINT_MOVIE.format(TEST_MOVIE_ID), headers={API_HEADER_KEY: INVALID_TOKEN})
        assert response.status_code == 401, f"Ошибка HTTP: {response.status_code}, Текст: {response.text}"


    @allure.story("Получение данных актёра по ID")
    def test_get_actor(self, api_client):
        """Тест проверяет получение списка фильмов"""
        response = api_client.get(API_URL + API_ENDPOINT_PERSON.format(TEST_PERSON_ID), headers={API_HEADER_KEY: TOKEN})
        data = response.json()
        assert response.status_code == 200, f"Ошибка HTTP: {response.status_code}, Текст: {response.text}"
        assert data[API_RESPONSE_NAME_KEY] == EXPECTED_PERSON_NAME, "Другое имя актёра"
