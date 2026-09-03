from pages.login_page import LoginPage


def test_login(page):
    login = LoginPage(page)

    login.load()
    login.login("dhakacitycountryadmin@gmail.com", "12345")
    page.wait_for_timeout(3000)