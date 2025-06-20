# 🎭 Playwright Python Pytest Framework

A comprehensive hybrid automation framework for UI and API testing using Playwright and pytest.

## 📋 Table of Contents

- [Initial Setup](#-initial-setup)
- [Development Environment](#-development-environment)
- [Test Execution](#-test-execution)
- [Testing Resources](#-testing-resources)
- [Troubleshooting](#-troubleshooting)

## 🚀 Initial Setup

### Prerequisites

- Python 3.8 or higher
- Git
- VS Code (recommended IDE)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd playwright-framework
   ```

2. **Create and activate virtual environment**
   ```bash
   # Create virtual environment
   python -m venv .venv
   
   # Activate virtual environment
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers**
   ```bash
   playwright install
   ```

5. **Verify installation**
   ```bash
   pytest --version
   playwright --version
   ```

## 💻 Development Environment

### IDE Restart Workflow

When restarting your IDE, always activate the virtual environment first:

```bash
.venv\Scripts\activate
```

### Project Structure

```
playwright-framework/
├── .venv/                          # Virtual environment
├── allure-results/                 # Allure report
├── pages/                          # Page object models
├── apis/                           # API client 
├── tests/
│   ├── ui_tests/                   # UI test files
│   ├── api_tests/                  # API test files
│   └── conftest.py                 # Pytest configuration
├── utils/                          # Utility functions
|   ├── config.py                   # Configuration
|   └── report_generator.py         # Report generator
|   └── soft_assert.py              # Soft assertion
├── allure.properties               # Allure settings
├── playwright/                     # Legacy test location
├── rahulShettyPlaywrightBasicsFromUdemy/  # Learning examples
├── requirements.txt                # Python dependencies
└── pytest.ini                     # Pytest settings
```

## 🧪 Test Execution

### Basic Test Execution

#### Run all tests

```bash
pytest
```

#### Run tests with browser visible (headed mode)

```bash
pytest --headed
```

#### Run specific test categories

```bash
# UI tests only
pytest -m ui

# API tests only  
pytest -m api
```

### Specific Test Execution

#### Run a specific test file

```bash
pytest playwright/test_riverside_BDI3.py --headed
```

#### Run a specific test method

```bash
pytest playwright/test_riverside_BDI3.py::test_login_BDI3 --headed
```

#### Run raw Python scripts

```bash
python rahulShettyPlaywrightBasicsFromUdemy/first.py
```

### 🐛 Debug Mode

#### PowerShell (Recommended)

```powershell
$env:PWDEBUG=1; pytest playwright/test_riverside_BDI3.py::test_login_BDI3 -s
```

#### Command to run in regular mode (Non-debug)

*Just dont add that "set PWDEBUG"*

```cmd
pytest tests/ui_tests/test_cart.py -s & allure serve allure-results

pytest tests -m all -s & allure serve allure-results
```

#### Debug with Allure Report

```cmd
set PWDEBUG=1 & pytest tests/ui_tests/ -m ui -s & allure serve allure-results
```

### 📊 Reporting Options

#### Generate Allure Report

```bash
# Run tests and generate Allure results
pytest --alluredir=allure-results

# Serve the report in browser
allure serve allure-results
```

#### HTML Report

```bash
pytest --html=report.html --self-contained-html
```

#### JUnit XML Report

```bash
pytest --junitxml=report.xml
```

## 🌐 Testing Resources

### Test Applications

| Type            | URL                                                                     | Purpose                           |
|-----------------|-------------------------------------------------------------------------|-----------------------------------|
| **UI Testing**  | [Selenium Practice](https://rahulshettyacademy.com/seleniumPractise/#/) | E-commerce UI automation practice |
| **API Testing** | [Notes API](https://practice.expandtesting.com/notes/api/api-docs/)     | RESTful API testing scenarios     |

### Useful Playwright Commands

```bash
# Generate test code from browser interactions
playwright codegen https://example.com

# Run tests in different browsers
pytest --browser chromium
pytest --browser firefox  
pytest --browser webkit

# Run tests in parallel
pytest -n auto  # Requires pytest-xdist

# Run tests with specific timeout
pytest --timeout=60
```

## 🔧 Troubleshooting

### Common Issues

**Virtual Environment Not Activated**

```bash
# Symptoms: Command not found errors
# Solution: Always activate first
.venv\Scripts\activate
```

**Browser Installation Issues**

```bash
# Reinstall browsers
playwright install --force
```

**Port Conflicts**

```bash
# Kill processes using specific ports
netstat -ano | findstr :8080
taskkill /PID <process_id> /F
```

**Module Import Errors**

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Performance Tips

- Use `--headed` only when debugging
- Implement page object models for better maintainability
- Use fixtures for common setup/teardown operations
- Enable parallel execution for faster test runs
- Implement proper waits instead of sleep statements

### Best Practices

1. **Test Organization**: Group related tests in classes
2. **Data Management**: Use external files for test data
3. **Error Handling**: Implement proper exception handling
4. **Logging**: Add comprehensive logging for debugging
5. **CI/CD Integration**: Configure for continuous integration

## 📝 Additional Notes

- Always commit your `requirements.txt` when adding new dependencies
- Use meaningful test names that describe what is being tested
- Implement proper assertions with clear error messages
- Consider using environment variables for sensitive data
- Regular maintenance of test data and test environments