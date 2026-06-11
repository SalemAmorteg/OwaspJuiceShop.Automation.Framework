# 🚀 OWASP Juice Shop QA Automation Platform

A production-style QA Automation framework built against the OWASP Juice Shop application using **Python**, **Playwright**, **Pytest**, and **C# Playwright**.

This project demonstrates modern Quality Engineering practices including:

* UI Automation
* API Testing
* Database Validation
* Page Object Model (POM)
* Cross-language automation architecture
* CI/CD readiness
* Playwright best practices
* Scalable test framework design

The goal of this repository is not simply to automate test cases, but to showcase how a real-world QA Automation framework can be structured, maintained, and extended.

---

# 📋 Project Overview

OWASP Juice Shop is an intentionally vulnerable e-commerce application widely used for security awareness, testing practice, and automation learning.

This repository contains two complementary automation implementations:

| Framework           | Purpose                                                  |
| ------------------- | -------------------------------------------------------- |
| Python + Playwright | Primary automation framework                             |
| C# + Playwright     | Cross-language validation and architecture demonstration |

The Python framework contains the majority of the automated coverage, while the C# framework demonstrates equivalent automation patterns in a .NET ecosystem.

---

# 🏗 Architecture

```text
automation_juice_shop/
│
├── python/
│   ├── api_suite/
│   ├── ui_suite/
│   └── shared_utils/
│
├── csharp/
│
├── juice-shop-env/
│   └── docker-compose.yml
│
└── README.md
```

---

# 🧩 Technology Stack

## UI Automation

* Playwright
* Pytest
* Page Object Model (POM)

## API Testing

* Requests
* Pytest
* Pydantic

## Database Validation

* SQLite

## Reporting & Debugging

* Playwright Traces
* Screenshots
* Videos

## Secondary Framework

* C#
* .NET
* Microsoft Playwright

---

# 📂 Python Framework Structure

```text
python/
│
├── api_suite/
│   ├── clients/
│   ├── models/
│   ├── tests/
│   └── utils/
│
├── ui_suite/
│   ├── pages/
│   ├── tests/
│   └── artifacts/
│
└── shared_utils/
```

### Design Principles

* Page Object Model
* Reusable fixtures
* Separation of concerns
* Test independence
* Maintainable locator strategy
* Web-first assertions

---

# 🎭 Playwright Best Practices

The framework follows modern Playwright recommendations:

✅ Role-based locators

```python
page.get_by_role("button", name="Login")
```

✅ Label locators

```python
page.get_by_label("Email")
```

✅ Test ID locators

```python
page.get_by_test_id("add-to-cart")
```

🚫 Avoided practices

* XPath locators
* Hard waits
* Thread sleeps
* Brittle CSS selectors

---

# 🧪 Test Coverage

## UI Tests

Current automated user flows include:

* User Login
* Product Search
* Product Details
* Shopping Cart
* Checkout Flow
* Order Validation

## API Tests

Coverage includes:

* User Authentication
* Product Endpoints
* Basket Operations
* Response Validation
* Contract Validation with Pydantic

## Database Validation

The framework validates application state directly against the database when appropriate.

Examples include:

* User creation verification
* Product validation
* Cart verification
* Order verification

---

# 🔍 Validation Layers

Instead of relying only on UI assertions, the framework validates functionality at multiple levels:

```text
UI Layer
    ↓
API Layer
    ↓
Database Layer
```

This approach increases confidence in test results and helps identify issues closer to their root cause.

---

# 🎥 Test Artifacts

When tests fail, the framework can generate:

* Screenshots
* Videos
* Playwright Traces

Artifacts are stored under:

```text
python/ui_suite/artifacts/
├── screenshots/
├── traces/
└── videos/
```

---

# 🐳 Running Juice Shop

Start the application using Docker:

```bash
cd juice-shop-env

docker compose up -d
```

Verify the application is available:

```text
http://localhost:3000
```

---

# ⚙️ Local Setup

## Clone Repository

```bash
git clone <repository-url>

cd automation_juice_shop
```

## Create Virtual Environment

```bash
python -m venv .venv

source .venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Install Playwright Browsers

```bash
playwright install
```

---

# ▶️ Running Tests

## Run Entire Python Suite

```bash
pytest
```

## Run UI Tests

```bash
pytest python/ui_suite/tests
```

## Run API Tests

```bash
pytest python/api_suite/tests
```

## Run Specific Test

```bash
pytest test_cart.py -v
```

---

# 📦 requirements.txt

Core dependencies:

```text
playwright
pytest
pytest-playwright
pytest-base-url
pytest-xdist
requests
pydantic
email-validator
python-slugify
```

---

# 🛠 Current Python Dependencies

The framework currently uses:

* playwright
* pytest
* pytest-playwright
* pytest-base-url
* pytest-xdist
* requests
* pydantic
* email-validator
* python-slugify

Additional packages are installed automatically as transitive dependencies.

---

# 📈 Future Enhancements

Potential future improvements include:

* Allure reporting
* GitHub Actions CI/CD pipelines
* Security testing suite
* Performance testing
* Test data management layer
* Dockerized test execution
* Unified reporting dashboard

---

# 👥 Authors & Contributors

### Miguel Bautista Gómez
QA Automation Engineer specializing in Python, Playwright, UI Automation, Framework Design, and Database Validation.

### Natalia Molina
QA Automation Engineer specializing in Python, API Testing, Contract Validation, and Quality Engineering.

### Salem Amortegui
QA Automation Engineer specializing in C#, Playwright, CI/CD, Cross-Language Automation Architecture, and Test Infrastructure.

---

This project was built collaboratively to demonstrate modern QA Automation practices, scalable framework design, and production-style quality engineering workflows.

---

# 📄 License

This project is intended for educational and portfolio purposes.
