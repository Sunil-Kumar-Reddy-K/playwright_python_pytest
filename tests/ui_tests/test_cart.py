import allure
import pytest
from pages.cart_page import CartPage


@allure.epic("E-Commerce Application")
@allure.feature("Shopping Cart")
@allure.story("Add Items to Cart")
@allure.title("Verify user can add items to cart - {config.current_env}")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.ui_tests
@pytest.mark.all_tests
def test_add_item_to_cart(pages, soft_assert, page: CartPage):
    pages.cart_page.navigate()
    pages.cart_page.add_item_to_cart()
    pages.cart_page.go_to_cart()
    pages.cart_page.proceed_to_checkout()
    soft_assert.assert_contains(page.url, "cart", "Failed to navigate to cart page")
    # assert "cart" in page.url, "Failed to navigate to cart page"
    print("The page url is ", page.url)

    soft_assert.assert_all()

# @allure.title("Test adding item to cart")
# @allure.description("This test verifies that user can add an item to the shopping cart")
# @allure.tag("smoke", "cart", "ui")
# def test_add_item_to_cart(self, page: CartPage):
#     with allure.step("Navigate to the shopping page"):
#         page.goto("https://rahulshettyacademy.com/seleniumPractise/")
#
#     with allure.step("Add first item to cart"):
#         add_to_cart_btn = page.locator("text=ADD TO CART").first
#         add_to_cart_btn.click()
#
#     with allure.step("Verify item is added to cart"):
#         cart_count = page.locator(".cart-info tbody tr").count()
#         assert cart_count > 0, "Cart should have at least one item"
