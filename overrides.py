import frappe

def boot_session(bootinfo):
    """Simple boot hook"""
    try:
        if frappe.db.exists("Warehouse Control Settings", "Warehouse Control Settings"):
            settings = frappe.get_single("Warehouse Control Settings")
            if settings and not settings.enable_app:
                # Remove from modules
                if "warehouse_control" in bootinfo.modules:
                    bootinfo.modules.pop("warehouse_control")
    except:
        pass

def has_permission(doc, ptype, user):
    """Check permissions"""
    return True

def get_permission_query_conditions(user):
    """Filter queries"""
    return ""
