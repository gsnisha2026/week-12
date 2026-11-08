
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def setup_teardown():
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install())
    )
    try:
        yield driver
    finally:
        driver.quit()


def get_alert_text(driver):
    WebDriverWait(driver, 5).until(EC.alert_is_present())
    alert = Alert(driver)
    message = alert.text
    alert.accept()
    return message


def test_registration_page(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")

    assert driver.title == "Form Example"
    assert driver.find_element(By.TAG_NAME, "h2").text == "Application Form"


def test_empty_name(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")

    driver.find_element(By.NAME, "username").send_keys(" ")
    driver.find_element(By.NAME, "pwd").send_keys("testpassword")
    driver.find_element(By.NAME, "sb").click()

    assert get_alert_text(driver) == "Username cannot be empty."


def test_empty_password(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")

    driver.find_element(By.NAME, "username").send_keys("Nisha")
    driver.find_element(By.NAME, "pwd").clear()
    driver.find_element(By.NAME, "sb").click()

    assert get_alert_text(driver) == "Password cannot be empty."


def test_short_password(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")

    driver.find_element(By.NAME, "username").send_keys("Nisha")
    driver.find_element(By.NAME, "pwd").send_keys("123")
    driver.find_element(By.NAME, "sb").click()

    assert get_alert_text(driver) == (
        "Password must be at least 6 characters long."
    )


def test_valid_registration(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")

    driver.find_element(By.NAME, "username").send_keys("Nisha")
    driver.find_element(By.NAME, "pwd").send_keys("testpassword")
    driver.find_element(By.NAME, "sb").click()

    WebDriverWait(driver, 5).until(EC.url_contains("/submit"))

    assert "/submit" in driver.current_url
    assert driver.find_element(By.TAG_NAME, "h2").text == (
        "Hello, Nisha! Welcome to the website"
    )
