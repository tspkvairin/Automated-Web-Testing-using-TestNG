import os
import logging
from datetime import datetime

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


BASE_URL = "https://the-internet.herokuapp.com"


def _dirs():
    os.makedirs("logs", exist_ok=True)
    os.makedirs("screenshots", exist_ok=True)
    os.makedirs("reports", exist_ok=True)


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def logger():
    _dirs()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = os.path.join("logs", f"run_{ts}.log")

    logger = logging.getLogger("A5")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    fh = logging.FileHandler(log_path, encoding="utf-8")
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    logger.info("=== TEST RUN START ===")
    yield logger
    logger.info("=== TEST RUN END ===")


@pytest.fixture(scope="session")
def driver(logger):
    _dirs()
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")
    options.add_argument("--window-size=1366,768")
    options.add_argument("--disable-gpu")

    logger.info("Setup: start Chrome driver")
    drv = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    drv.implicitly_wait(2)

    yield drv

    logger.info("Teardown: quit Chrome driver")
    drv.quit()


@pytest.fixture(autouse=True)
def log_test_start_end(request, logger):
    name = request.node.name
    logger.info(f"[TEST START] {name}")
    yield
    logger.info(f"[TEST END] {name}")


@pytest.fixture
def step(logger):
    def _s(msg: str):
        logger.info(f"[STEP] {msg}")
    return _s


def _screenshot(driver, test_name: str) -> str:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    file = f"{test_name}_{ts}.png".replace(" ", "_").replace("/", "_").replace("\\", "_")
    path = os.path.abspath(os.path.join("screenshots", file))
    driver.save_screenshot(path)
    return path


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call":
        return

    logger = item.funcargs.get("logger")
    driver = item.funcargs.get("driver")

    extra = getattr(report, "extra", [])

    if report.failed:
        if logger:
            logger.error(f"[FAIL] {item.name} :: {report.longrepr}")
        if driver:
            path = _screenshot(driver, item.name)
            try:
                from pytest_html import extras
                extra.append(extras.png(path))
                extra.append(extras.text(f"Screenshot: {path}"))
            except Exception:
                if logger:
                    logger.error("pytest-html extras failed (screenshot still saved).")

    report.extra = extra
