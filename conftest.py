from pathlib import Path

import pytest
from pytest_html import extras


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page is None:
            return

        screenshot_dir = Path("reports") / "screenshots"
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        screenshot_path = screenshot_dir / f"{item.name}.png"
        page.screenshot(path=str(screenshot_path), full_page=True)

        report.extras = getattr(report, "extras", [])
        report.extras.append(extras.image(screenshot_path.as_posix(), name=f"{item.name} failure screenshot"))
