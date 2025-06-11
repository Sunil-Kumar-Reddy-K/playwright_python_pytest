class SoftAssert:
    """
    Custom Soft Assertion class for collecting multiple assertion failures
    and reporting them at the end of the test
    """

    def __init__(self):
        self.errors = []
        self.passed_assertions = 0

    def soft_assert(self, condition, message="Assertion failed"):
        """
        Perform soft assertion - collect failures without stopping execution

        Args:
            condition: Boolean condition to check
            message: Custom error message if assertion fails
        """
        try:
            assert condition, message
            self.passed_assertions += 1
            print(f"✓ PASS: {message}")
        except AssertionError as e:
            error_msg = str(e)
            self.errors.append(error_msg)
            print(f"✗ FAIL: {error_msg}")

    def assert_equal(self, actual, expected, message=None):
        """
        Soft assertion for equality

        Args:
            actual: Actual value
            expected: Expected value
            message: Custom error message
        """
        if message is None:
            message = f"Expected '{expected}', but got '{actual}'"
        self.soft_assert(actual == expected, message)

    def assert_contains(self, container, item, message=None):
        """
        Soft assertion for containment

        Args:
            container: String or list to search in
            item: Item to search for
            message: Custom error message
        """
        if message is None:
            message = f"'{container}' should contain '{item}'"
        self.soft_assert(item in container, message)

    def assert_true(self, condition, message="Expected True"):
        """Soft assertion for truthy values"""
        self.soft_assert(condition is True, message)

    def assert_false(self, condition, message="Expected False"):
        """Soft assertion for falsy values"""
        self.soft_assert(condition is False, message)

    def assert_not_none(self, value, message="Value should not be None"):
        """Soft assertion for non-None values"""
        self.soft_assert(value is not None, message)

    def assert_greater_than(self, actual, expected, message=None):
        """Soft assertion for greater than comparison"""
        if message is None:
            message = f"Expected {actual} to be greater than {expected}"
        self.soft_assert(actual > expected, message)

    def assert_all(self):
        """
        Raise AssertionError with all collected failures
        This should be called at the end of your test
        """
        print(f"\n--- Soft Assertion Summary ---")
        print(f"Passed: {self.passed_assertions}")
        print(f"Failed: {len(self.errors)}")
        print(f"Total: {self.passed_assertions + len(self.errors)}")

        if self.errors:
            error_message = "\n".join([f"  {i + 1}. {error}" for i, error in enumerate(self.errors)])
            raise AssertionError(f"\n{len(self.errors)} Soft assertion failure(s):\n{error_message}")
        else:
            print("✓ All soft assertions passed!")

    def get_error_count(self):
        """Get number of failed assertions"""
        return len(self.errors)

    def get_passed_count(self):
        """Get number of passed assertions"""
        return self.passed_assertions

    def clear_errors(self):
        """Clear all collected errors and reset counters"""
        self.errors.clear()
        self.passed_assertions = 0

    def has_errors(self):
        """Check if there are any assertion failures"""
        return len(self.errors) > 0