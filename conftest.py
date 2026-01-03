import os

import pytest
from playwright.sync_api import sync_playwright

BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com/")


@pytest.fixture(scope="session")
def base_url() -> str:
    return BASE_URL


@pytest.fixture()
def page():
    """
    Создаёт новый контекст/страницу на каждый тест.
    HEADLESS можно переопределить через переменную окружения (по умолчанию 1).
    """
    headless_env = os.getenv("HEADLESS", "1").strip()
    headless = headless_env not in ("0", "false", "False", "no", "No")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context()
        page = context.new_page()
        yield page
        context.close()
        browser.close()
