import frappe
from frappe import _

def check_app_enabled():
    """Middleware to check if app is enabled for each request"""
    try:
        # Skip check for certain paths
        skip_paths = [
            '/api/method/frappe.client.get_value',
            '/api/method/frappe.client.get_single',
            '/api/method/warehouse_control',
            '/app/warehouse-control-settings'
        ]
        
        current_path = frappe.request.path
        if any(skip in current_path for skip in skip_paths):
            return
        
        # Check if this is a warehouse_control related request
        is_warehouse_request = False
        
        # Check if doctype is from warehouse_control
        if frappe.request.args.get('doctype'):
            doctype = frappe.request.args.get('doctype')
            if doctype:
                meta = frappe.get_meta(doctype)
                if meta.module and meta.module_app == 'warehouse_control':
                    is_warehouse_request = True
        
        # Check if it's a warehouse_control page
        if '/app/warehouse-control' in current_path:
            is_warehouse_request = True
        
        if is_warehouse_request:
            settings = frappe.get_single('Warehouse Control Settings')
            
            if not settings.enable_app:
                # Allow System Manager to access
                if 'System Manager' in frappe.get_roles():
                    return
                
                # For API requests
                if '/api/' in current_path:
                    frappe.throw(_('Warehouse Control app is currently disabled'), 
                               frappe.PermissionError)
                
                # For web page requests
                frappe.respond_as_web_page(
                    _('App Disabled'),
                    _('Warehouse Control app is currently disabled. Please contact System Manager.'),
                    success=False,
                    http_status_code=403
                )
    except Exception as e:
        # Log error but don't block request
        frappe.log_error(f"Error in warehouse_control middleware: {str(e)}")
        pass
