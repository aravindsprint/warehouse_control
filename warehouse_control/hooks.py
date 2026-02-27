# -*- coding: utf-8 -*-
from __future__ import unicode_literals

app_name = "warehouse_control"
app_title = "Warehouse Control"
app_publisher = "Your Company"
app_description = "Building-based warehouse access control for ERPNext"
app_email = "your-email@company.com"
app_license = "MIT"

required_erpnext_version = ">=15.0.0"

# Install/Migrate Hooks
# ------------
after_install = "warehouse_control.custom_fields.warehouse_building.setup_custom_fields"
after_migrate = "warehouse_control.custom_fields.warehouse_building.setup_custom_fields"

# Apps
# ------------
app_include_js = []
app_include_css = []

# Fixtures
# ------------
fixtures = []

# Permissions
# ------------
permissions = []

# Document Events
# ------------
doc_events = {}

# Scheduler Events
# ------------
scheduler_events = {}

# Custom fields
# ------------
custom_fields = {}

# Property Setters
# ------------
property_setters = {}

# Rename Doctypes
# ------------
rename_doctype_map = {}

# Boot Session
# ------------
boot_session = []