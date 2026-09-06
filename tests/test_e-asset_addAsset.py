import pytest
from playwright.sync_api import expect

from pages.asset_manage_page import AssetManagePage
from pages.login_page import LoginPage


@pytest.mark.parametrize(
    "test_case_id",
    ["TC_ASSET_01"],
    ids=["TC_ASSET_01"],
)
def test_easset_addAsset(page, test_case_id):
    login = LoginPage(page)
    asset = AssetManagePage(page)

    login.load()
    login.login("dhakacitycountryadmin@gmail.com", "12345")
    asset.open_asset_entry()
    asset.add_asset()
    expect(asset.page_title).to_be_visible()
    page.wait_for_timeout(2000)
    page.wait_for_timeout(10000)
