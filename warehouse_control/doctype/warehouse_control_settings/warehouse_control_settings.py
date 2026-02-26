import frappe
from frappe.model.document import Document

class WarehouseControlSettings(Document):
    def validate(self):
        if self.has_value_changed('enable_app'):
            self.toggle_app()
    
    def toggle_app(self):
        """Simple toggle - just clear cache"""
        frappe.clear_cache()
        frappe.db.commit()
        print(f"App toggled to: {'Enabled' if self.enable_app else 'Disabled'}")
