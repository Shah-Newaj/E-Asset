# E-Asset
E-Asset provides a centralized solution for tracking, managing, maintaining, transferring, reclassifying, and disposing of organizational assets and GPE throughout their lifecycle.

## Command to Run...
	pytest -v -s .\tests\test_e-asset_addAsset.py --html=reports/report.html -q --headed

	pytest tests\test_e-asset_login.py tests\test_e-asset_addAsset.py -q --html=reports\combined_report.html --self-contained-html
