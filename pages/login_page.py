import logging

from playwright.sync_api import Page, expect

logger = logging.getLogger(__name__)
DEFAULT_TIMEOUT = 30000


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username = page.get_by_placeholder("example@savethechildren.org")
        self.password = page.locator("//input[@placeholder='************']")
        self.login_btn = page.get_by_role("button", name="Login")
        self.userIcon = page.locator("//div[@class='rf-page-header-action-item-userletter']")
        self.logout_btn = page.get_by_role("button", name="Logout")

    def wait_for_page_ready(self):
        self.page.wait_for_load_state("domcontentloaded", timeout=DEFAULT_TIMEOUT)
        try:
            self.page.wait_for_load_state("networkidle", timeout=5000)
        except Exception:
            pass
        preloader = self.page.locator(".preloader-rf-backarea")
        if preloader.count() > 0:
            preloader.first.wait_for(state="hidden", timeout=DEFAULT_TIMEOUT)

    def load(self):
        self.page.goto("https://easset.scibd.info/", wait_until="domcontentloaded", timeout=DEFAULT_TIMEOUT)
        self.wait_for_page_ready()
        self.page.wait_for_timeout(2000)
        expect(self.username).to_be_visible(timeout=DEFAULT_TIMEOUT)

    def login(self, user, pwd):
        self.username.fill(user, timeout=DEFAULT_TIMEOUT)
        self.password.fill(pwd, timeout=DEFAULT_TIMEOUT)
        self.login_btn.click(timeout=DEFAULT_TIMEOUT)
        self.wait_for_page_ready()
        self.page.wait_for_timeout(3000)
        expect(self.page).to_have_url("https://easset.scibd.info/", timeout=DEFAULT_TIMEOUT)
        expect(self.userIcon).to_be_visible(timeout=DEFAULT_TIMEOUT)
        logger.info("TC_LOGIN_01: PASS - valid credentials accepted for %s", user)

    def login2(self, user, pwd):
        self.username.fill(user, timeout=DEFAULT_TIMEOUT)
        self.password.fill(pwd, timeout=DEFAULT_TIMEOUT)
        self.login_btn.click(timeout=DEFAULT_TIMEOUT)
        self.wait_for_page_ready()
        expect(self.userIcon).to_be_visible(timeout=DEFAULT_TIMEOUT)
        logger.info("TC_LOGIN_01: PASS - valid credentials accepted for %s", user)

    def invalid_login(self, user, pwd):
        self.username.fill(user, timeout=DEFAULT_TIMEOUT)
        self.password.fill(pwd, timeout=DEFAULT_TIMEOUT)
        self.login_btn.click(timeout=DEFAULT_TIMEOUT)
        self.wait_for_page_ready()
        expect(self.page.locator("text=Invalid")).to_be_visible(timeout=DEFAULT_TIMEOUT)
        expect(self.page).to_have_url("https://easset.scibd.info/Account/Login", timeout=DEFAULT_TIMEOUT)
        expect(self.username).to_be_visible(timeout=DEFAULT_TIMEOUT)

    def logout(self):
        self.userIcon.click()
        self.logout_btn.click()