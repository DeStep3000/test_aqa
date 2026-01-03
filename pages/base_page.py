import re

from playwright.sync_api import Page, expect


class BasePage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    def open(self, url: str) -> None:
        self.page.goto(url, wait_until="domcontentloaded", timeout=60_000)

    def expect_url_contains(self, part: str) -> None:
        pattern = re.compile(rf".*{re.escape(part)}.*")
        expect(self.page).to_have_url(pattern)

    def expect_visible(self, locator):
        expect(locator).to_be_visible()

    def expect_text(self, locator, text: str) -> None:
        expect(locator).to_have_text(text)
