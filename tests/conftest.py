import logging
import os
import sys
from datetime import datetime

import pytest
from pytest_html import extras

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from utils.driver_factory import create_driver


def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        help="Run UI tests in headless mode",
    )


def pytest_configure(config):
    reports_dir = os.path.join(ROOT, "reports")
    logs_dir = os.path.join(reports_dir, "logs")
    screenshots_dir = os.path.join(reports_dir, "screenshots")

    os.makedirs(reports_dir, exist_ok=True)
    os.makedirs(logs_dir, exist_ok=True)
    os.makedirs(screenshots_dir, exist_ok=True)

    config._reports_dir = reports_dir
    config._logs_dir = logs_dir
    config._screenshots_dir = screenshots_dir

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.StreamHandler()],
    )


@pytest.fixture
def driver(request):
    headless = request.config.getoption("--headless")
    try:
        driver = create_driver(headless=headless)
    except RuntimeError as exc:
        pytest.skip(f"WebDriver unavailable: {exc}")
        return
    yield driver
    driver.quit()


@pytest.fixture(autouse=True)
def ui_logger(request):
    if "api" in request.keywords:
        yield None
        return

    logs_dir = request.config._logs_dir
    log_filename = f"{request.node.name}_ui.log"
    log_path = os.path.join(logs_dir, log_filename)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    handler = logging.FileHandler(log_path, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
    root_logger.addHandler(handler)

    yield root_logger

    handler.close()
    root_logger.removeHandler(handler)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call":
        report.extra = getattr(report, "extra", [])

        api_logger = item.funcargs.get("api_logger", None)
        if api_logger is not None:
            log_path = os.path.join(item.config._logs_dir, f"{item.name}_api.log")
            if os.path.exists(log_path):
                with open(log_path, "r", encoding="utf-8") as log_file:
                    report.extra.append(extras.text(log_file.read(), name="API Log"))

        ui_logger = item.funcargs.get("ui_logger", None)
        if ui_logger is not None:
            ui_log_path = os.path.join(item.config._logs_dir, f"{item.name}_ui.log")
            if os.path.exists(ui_log_path):
                with open(ui_log_path, "r", encoding="utf-8") as log_file:
                    report.extra.append(extras.text(log_file.read(), name="UI Log"))

        driver = item.funcargs.get("driver", None)
        if driver is not None and report.failed:
            screenshot_filename = f"{item.name}_{datetime.now():%Y%m%d_%H%M%S}.png"
            screenshot_path = os.path.join(item.config._screenshots_dir, screenshot_filename)
            try:
                driver.save_screenshot(screenshot_path)
                report.extra.append(extras.image(screenshot_path))
            except Exception:
                pass
