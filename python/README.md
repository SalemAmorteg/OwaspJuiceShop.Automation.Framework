# Primary Test Automation Engine (Python)

This sub-workspace houses the production-grade Playwright Python automation engine, functional API regression layer, and transactional database verification hooks managed by Miguel Bautista. It serves as the primary automation codebase for the platform.

---

## 🛠️ Technical Stack & Framework Specs

*   **UI Automation:** Playwright Python sync API wrapper
*   **Test Runner Engine:** Pytest with structural test decoration
*   **API Verification Client:** Requests library paired with Pydantic/JSON Schema data validation structures
*   **Database Integration:** Native SQLite connectivity utilities
*   **Reporting Integrations:** Allure Reports and Playwright Trace Viewer assets

---

## 📂 Framework Directory Blueprints

The codebase strictly enforces modular architecture isolation to maximize onboarding simplicity and preserve a clean separation of concerns:

```text
python/
├── config/              # Runtime execution profiles and global environment properties
├── data/                # Static serialized test data payloads (JSON)
├── pages/               # Page Object Model (POM) layer abstractions
│   └── components/      # Persistent, global UI sub-components (e.g., Navigation Headers)
├── tests/               # Automated test execution suites
│   ├── api/             # Backend validation, schema checks, and endpoint sanity runs
│   └── ui/              # Structural end-to-end user journey validations
└── utils/               # Decoupled database handler abstractions and API clients
⚙️ Local Installation & Environment Provisioning
Execute these initialization steps sequentially inside your Ubuntu terminal from the /python directory to spin up your local execution workspace:

Initialize the Isolated Virtual Environment:

Bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

2.  **Install Synchronized Dependencies:**
```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

3.  **Provision the Target Playwright Core Browser Binaries:**
```bash
    playwright install --with-deps
    ```

---

## 🧪 Automated Suite Execution Profiles

Manage your active validation routines utilizing `pytest` switches directly within your active virtual environment:

```bash
# Execute the entire UI end-to-end regression sweep
pytest tests/ui/

# Execute targeted backend database data-integrity verification
pytest tests/api/test_db_users.py

# Execute a single UI suite with visible browser rendering (Headed Mode)
pytest tests/ui/test_login.py --headed

# Execute tests and stage reporting data logs for Allure compilation
pytest --alluredir=../allure-results

---

##📐 Python Architecture Guardrails

All contributions to this Python framework must conform strictly to the architectural expectations defined in the global engineering standards:

#1. Locator Strategy Priority Order

Do not utilize brittle CSS selectors, chained parent-child strings, or raw XPath trajectories. Target elements exclusively using semantic, intention-revealing accessors:

page.get_by_role()

page.get_by_test_id()

page.get_by_label()

#2. Composition Over Inheritance (Page Object Model Design)

Persistent global elements—such as the top application header, product search field, and shopping basket counter badge—must be isolated into discrete components within pages/components/. These are composed dynamically into the BasePage constructor, rather than duplicated across standalone page objects or bloatways.

#3. Asynchronous Web-First Assertions

Explicit thread pauses or hardcoded time.sleep() statements are strictly banned because they induce flaky runtime failures in target CI/CD pipelines. All validation checks must utilize Playwright’s auto-waiting web assertions:

expect(locator).to_be_visible()

expect(locator).to_have_text()

expect(locator).to_have_url()

#4. Database Persistence Gates

Tests validating critical mutation flows (such as registration or cart alterations) must verify state transitions directly inside the SQLite storage engine. These database checks must focus strictly on data persistence validation and maintain structural independence from UI implementation details.
