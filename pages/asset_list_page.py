import logging

from playwright.sync_api import Page, expect

logger = logging.getLogger(__name__)
DEFAULT_TIMEOUT = 30000


class AssetListPage:
    def __init__(self, page: Page):
        self.page = page
        self.asset_manage = page.get_by_text("Asset Manage")
        self.manage = page.get_by_role("link", name="Manage")
        self.asset_list = page.get_by_role("link", name="Asset List")
        self.add_new_btn = page.get_by_role("button", name="Add New")
        self.page_title = page.locator("div.page-rf-header-title", has_text="Asset Entry").first
        self.save_btn = page.get_by_text("Save", exact=True)

    def wait_for_app_ready(self):
        self.page.wait_for_load_state("domcontentloaded", timeout=DEFAULT_TIMEOUT)
        for _ in range(20):
            try:
                self.page.wait_for_load_state("networkidle", timeout=2000)
            except Exception:
                pass

            preloader = self.page.locator(".preloader-rf-backarea")
            loading = self.page.locator("text=Loading...")
            preloader_visible = preloader.count() > 0 and preloader.first.is_visible()
            loading_visible = loading.count() > 0 and loading.first.is_visible()

            if not preloader_visible and not loading_visible:
                return
            self.page.wait_for_timeout(500)

    def click_via_script(self, locator):
        try:
            locator.click(force=True, timeout=DEFAULT_TIMEOUT)
        except Exception:
            locator.evaluate("node => node.click()")
        self.page.wait_for_timeout(1000)

    def open_asset_entry(self):
        self.page.goto("https://easset.scibd.info/Operation/AssetList", wait_until="domcontentloaded", timeout=DEFAULT_TIMEOUT)
        self.wait_for_app_ready()
        expect(self.page).to_have_url("https://easset.scibd.info/Operation/AssetList", timeout=DEFAULT_TIMEOUT)

        for attempt in range(3):
            try:
                self.page.goto("https://easset.scibd.info/Operation/AssetEntry", wait_until="domcontentloaded", timeout=DEFAULT_TIMEOUT)
                self.wait_for_app_ready()
                if self.page.url.startswith("https://easset.scibd.info/Operation/AssetEntry"):
                    break
            except Exception:
                pass
            if attempt == 2:
                raise
            self.page.wait_for_timeout(2000)

        page_title = self.page.locator("div.page-rf-header-title", has_text="Asset Entry").first
        expect(page_title).to_be_visible(timeout=DEFAULT_TIMEOUT)
        expect(self.page).to_have_url("https://easset.scibd.info/Operation/AssetEntry", timeout=DEFAULT_TIMEOUT)
        logger.info("TC_ASSET_01: PASS - Asset Entry page loaded via direct route navigation")

    def assert_field_visible(self, label_text):
        locator = self.page.locator("label.rf-control-label", has_text=label_text)
        expect(locator).to_be_visible(timeout=DEFAULT_TIMEOUT)
        logger.info("TC_ASSET_01: PASS - field visible: %s", label_text)
        return locator

    def field_input(self, label_text, log=True):
        locator = self.page.locator("label.rf-control-label", has_text=label_text).locator("xpath=following-sibling::div[1]//input").first
        expect(locator).to_be_visible(timeout=DEFAULT_TIMEOUT)
        if log:
            logger.info("TC_ASSET_01: PASS - input field visible: %s", label_text)
        return locator

    def field_textarea(self, label_text, log=True):
        locator = self.page.locator("label.rf-control-label", has_text=label_text).locator("xpath=following-sibling::textarea").first
        expect(locator).to_be_visible(timeout=DEFAULT_TIMEOUT)
        if log:
            logger.info("TC_ASSET_01: PASS - textarea field visible: %s", label_text)
        return locator

    def visible_dropdown_popper(self, label_text):
        for _ in range(10):
            popper = self.page.locator("div.select-rf-popper:visible")
            if popper.count() > 0:
                return popper.first
            self.page.wait_for_timeout(500)
        raise AssertionError(f"No visible dropdown popup found for {label_text}")

    def visible_date_popup(self, label_text):
        for _ in range(10):
            popup = self.page.locator("div.datepicker-popup-rf:visible")
            if popup.count() > 0:
                return popup.first
            self.page.wait_for_timeout(500)
        raise AssertionError(f"No visible date popup found for {label_text}")

    def select_dropdown(self, label_text, option_text):
        self.assert_field_visible(label_text)
        field = self.page.locator("label.rf-control-label", has_text=label_text).locator("xpath=following-sibling::div[contains(@class, 'select-rf')][1]")
        expect(field).to_be_visible(timeout=DEFAULT_TIMEOUT)

        for attempt in range(3):
            self.click_via_script(field)
            try:
                popper = self.visible_dropdown_popper(label_text)
                break
            except AssertionError:
                if attempt == 2:
                    raise
                self.page.wait_for_timeout(1000)

        option = popper.locator(".select-rf-popper-item").filter(has_text=option_text).first
        expect(option).to_be_visible(timeout=DEFAULT_TIMEOUT)
        self.click_via_script(option)
        expect(field).to_contain_text(option_text, timeout=DEFAULT_TIMEOUT)
        logger.info("TC_ASSET_01: PASS - dropdown selected: %s -> %s", label_text, option_text)

    def set_date(self, label_text, value):
        self.assert_field_visible(label_text)
        date_field = self.page.locator("label.rf-control-label", has_text=label_text).locator("xpath=following-sibling::div[contains(@class, 'datepicker-rf')][1]")
        expect(date_field).to_be_visible(timeout=DEFAULT_TIMEOUT)
        self.click_via_script(date_field)

        popup = self.visible_date_popup(label_text)

        day = value.split('/')[0]
        day_cell = popup.locator("td", has_text=day).first
        expect(day_cell).to_be_visible(timeout=DEFAULT_TIMEOUT)
        day_cell.scroll_into_view_if_needed()
        self.click_via_script(day_cell)

        date_input = self.page.locator("label.rf-control-label", has_text=label_text).locator("xpath=following-sibling::div[contains(@class, 'datepicker-rf')][1]//input").first
        expect(date_input).to_have_value(value, timeout=DEFAULT_TIMEOUT)
        logger.info("TC_ASSET_01: PASS - date field selected via date picker: %s = %s", label_text, value)

    def save_asset(self):
        expect(self.save_btn).to_be_visible(timeout=DEFAULT_TIMEOUT)
        self.click_via_script(self.save_btn)

        self.page.wait_for_timeout(10000)
        self.page.wait_for_load_state("networkidle", timeout=DEFAULT_TIMEOUT)
        self.page.wait_for_url("**/Operation/AssetList", timeout=DEFAULT_TIMEOUT)

        success_toast = self.page.locator("text=/Saved successfully|successfully saved|Success|Successful/i")
        if success_toast.count() > 0:
            expect(success_toast.first).to_be_visible(timeout=DEFAULT_TIMEOUT)

        expect(self.page).to_have_url("https://easset.scibd.info/Operation/AssetList", timeout=DEFAULT_TIMEOUT)
        expect(self.page.locator("text=Purchase date is required")).to_have_count(0, timeout=DEFAULT_TIMEOUT)
        expect(self.page.locator("text=Warranty end date is required")).to_have_count(0, timeout=DEFAULT_TIMEOUT)
        expect(self.page.locator("text=Supplier is required")).to_have_count(0, timeout=DEFAULT_TIMEOUT)
        expect(self.page.locator("text=End of award date is required")).to_have_count(0, timeout=DEFAULT_TIMEOUT)
        expect(self.page.locator("text=SOF is required")).to_have_count(0, timeout=DEFAULT_TIMEOUT)
        logger.info("TC_ASSET_01: PASS - asset form submitted successfully and redirected to Asset List")

    def Add_Asset(self):
        self.asset_manage.click()
        self.asset_list.click()

    def add_asset(self):
        self.select_dropdown("Office", "Gulshan Country Office")
        self.select_dropdown("Category", "Vehicles (all vehicles including 4x4, Van, Light Truck, Heavy Truck and tractors, but excluding motorbikes / quad bikes)")
        self.field_input("Asset Name").fill("Automation Asset 001")
        expect(self.field_input("Asset Name", log=False)).to_have_value("Automation Asset 001")
        self.field_input("Make").fill("Dell")
        expect(self.field_input("Make", log=False)).to_have_value("Dell")
        self.field_input("Model").fill("Latitude 7440")
        expect(self.field_input("Model", log=False)).to_have_value("Latitude 7440")
        self.field_input("Serial Number 1").fill("SN-AUT-001")
        expect(self.field_input("Serial Number 1", log=False)).to_have_value("SN-AUT-001")
        self.field_input("Serial Number 2").fill("SN-AUT-002")
        expect(self.field_input("Serial Number 2", log=False)).to_have_value("SN-AUT-002")
        self.field_input("Location").fill("Office Room 1")
        expect(self.field_input("Location", log=False)).to_have_value("Office Room 1")
        self.field_input("Other Reference Number").fill("REF-AUT-001")
        expect(self.field_input("Other Reference Number", log=False)).to_have_value("REF-AUT-001")
        self.field_textarea("Asset Description").fill("Automation test asset created via Playwright")
        expect(self.field_textarea("Asset Description", log=False)).to_have_value("Automation test asset created via Playwright")
        self.field_input("FMS Asset Number").fill("FMS-AUT-001")
        expect(self.field_input("FMS Asset Number", log=False)).to_have_value("FMS-AUT-001")
        self.field_input("Property Reference Information").fill("PROP-001")
        expect(self.field_input("Property Reference Information", log=False)).to_have_value("PROP-001")
        self.set_date("Purchase Date", "15/09/2026")
        self.set_date("Warranty End Date", "15/09/2026")
        self.field_input("Purchase Order No").fill("PO-001")
        expect(self.field_input("Purchase Order No", log=False)).to_have_value("PO-001")
        self.field_input("Item Value (Invoice Currency)").fill("1000")
        expect(self.field_input("Item Value (Invoice Currency)", log=False)).to_have_value("1000")
        self.field_input("Item Value (USD)").fill("1000")
        expect(self.field_input("Item Value (USD)", log=False)).to_have_value("1000")
        self.field_input("Cost of Replacement in USD").fill("1200")
        expect(self.field_input("Cost of Replacement in USD", log=False)).to_have_value("1200")
        self.select_dropdown("Supplier", "Tahmid supplier")
        self.field_input("Project Code").fill("PRJ-001")
        expect(self.field_input("Project Code", log=False)).to_have_value("PRJ-001")
        self.field_input("DRC Code").fill("DRC-001")
        expect(self.field_input("DRC Code", log=False)).to_have_value("DRC-001")
        self.field_input("Activity Code").fill("ACT-001")
        expect(self.field_input("Activity Code", log=False)).to_have_value("ACT-001")
        self.field_input("Account Code").fill("ACC-001")
        expect(self.field_input("Account Code", log=False)).to_have_value("ACC-001")
        self.set_date("End of Award Date", "15/09/2026")
        self.select_dropdown("Asset Condition", "New (Purchased within the last 12 months)")
        self.field_input("Donor").fill("Test Donor")
        expect(self.field_input("Donor", log=False)).to_have_value("Test Donor")
        self.field_input("Disposal Plan").fill("N/A")
        expect(self.field_input("Disposal Plan", log=False)).to_have_value("N/A")
        self.field_input("NBV/FMV (Insurance)").fill("500")
        expect(self.field_input("NBV/FMV (Insurance)", log=False)).to_have_value("500")
        self.field_input("SOF").fill("SOF-001")
        expect(self.field_input("SOF", log=False)).to_have_value("SOF-001")
        self.save_asset()
