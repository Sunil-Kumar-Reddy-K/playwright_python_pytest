from playwright.sync_api import Page
from utils.config import Config


class CartPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = Config.UI_BASE_URL
        self.add_to_cart_btn = page.locator("text=ADD TO CART").first
        self.cart_icon = page.locator(".cart-icon")

    def navigate(self):
        self.page.goto(self.url)

    def add_item_to_cart(self):
        self.add_to_cart_btn.click()

    def go_to_cart(self):
        self.cart_icon.click()

    def proceed_to_checkout(self):
        self.page.locator("text=PROCEED TO CHECKOUT").click()
        self.page.wait_for_load_state("load")
        self.page.locator("text=PLACE ORDER").wait_for(state="visible")
