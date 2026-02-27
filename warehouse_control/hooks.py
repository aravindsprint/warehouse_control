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

# Boot session hook
boot_session = "warehouse_control.overrides.boot_session"

# Document events
doc_events = {
    "Stock Entry": {
        "before_submit": "warehouse_control.controllers.warehouse_validator.validate_warehouse_access",
        "before_save": "warehouse_control.controllers.warehouse_validator.validate_warehouse_access"
    },
    "Purchase Receipt": {
        "before_submit": "warehouse_control.controllers.warehouse_validator.validate_warehouse_access",
        "before_save": "warehouse_control.controllers.warehouse_validator.validate_warehouse_access"
    },
    "Purchase Invoice": {
        "before_submit": "warehouse_control.controllers.warehouse_validator.validate_warehouse_access",
        "before_save": "warehouse_control.controllers.warehouse_validator.validate_warehouse_access"
    },
    "Sales Invoice": {
        "before_submit": "warehouse_control.controllers.warehouse_validator.validate_warehouse_access",
        "before_save": "warehouse_control.controllers.warehouse_validator.validate_warehouse_access"
    },
    "Delivery Note": {
        "before_submit": "warehouse_control.controllers.warehouse_validator.validate_warehouse_access",
        "before_save": "warehouse_control.controllers.warehouse_validator.validate_warehouse_access"
    },
    "Subcontracting Receipt": {
        "before_submit": "warehouse_control.controllers.warehouse_validator.validate_warehouse_access",
        "before_save": "warehouse_control.controllers.warehouse_validator.validate_warehouse_access"
    },
    "Stock Reconciliation": {
        "before_submit": "warehouse_control.controllers.warehouse_validator.validate_warehouse_access",
        "before_save": "warehouse_control.controllers.warehouse_validator.validate_warehouse_access"
    },
    "Material Request": {
        "before_submit": "warehouse_control.controllers.warehouse_validator.validate_warehouse_access",
        "before_save": "warehouse_control.controllers.warehouse_validator.validate_warehouse_access"
    }
}

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

