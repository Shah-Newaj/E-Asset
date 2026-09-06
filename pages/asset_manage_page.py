import logging

from playwright.sync_api import Page, expect

logger = logging.getLogger(__name__)
DEFAULT_TIMEOUT = 30000


class AssetManagePage:
    def __init__(self, page: Page):
        self.page = page
        self.asset_manage = page.get_by_text("Asset Manage")
        self.manage = page.get_by_role("link", name="Manage")
        self.asset_list = page.get_by_role("link", name="Asset List")
        self.add_new_btn = page.get_by_role("button", name="Add New")
        self.page_title = page.locator("div.page-rf-header-title", has_text="Asset Entry").first
        self.save_btn = page.get_by_text("Save", exact=True)

    def wait_for_app_ready(self):
        self.page.wait_for_load_state("networkidle", timeout=DEFAULT_TIMEOUT)
        preloader = self.page.locator(".preloader-rf-backarea")
        if preloader.count() > 0:
            preloader.first.wait_for(state="hidden", timeout=DEFAULT_TIMEOUT)

    def click_via_script(self, locator):
        locator.evaluate("node => node.click()")

    def open_asset_entry(self):
        self.wait_for_app_ready()
        self.click_via_script(self.asset_manage)
        expect(self.page).to_have_url("https://easset.scibd.info/", timeout=DEFAULT_TIMEOUT)
        self.wait_for_app_ready()
        self.click_via_script(self.asset_list)
        expect(self.page).to_have_url("https://easset.scibd.info/Operation/AssetList", timeout=DEFAULT_TIMEOUT)
        self.wait_for_app_ready()
        self.click_via_script(self.add_new_btn)
        page_title = self.page.locator("div.page-rf-header-title", has_text="Asset Entry").first
        expect(page_title).to_be_visible(timeout=DEFAULT_TIMEOUT)
        expect(self.page).to_have_url("https://easset.scibd.info/Operation/AssetEntry", timeout=DEFAULT_TIMEOUT)
        logger.info("TC_ASSET_01: PASS - Asset Entry page loaded via Asset Manage > Asset List > Add New")

    def assert_field_visible(self, label_text):
        locator = self.page.locator("label.rf-control-label", has_text=label_text)
        expect(locator).to_be_visible(timeout=DEFAULT_TIMEOUT)
        logger.info("TC_ASSET_01: PASS - field visible: %s", label_text)
        return locator

    def field_input(self, label_text):
        locator = self.page.locator("label.rf-control-label", has_text=label_text).locator("xpath=following-sibling::div[1]//input").first
        expect(locator).to_be_visible(timeout=DEFAULT_TIMEOUT)
        logger.info("TC_ASSET_01: PASS - input field visible: %s", label_text)
        return locator

    def field_textarea(self, label_text):
        locator = self.page.locator("label.rf-control-label", has_text=label_text).locator("xpath=following-sibling::textarea").first
        expect(locator).to_be_visible(timeout=DEFAULT_TIMEOUT)
        logger.info("TC_ASSET_01: PASS - textarea field visible: %s", label_text)
        return locator

    def select_dropdown(self, label_text, option_text):
        self.assert_field_visible(label_text)
        field = self.page.locator("label.rf-control-label", has_text=label_text).locator("xpath=following-sibling::div[contains(@class, 'select-rf')][1]")
        expect(field).to_be_visible(timeout=DEFAULT_TIMEOUT)
        field.click(timeout=DEFAULT_TIMEOUT)
        popper = self.page.locator("label.rf-control-label", has_text=label_text).locator("xpath=following-sibling::div[contains(@class, 'select-rf-popper')][1]")
        expect(popper).to_be_visible(timeout=DEFAULT_TIMEOUT)
        option = popper.locator(".select-rf-popper-item").filter(has_text=option_text).first
        expect(option).to_be_visible(timeout=DEFAULT_TIMEOUT)
        option.click(timeout=DEFAULT_TIMEOUT)
        expect(field).to_contain_text(option_text, timeout=DEFAULT_TIMEOUT)
        logger.info("TC_ASSET_01: PASS - dropdown selected: %s -> %s", label_text, option_text)

    def set_date(self, label_text, value):
        self.assert_field_visible(label_text)
        date_field = self.page.locator("label.rf-control-label", has_text=label_text).locator("xpath=following-sibling::div[contains(@class, 'datepicker-rf')][1]")
        expect(date_field).to_be_visible(timeout=DEFAULT_TIMEOUT)
        date_field.click(timeout=DEFAULT_TIMEOUT)

        popup = date_field.locator("xpath=following-sibling::div[contains(@class, 'datepicker-popup-rf')][1]")
        expect(popup).to_be_visible(timeout=DEFAULT_TIMEOUT)

        day = value.split('/')[0]
        day_cell = popup.locator("td", has_text=day).first
        expect(day_cell).to_be_visible(timeout=DEFAULT_TIMEOUT)
        day_cell.scroll_into_view_if_needed()
        day_cell.click(force=True, timeout=DEFAULT_TIMEOUT)

        date_input = self.page.locator("label.rf-control-label", has_text=label_text).locator("xpath=following-sibling::div[contains(@class, 'datepicker-rf')][1]//input").first
        expect(date_input).to_have_value(value, timeout=DEFAULT_TIMEOUT)
        logger.info("TC_ASSET_01: PASS - date field selected via date picker: %s = %s", label_text, value)

    def save_asset(self):
        expect(self.save_btn).to_be_visible(timeout=DEFAULT_TIMEOUT)
        self.click_via_script(self.save_btn)
        expect(self.page).to_have_url("https://easset.scibd.info/Operation/AssetEntry", timeout=DEFAULT_TIMEOUT)
        expect(self.page.locator("text=Purchase date is required")).to_have_count(0, timeout=DEFAULT_TIMEOUT)
        expect(self.page.locator("text=Warranty end date is required")).to_have_count(0, timeout=DEFAULT_TIMEOUT)
        expect(self.page.locator("text=Supplier is required")).to_have_count(0, timeout=DEFAULT_TIMEOUT)
        expect(self.page.locator("text=End of award date is required")).to_have_count(0, timeout=DEFAULT_TIMEOUT)
        expect(self.page.locator("text=SOF is required")).to_have_count(0, timeout=DEFAULT_TIMEOUT)
        expect(self.page_title).to_be_visible(timeout=DEFAULT_TIMEOUT)
        logger.info("TC_ASSET_01: PASS - asset form submitted successfully")

    def Add_Asset(self):
        self.asset_manage.click()
        self.asset_list.click()

    def add_asset(self):
        self.select_dropdown("Office", "Dhanmondi")
        self.select_dropdown("Category", "Vehicles (all vehicles including 4x4, Van, Light Truck, Heavy Truck and tractors, but excluding motorbikes / quad bikes)")
        self.field_input("Asset Name").fill("Automation Asset 001")
        expect(self.field_input("Asset Name")).to_have_value("Automation Asset 001")
        self.field_input("Make").fill("Dell")
        expect(self.field_input("Make")).to_have_value("Dell")
        self.field_input("Model").fill("Latitude 7440")
        expect(self.field_input("Model")).to_have_value("Latitude 7440")
        self.field_input("Serial Number 1").fill("SN-AUT-001")
        expect(self.field_input("Serial Number 1")).to_have_value("SN-AUT-001")
        self.field_input("Serial Number 2").fill("SN-AUT-002")
        expect(self.field_input("Serial Number 2")).to_have_value("SN-AUT-002")
        self.field_input("Location").fill("Office Room 1")
        expect(self.field_input("Location")).to_have_value("Office Room 1")
        self.field_input("Other Reference Number").fill("REF-AUT-001")
        expect(self.field_input("Other Reference Number")).to_have_value("REF-AUT-001")
        self.field_textarea("Asset Description").fill("Automation test asset created via Playwright")
        expect(self.field_textarea("Asset Description")).to_have_value("Automation test asset created via Playwright")
        self.field_input("FMS Asset Number").fill("FMS-AUT-001")
        expect(self.field_input("FMS Asset Number")).to_have_value("FMS-AUT-001")
        self.field_input("Property Reference Information").fill("PROP-001")
        expect(self.field_input("Property Reference Information")).to_have_value("PROP-001")
        self.set_date("Purchase Date", "15/09/2026")
        self.set_date("Warranty End Date", "15/09/2026")
        self.field_input("Purchase Order No").fill("PO-001")
        expect(self.field_input("Purchase Order No")).to_have_value("PO-001")
        self.field_input("Item Value (Invoice Currency)").fill("1000")
        expect(self.field_input("Item Value (Invoice Currency)")).to_have_value("1000")
        self.field_input("Item Value (USD)").fill("1000")
        expect(self.field_input("Item Value (USD)")).to_have_value("1000")
        self.field_input("Cost of Replacement in USD").fill("1200")
        expect(self.field_input("Cost of Replacement in USD")).to_have_value("1200")
        self.select_dropdown("Supplier", "Tahmid supplier")
        self.field_input("Project Code").fill("PRJ-001")
        expect(self.field_input("Project Code")).to_have_value("PRJ-001")
        self.field_input("DRC Code").fill("DRC-001")
        expect(self.field_input("DRC Code")).to_have_value("DRC-001")
        self.field_input("Activity Code").fill("ACT-001")
        expect(self.field_input("Activity Code")).to_have_value("ACT-001")
        self.field_input("Account Code").fill("ACC-001")
        expect(self.field_input("Account Code")).to_have_value("ACC-001")
        self.set_date("End of Award Date", "15/09/2026")
        self.select_dropdown("Asset Condition", "New (Purchased within the last 12 months)")
        self.field_input("Donor").fill("Test Donor")
        expect(self.field_input("Donor")).to_have_value("Test Donor")
        self.field_input("Disposal Plan").fill("N/A")
        expect(self.field_input("Disposal Plan")).to_have_value("N/A")
        self.field_input("NBV/FMV (Insurance)").fill("500")
        expect(self.field_input("NBV/FMV (Insurance)")).to_have_value("500")
        self.field_input("SOF").fill("SOF-001")
        expect(self.field_input("SOF")).to_have_value("SOF-001")
        self.save_asset()