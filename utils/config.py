# utils/config.py
import os
from typing import Dict, Any, TypedDict


class EnvironmentConfig(TypedDict):
    """Type definition for environment configuration"""
    ui_base_url: str
    api_base_url: str
    timeout: int


class Config:
    """Configuration class supporting multiple environments and test types"""

    # Environment configurations with proper typing
    ENVIRONMENTS: Dict[str, EnvironmentConfig] = {
        'qa': {
            'ui_base_url': 'https://rahulshettyacademy.com/seleniumPractise/',
            'api_base_url': 'https://practice.expandtesting.com/notes/api',
            'timeout': 30000,
        },
        'stage': {
            'ui_base_url': 'https://stage.rahulshettyacademy.com/seleniumPractise/',
            'api_base_url': 'https://stage.practice.expandtesting.com/notes/api',
            'timeout': 45000,
        },
        'prod': {
            'ui_base_url': 'https://prod.rahulshettyacademy.com/seleniumPractise/',
            'api_base_url': 'https://prod.practice.expandtesting.com/notes/api',
            'timeout': 60000,
        }
    }

    # Default values
    DEFAULT_ENV = 'qa'
    DEFAULT_TEST_TYPE = 'ui'

    def __init__(self):
        self._current_env = self.DEFAULT_ENV
        self._current_test_type = self.DEFAULT_TEST_TYPE

    def set_environment(self, env: str):
        """Set the current environment"""
        if env.lower() not in self.ENVIRONMENTS:
            raise ValueError(f"Environment '{env}' not supported. Available: {list(self.ENVIRONMENTS.keys())}")
        self._current_env = env.lower()

    def set_test_type(self, test_type: str):
        """Set the current test type"""
        if test_type.lower() not in ['ui', 'api']:
            raise ValueError(f"Test type '{test_type}' not supported. Available: ['ui', 'api']")
        self._current_test_type = test_type.lower()

    @property
    def current_env(self) -> str:
        return self._current_env

    @property
    def current_test_type(self) -> str:
        return self._current_test_type

    @property
    def ui_base_url(self) -> str:
        return self.ENVIRONMENTS[self._current_env]['ui_base_url']

    @property
    def api_base_url(self) -> str:
        return self.ENVIRONMENTS[self._current_env]['api_base_url']

    @property
    def timeout(self) -> int:
        return self.ENVIRONMENTS[self._current_env]['timeout']

    def get_env_config(self) -> EnvironmentConfig:
        """Get complete environment configuration"""
        return self.ENVIRONMENTS[self._current_env]

    def __str__(self):
        return f"Config(env={self._current_env}, test_type={self._current_test_type})"


# Global config instance
config = Config()
