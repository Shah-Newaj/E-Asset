from pages.asset_manage_page import AssetManagePage
from pages.login_page import LoginPage


def test_easset_addAsset(page):
    login = LoginPage(page)
    asset = AssetManagePage(page)

    login.load()
    login.login("dhakacitycountryadmin@gmail.com", "12345")
    page.wait_for_timeout(3000)

    asset.Add_Asset()
    page.wait_for_timeout(3000)