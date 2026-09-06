import logging

import pytest
from playwright.sync_api import expect

from pages.login_page import LoginPage

logger = logging.getLogger(__name__)


@pytest.mark.parametrize(
    "test_case_id, email, password",
    [
        ("TC_LOGIN_01", "dhakacitycountryadmin@gmail.com", "12345"),
    ],
    ids=["TC_LOGIN_01"],
)
def test_login_valid_credentials(page, test_case_id, email, password):
    login = LoginPage(page)
    login.load()
    login.login(email, password)
    logger.info("%s: PASS - user successfully logged in", test_case_id)
    expect(page).to_have_url("https://easset.scibd.info/")
    page.wait_for_timeout(3000)


@pytest.mark.parametrize(
    "test_case_id, email, password",
    [
        ("TC_LOGIN_02", "dhakacitycountryadmin@gmail.com", "wrongpassword"),
        ("TC_LOGIN_03", "invalidemail", "12345"),
    ],
    ids=["TC_LOGIN_02", "TC_LOGIN_03"],
)
def test_login_negative_cases(page, test_case_id, email, password):
    login = LoginPage(page)
    login.load()
    login.invalid_login(email, password)
    logger.info("%s: PASS - invalid credentials rejected as expected", test_case_id)
    expect(page.locator("text=Invalid")).to_be_visible()
    page.wait_for_timeout(2000)