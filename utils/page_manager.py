# utils/page_manager.py
from functools import cached_property
from playwright.sync_api import Page
from pages.cart_page import CartPage
# Import other page classes as you add them
# from pages.checkout_page import CheckoutPage
# from pages.login_page import LoginPage

class PageManager:
    def __init__(self, page: Page):
        self.page = page

    @cached_property
    def cart_page(self) -> CartPage:
        """Cached property - creates CartPage once and reuses it"""
        return CartPage(self.page)

    # Add other page properties as needed
    # @cached_property
    # def checkout_page(self) -> CheckoutPage:
    #     return CheckoutPage(self.page)

    # @cached_property
    # def login_page(self) -> LoginPage:
    #     return LoginPage(self.page)