import allure
import pytest
from playwright.sync_api import expect

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


@allure.feature("Authorization")
@allure.suite("Login tests")
class TestLogin:
    @allure.title("Успешный логин standard_user / secret_sauce")
    def test_success_login_standard_user(self, page, base_url):
        login = LoginPage(page, base_url)
        login.open_login()

        login.login("standard_user", "secret_sauce")

        inventory = InventoryPage(page, base_url)
        inventory.expect_opened()

    @allure.title("Логин с неверным паролем")
    def test_login_wrong_password(self, page, base_url):
        login = LoginPage(page, base_url)
        login.open_login()

        login.login("standard_user", "wrong_password")

        # Остаёмся на странице логина
        expect(page).to_have_url(base_url)
        login.expect_error_visible()
        login.expect_error_text_contains("Username and password do not match")

    @allure.title("Логин заблокированного пользователя locked_out_user")
    def test_login_locked_out_user(self, page, base_url):
        login = LoginPage(page, base_url)
        login.open_login()

        login.login("locked_out_user", "secret_sauce")

        expect(page).to_have_url(base_url)
        login.expect_error_visible()
        login.expect_error_text_contains(
            "Sorry, this user has been locked out")

    @allure.title("Логин с пустыми полями")
    @pytest.mark.parametrize(
        "username,password,expected_error",
        [
            ("", "", "Username is required"),
            ("standard_user", "", "Password is required"),
            ("", "secret_sauce", "Username is required"),
        ],
    )
    def test_login_empty_fields(self, page, base_url, username, password, expected_error):
        login = LoginPage(page, base_url)
        login.open_login()

        login.login(username, password)

        expect(page).to_have_url(base_url)
        login.expect_error_visible()
        login.expect_error_text_contains(expected_error)

    @allure.title("Логин performance_glitch_user: переход корректный даже при задержках")
    def test_login_performance_glitch_user(self, page, base_url):
        login = LoginPage(page, base_url)
        login.open_login()

        login.login("performance_glitch_user", "secret_sauce")

        # Увеличиваем терпение к задержкам (глитч может быть медленный)
        page.set_default_timeout(15_000)

        inventory = InventoryPage(page, base_url)
        inventory.expect_opened()
