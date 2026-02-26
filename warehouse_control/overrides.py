import frappe

def boot_session(bootinfo):
    """Hide Warehouse Control modules when app is disabled"""
    try:
        if frappe.db.exists("Warehouse Control Settings", "Warehouse Control Settings"):
            enabled = frappe.db.get_value("Warehouse Control Settings", 
                "Warehouse Control Settings", "enable_app")
            
            if not enabled:
                # Remove Warehouse Control modules from bootinfo
                modules_to_remove = []
                for module_name in bootinfo.get('modules', {}):
                    module_info = bootinfo['modules'].get(module_name, {})
                    if isinstance(module_info, dict) and module_info.get('app_name') == 'warehouse_control':
                        modules_to_remove.append(module_name)
                
                for module_name in modules_to_remove:
                    bootinfo['modules'].pop(module_name, None)
                
                # Also hide from desk pages
                if hasattr(bootinfo, 'desk_pages'):
                    bootinfo.desk_pages = [
                        page for page in bootinfo.get('desk_pages', [])
                        if not (isinstance(page, dict) and page.get('module') == 'Warehouse Control')
                    ]
    except Exception as e:
        frappe.log_error(f"Error in boot_session: {str(e)}", "Warehouse Control Boot")