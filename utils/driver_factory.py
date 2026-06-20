import os
import logging
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager

_LOG = logging.getLogger(__name__)

def create_driver(headless: bool = False):
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    msedgedriver_path = os.getenv("MS_EDGEDRIVER_PATH")
    if msedgedriver_path:
        service = EdgeService(msedgedriver_path)
    else:
        try:
            service = EdgeService(EdgeChromiumDriverManager().install())
        except Exception as exc:
            _LOG.error("Failed to install msedgedriver: %s", exc)
            raise RuntimeError("Could not install or initialize msedgedriver. Set MS_EDGEDRIVER_PATH or install the driver manually.") from exc

    if service:
        driver = webdriver.Edge(service=service, options=options)
    else:
        driver = webdriver.Edge(options=options)

    driver.implicitly_wait(5)
    return driver

def load_users_from_csv(file_path: str) -> list[dict]:
    users = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if len(row) < 2:
                continue
            users.append({
                "username": row[0].strip(),
                "password": row[1].strip()
            })
    return users

def load_users_from_json(file_path: str) -> list[dict]:
    with open(file_path, 'r', encoding='utf-8') as jsonfile:
        return json.load(jsonfile)