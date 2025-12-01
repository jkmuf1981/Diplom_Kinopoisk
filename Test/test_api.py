import requests
import allure
import pytest
from Diplom_Kinopoisk.settings import API_URL, TOKEN, INVALID_TOKEN


@pytest.fixture(scope="module")
def api_client():
    return requests.Session()


@allure.feature('API Tests')
class TestAPITests:

    @allure.story("Получение списка фильмов")
    def test_get_films_list(self, api_client):
        """Тест проверяет получение списка фильмов"""
        response = api_client.get(API_URL + 'v1.4/movie/random', headers={'X-API-KEY':  TOKEN})
        data = response.json()
        assert response.status_code == 200, f"Ошибка HTTP: {response.status_code}, Текст: {response.text}"
        assert len(data['names']) > 0, "Список фильмов пуст"

    @allure.story("Получение рандомного списка фильмов ")
    def test_get_films_list_notoken(self, api_client):
        """Тест проверяет получение списка фильмов"""
        response = api_client.get(API_URL + 'v1.4/movie/random')
        assert response.status_code == 401, f"Ошибка HTTP: {response.status_code}, Текст: {response.text}"

    @allure.story("Получение одного фильма")
    def test_get_film(self, api_client):
        """Тест проверяет получение списка фильмов"""
        response = api_client.get(API_URL + 'v1.4/movie/12345', headers={'X-API-KEY': TOKEN})
        data = response.json()
        assert response.status_code == 200, f"Ошибка HTTP: {response.status_code}, Текст: {response.text}"
        assert data['name'] == "Ночь страха", "Другое название фильма"

    @allure.story("Получение одного фильма c невалидным  токеном")
    def test_get_film_invalidtoken(self, api_client):
        """Тест проверяет получение списка фильмов"""
        response = api_client.get(API_URL + 'v1.4/movie/12345', headers={'X-API-KEY': INVALID_TOKEN})
        assert response.status_code == 401, f"Ошибка HTTP: {response.status_code}, Текст: {response.text}"

    @allure.story("Получение данных актёра по ID")
    def test_get_actor(self, api_client):
        """Тест проверяет получение списка фильмов"""
        response = api_client.get(API_URL + 'v1.4/person/54321', headers={'X-API-KEY': TOKEN})
        data = response.json()
        assert response.status_code == 200, f"Ошибка HTTP: {response.status_code}, Текст: {response.text}"
        assert data['name'] == "Энн Лайонс", "Другое имя актёра"

