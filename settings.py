BASE_URL = "https://www.kinopoisk.ru/"
API_URL = 'https://api.poiskkino.dev/'
LOGIN = 'your_login'
PASSWORD = 'your_password'
TOKEN = 'W7SSTQ7-PJWMEC4-N3JWKK0-6E913BW'
INVALID_TOKEN = 'W7SSTQ7-PJWMEC4-N3JWKK0-6E913B0'


TIMEOUT_SHORT = 20
TIMEOUT_LONG = 30


TEST_MOVIE_TITLE = "Матрица"
TEST_GENRE = "Драма"


SELECTOR_LOGO = 'header__logo'
SELECTOR_SEARCH_INPUT = 'input[name="kp_query"]'
SELECTOR_SUBMIT_BUTTON = '[type="submit"]'
XPATH_SEARCH_RESULT = '//p[@class="name"]/a'
SELECTOR_FILM_CARD = 'film-card'
SELECTOR_FILM_GENRES = 'film-genres'


CATALOG_PATH = "/catalog/"
XPATH_GENRE_FILTER = "//button[contains(@class,'genre-filter')][normalize-space(text())='{}']"


LOGIN_BUTTON_SELECTORS = [
    ("xpath", "//button[contains(text(), 'Войти')]"),
    ("xpath", "//a[contains(text(), 'Войти')]"),
    ("css", "[data-tid='header-login-button']"),
    ("css", ".styles_loginButton__*"),
    ("xpath", "//*[contains(@class, 'login') or contains(@class, 'sign-in')]")
]


HEADER_SELECTORS = ['header', '[class*="header"]', '[class*="Header"]', 'nav', '[role="banner"]']


API_ENDPOINT_RANDOM_MOVIE = 'v1.4/movie/random'
API_ENDPOINT_MOVIE = 'v1.4/movie/{}'
API_ENDPOINT_PERSON = 'v1.4/person/{}'


TEST_MOVIE_ID = 12345
TEST_PERSON_ID = 54321
EXPECTED_MOVIE_NAME = "Ночь страха"
EXPECTED_PERSON_NAME = "Энн Лайонс"


API_HEADER_KEY = 'X-API-KEY'
API_RESPONSE_NAMES_KEY = 'names'
API_RESPONSE_NAME_KEY = 'name'