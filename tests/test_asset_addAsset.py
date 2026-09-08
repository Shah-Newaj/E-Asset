import pytest
from playwright.sync_api import expect

from pages.asset_list_page import AssetListPage
from pages.login_page import LoginPage


@pytest.mark.parametrize(
    "test_case_id",
    ["TC_ASSET_01"],
    ids=["TC_ASSET_01"],
)
def test_easset_addAsset(page, test_case_id):
    login = LoginPage(page)
    asset = AssetListPage(page)

    login.load()
    login.login("dhakacitycountryadmin@gmail.com", "12345")
    asset.open_asset_entry()
    asset.add_asset()
    expect(page).to_have_url("https://easset.scibd.info/Operation/AssetList")
    expect(page.get_by_role("link", name="Asset List")).to_be_visible(timeout=15000)
    page.wait_for_timeout(2000)
