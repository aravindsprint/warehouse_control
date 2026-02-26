import frappe
from frappe.model.document import Document

class WarehouseControlSettings(Document):
    def validate(self):
        if self.has_value_changed('enable_app'):
            frappe.msgprint(
                f"Warehouse Control app will be {'enabled' if self.enable_app else 'disabled'} after page refresh.",
                indicator='green' if self.enable_app else 'orange',
                alert=True
            )
    
    def on_update(self):
        # Clear cache to apply changes immediately
        frappe.clear_cache()