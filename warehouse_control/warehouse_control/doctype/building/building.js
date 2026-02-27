// Copyright (c) 2024, Your Company and contributors
// For license information, please see license.txt

frappe.ui.form.on('Building', {
	refresh: function(frm) {
		// Add custom buttons
		if (!frm.is_new()) {
			frm.add_custom_button(__('View Warehouses'), function() {
				frappe.set_route('List', 'Warehouse', {building: frm.doc.name});
			});
			
			frm.add_custom_button(__('View Users'), function() {
				frappe.set_route('List', 'User', {assigned_building: frm.doc.name});
			});
		}
	}
});
