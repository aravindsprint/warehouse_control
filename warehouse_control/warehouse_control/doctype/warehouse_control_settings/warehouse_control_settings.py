import frappe
from frappe.model.document import Document

class WarehouseControlSettings(Document):
    def validate(self):
        if self.has_value_changed('enable_app'):
            self.last_updated = frappe.utils.now()
            self.updated_by = frappe.session.user
            frappe.msgprint(
                f"Warehouse Control app is now {'enabled' if self.enable_app else 'disabled'}. All data is preserved.",
                indicator='green' if self.enable_app else 'orange',
                alert=True
            )

    def on_update(self):
        frappe.clear_cache()
        