import frappe

def execute():
    """Create Warehouse Control Settings if it doesn't exist"""
    if not frappe.db.exists('DocType', 'Warehouse Control Settings'):
        # Create the doctype via code
        settings_doctype = frappe.get_doc({
            'doctype': 'DocType',
            'name': 'Warehouse Control Settings',
            'module': 'Warehouse Control',
            'custom': 0,
            'issingle': 1,
            'fields': [
                {
                    'fieldname': 'enable_app',
                    'fieldtype': 'Check',
                    'label': 'Enable Warehouse Control App',
                    'description': 'Check to enable the app, uncheck to disable (data preserved)'
                }
            ],
            'permissions': [{
                'role': 'System Manager',
                'read': 1,
                'write': 1,
                'create': 1,
                'delete': 1
            }]
        })
        settings_doctype.insert(ignore_permissions=True)
        
        # Create the settings record
        settings = frappe.new_doc('Warehouse Control Settings')
        settings.enable_app = 1
        settings.insert(ignore_permissions=True)
        
        frappe.db.commit()
        print("✓ Created Warehouse Control Settings")
