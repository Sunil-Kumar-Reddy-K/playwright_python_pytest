import allure
import pytest
from pages.cart_page import CartPage


@allure.epic("E-Commerce Application")
@allure.feature("Shopping Cart")
@allure.story("Add Items to Cart")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.ui
@pytest.mark.all
def test_add_item_to_cart(page, soft_assert, pages):
    pages.cart_page.navigate()
    pages.cart_page.add_item_to_cart()
    pages.cart_page.go_to_cart()
    pages.cart_page.proceed_to_checkout()
    soft_assert.assert_contains(page.url, "cart", "Failed to navigate to cart page")
    # assert "cart" in page.url, "Failed to navigate to cart page"
    print("The page url is ", page.url)

    soft_assert.assert_all()
