import allure
from playwright.sync_api import Page, expect

from .base_page import BasePage


class LoginPage(BasePage):
    URL_PATH = "/"

    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)

        # Локаторы
        self.username = page.locator("#user-name")
        self.password = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error_box = page.locator("[data-test='error']")
        self.login_logo = page.locator(".login_logo")

    @allure.step("Открыть страницу логина")
    def open_login(self) -> None:
        self.open(self.base_url)
        # Проверяем URL и ключевые элементы страницы
        expect(self.page).to_have_url(self.base_url)
        expect(self.login_logo).to_be_visible()
        expect(self.username).to_be_visible()
        expect(self.password).to_be_visible()
        expect(self.login_button).to_be_visible()

    @allure.step("Ввести username: {username}")
    def fill_username(self, username: str) -> None:
        self.username.fill(username)

    @allure.step("Ввести password: {password}")
    def fill_password(self, password: str) -> None:
        self.password.fill(password)

    @allure.step("Нажать Login")
    def submit(self) -> None:
        self.login_button.click()

    @allure.step("Логин: {username} / {password}")
    def login(self, username: str, password: str) -> None:
        self.fill_username(username)
        self.fill_password(password)
        self.submit()

    @allure.step("Проверить, что показана ошибка логина")
    def expect_error_visible(self) -> None:
        expect(self.error_box).to_be_visible()

    @allure.step("Проверить текст ошибки: {text}")
    def expect_error_text_contains(self, text: str) -> None:
        expect(self.error_box).to_contain_text(text)
