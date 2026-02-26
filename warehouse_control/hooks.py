# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from warehouse_control import __version__ as app_version

app_name = "warehouse_control"
app_title = "Warehouse Control"
app_publisher = "Your Company"
app_description = "Building-based warehouse access control for ERPNext"
app_icon = "octicon octicon-package"
app_color = "blue"
app_email = "your-email@company.com"
app_license = "MIT"

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