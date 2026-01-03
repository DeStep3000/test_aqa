import re

import allure
from playwright.sync_api import Page, expect

from .base_page import BasePage


class InventoryPage(BasePage):
    PATH = "/inventory.html"

    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)

        self.inventory_container = page.locator("[data-test='inventory-container']")
        self.products_title = page.locator(".title")  # "Products"
        self.shopping_cart = page.locator("#shopping_cart_container")

    @allure.step("Проверить, что открыта страница каталога (Inventory)")
    def expect_opened(self) -> None:
        expect(self.page).to_have_url(re.compile(r".*/inventory\.html$"))
        expect(self.inventory_container).to_be_visible()
        expect(self.products_title).to_have_text("Products")
        expect(self.shopping_cart).to_be_visible()
