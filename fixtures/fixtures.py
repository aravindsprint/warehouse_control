import frappe

def after_migrate():
    """Create settings and track module status"""
    try:
        # Check if we can add a custom field to Module Def
        module_doctype = 'Module Def'
        
        # Check if the custom field already exists
        if not frappe.db.exists('Custom Field', {'dt': module_doctype, 'fieldname': 'custom_is_disabled'}):
            try:
                custom_field = frappe.get_doc({
                    'doctype': 'Custom Field',
                    'dt': module_doctype,
                    'fieldname': 'custom_is_disabled',
                    'fieldtype': 'Check',
                    'label': 'Is Disabled',
                    'insert_after': 'app_name',
                    'module': 'Warehouse Control'
                })
                custom_field.insert(ignore_permissions=True)
                print(f"✓ Created custom_is_disabled field in {module_doctype}")
            except Exception as e:
                print(f"Could not create custom field: {e}")
                # Alternative: Create a separate table to track module status
                create_module_status_table()
        
        # Create the settings doctype if it doesn't exist
        if not frappe.db.exists("DocType", "Warehouse Control Settings"):
            doc = frappe.get_doc({
                "doctype": "DocType",
                "name": "Warehouse Control Settings",
                "module": "Warehouse Control",
                "custom": 0,
                "issingle": 1,
                "fields": [
                    {
                        "fieldname": "enable_app",
                        "fieldtype": "Check",
                        "label": "Enable Warehouse Control App"
                    },
                    {
                        "fieldname": "status_section",
                        "fieldtype": "Section Break",
                        "label": "Status"
                    },
                    {
                        "fieldname": "app_status_html",
                        "fieldtype": "HTML",
                        "label": "App Status"
                    },
                    {
                        "fieldname": "module_section",
                        "fieldtype": "Section Break",
                        "label": "Modules"
                    },
                    {
                        "fieldname": "module_list_html",
                        "fieldtype": "HTML",
                        "label": "Module List"
                    }
                ],
                "permissions": [{
                    "role": "System Manager",
                    "read": 1,
                    "write": 1,
                    "create": 1,
                    "delete": 1
                }]
            })
            doc.insert(ignore_permissions=True)
            print("✓ Created Warehouse Control Settings doctype")
        
        # Create the settings record
        if not frappe.db.exists("Warehouse Control Settings", "Warehouse Control Settings"):
            settings = frappe.new_doc("Warehouse Control Settings")
            settings.enable_app = 1
            settings.insert(ignore_permissions=True)
            frappe.db.commit()
            print("✓ Created settings record")
    except Exception as e:
        print(f"Error in after_migrate: {e}")
        import traceback
        traceback.print_exc()

def create_module_status_table():
    """Create a separate table to track module status"""
    try:
        if not frappe.db.exists("DocType", "Warehouse Control Module Status"):
            doc = frappe.get_doc({
                "doctype": "DocType",
                "name": "Warehouse Control Module Status",
                "module": "Warehouse Control",
                "custom": 0,
                "fields": [
                    {
                        "fieldname": "module_name",
                        "fieldtype": "Data",
                        "label": "Module Name",
                        "reqd": 1
                    },
                    {
                        "fieldname": "is_disabled",
                        "fieldtype": "Check",
                        "label": "Is Disabled"
                    }
                ],
                "permissions": [{
                    "role": "System Manager",
                    "read": 1,
                    "write": 1,
                    "create": 1,
                    "delete": 1
                }]
            })
            doc.insert(ignore_permissions=True)
            print("✓ Created Warehouse Control Module Status table")
            
            # Populate with existing modules
            modules = frappe.db.get_all('Module Def', 
                filters={'app_name': 'warehouse_control'},
                fields=['name'])
            
            for m in modules:
                status = frappe.get_doc({
                    "doctype": "Warehouse Control Module Status",
                    "module_name": m.name,
                    "is_disabled": 0
                })
                status.insert(ignore_permissions=True)
            frappe.db.commit()
            print(f"✓ Added {len(modules)} modules to status table")
    except Exception as e:
        print(f"Error creating status table: {e}")
