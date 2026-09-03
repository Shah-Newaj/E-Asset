from playwright.sync_api import Page

class AssetManagePage:
    def __init__(self, page: Page):
        self.page = page
        self.asset_manage = page.get_by_text("Asset Manage")
        self.manage = page.get_by_role("link", name="Manage")
        self.asset_list = page.get_by_role("link", name="Asset List")


    def Add_Asset(self):
        self.asset_manage.click()
        self.asset_list.click()