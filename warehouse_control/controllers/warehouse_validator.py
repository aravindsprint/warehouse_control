# -*- coding: utf-8 -*-
# Copyright (c) 2024, Your Company and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def validate_warehouse_access(doc, method=None):
    """
    Main entry point for warehouse validation
    Validates warehouse access based on user's assigned building
    
    This function is called from hooks for various stock documents before save/submit
    """
    # ✅ CHECK IF APP IS ENABLED - If disabled, skip all validation
    try:
        if frappe.db.exists("Warehouse Control Settings", "Warehouse Control Settings"):
            enabled = frappe.db.get_value("Warehouse Control Settings", 
                "Warehouse Control Settings", "enable_app")
            
            # Robust check - handle 0, "0", None, False
            if not enabled or enabled == 0 or enabled == "0":
                # App is disabled - skip validation entirely
                frappe.msgprint("Warehouse Control validation bypassed (app is disabled)", 
                    indicator='blue', alert=True)
                return
    except Exception as e:
        # If settings don't exist or error occurs, continue with validation for safety
        frappe.log_error(f"Error checking Warehouse Control settings: {str(e)}")
        pass
    
    # Check if user should be exempted from validation
    if should_skip_validation():
        return
    
    # Perform warehouse validation
    validator = WarehouseAccessValidator(frappe.session.user)
    validator.validate_document(doc)


def should_skip_validation():
    """Check if current user should skip warehouse validation"""
    user = frappe.session.user
    
    # Skip for privileged users who can access all warehouses
    privileged_roles = ['System Manager', 'Stock Manager', 'Administrator']
    user_roles = frappe.get_roles(user)
    
    if any(role in user_roles for role in privileged_roles):
        return True
    
    # Skip for automated processes
    if user in ['Administrator', 'Guest']:
        return True
    
    return False


class WarehouseAccessValidator:
    """
    Validates warehouse access based on user's assigned building
    
    Business Rules:
    - Users can only SOURCE stock from their own building's warehouses + subcontractor warehouses
    - Users can TARGET stock to their own building's warehouses + ALL In Transit warehouses + subcontractor warehouses
    - Subcontractor warehouses are accessible by all users (both SOURCE and TARGET)
    - Privileged roles (System Manager, Stock Manager) bypass all restrictions
    """
    
    def __init__(self, user):
        self.user = user
        self.user_building = None
        self.allowed_source_warehouses = set()
        self.allowed_target_warehouses = set()
        self._load_user_permissions()
    
    def _load_user_permissions(self):
        """Load user's building and calculate allowed warehouses"""
        # Get user's assigned building
        self.user_building = frappe.db.get_value("User", self.user, "assigned_building")
        
        if not self.user_building:
            # User has no building assigned - no warehouse access
            return
        
        # Calculate allowed warehouses
        self._calculate_allowed_warehouses()
    
    def _calculate_allowed_warehouses(self):
        """Calculate which warehouses user can access as SOURCE and TARGET"""
        if not self.user_building:
            return
        
        # Get all warehouses
        all_warehouses = frappe.get_all("Warehouse", 
            fields=["name", "building", "warehouse_category"],
            filters={"disabled": 0})
        
        for wh in all_warehouses:
            warehouse_name = wh.name
            warehouse_building = wh.building
            warehouse_category = wh.warehouse_category
            
            # Subcontractor warehouses - accessible by everyone (SOURCE and TARGET)
            if warehouse_category == "Subcontractor":
                self.allowed_source_warehouses.add(warehouse_name)
                self.allowed_target_warehouses.add(warehouse_name)
                continue
            
            # Own building's warehouses - accessible as both SOURCE and TARGET
            if warehouse_building == self.user_building:
                self.allowed_source_warehouses.add(warehouse_name)
                self.allowed_target_warehouses.add(warehouse_name)
                continue
            
            # In Transit warehouses from OTHER buildings
            # Can ONLY be used as TARGET (not SOURCE)
            if warehouse_category == "In Transit":
                self.allowed_target_warehouses.add(warehouse_name)
                # Explicitly NOT added to source warehouses
    
    def _get_allowed_source_warehouses(self):
        """Get set of warehouses user can use as SOURCE"""
        return self.allowed_source_warehouses
    
    def _get_allowed_target_warehouses(self):
        """Get set of warehouses user can use as TARGET"""
        return self.allowed_target_warehouses
    
    def validate_warehouse(self, warehouse, warehouse_type, row_idx=None, doc_name=None):
        """
        Validate a single warehouse
        
        Args:
            warehouse: Warehouse name to validate
            warehouse_type: Either 'source' or 'target'
            row_idx: Row number in child table (for error messages)
            doc_name: Document name (for error messages)
        """
        if not warehouse:
            return  # Empty warehouse is handled by mandatory field validation
        
        if not self.user_building:
            frappe.throw(_(
                "You do not have a building assigned. "
                "Please contact your System Manager to assign you to a building."
            ))
        
        # Determine which set of allowed warehouses to check
        if warehouse_type == 'source':
            allowed_warehouses = self._get_allowed_source_warehouses()
        else:  # target
            allowed_warehouses = self._get_allowed_target_warehouses()
        
        # Check if warehouse is allowed
        if warehouse not in allowed_warehouses:
            # Get warehouse details for better error message
            wh_details = frappe.db.get_value("Warehouse", warehouse, 
                ["building", "warehouse_category"], as_dict=True)
            
            wh_building = wh_details.building if wh_details else "Unknown"
            wh_category = wh_details.warehouse_category if wh_details else "Regular"
            
            # Build error message
            row_info = f"Row #{row_idx}: " if row_idx else ""
            
            # Special message for In Transit warehouses from other buildings used as SOURCE
            if wh_category == "In Transit" and wh_building != self.user_building and warehouse_type == 'source':
                frappe.throw(_(
                    "{row_info}You cannot use In Transit warehouse <b>{warehouse}</b> from Building <b>{wh_building}</b> as SOURCE. "
                    "In Transit warehouses from other buildings can only be used as TARGET.<br><br>"
                    "Your assigned building is <b>{user_building}</b>."
                ).format(
                    row_info=row_info,
                    warehouse=warehouse,
                    wh_building=wh_building,
                    user_building=self.user_building
                ))
            
            # General access denied message
            frappe.throw(_(
                "{row_info}You do not have access to use warehouse <b>{warehouse}</b> as {warehouse_type}.<br>"
                "Warehouse Building: <b>{wh_building}</b><br>"
                "Warehouse Category: <b>{wh_category}</b><br><br>"
                "Your assigned building is <b>{user_building}</b>.<br><br>"
                "You can only {action} from: {allowed_list}"
            ).format(
                row_info=row_info,
                warehouse=warehouse,
                warehouse_type=warehouse_type.upper(),
                wh_building=wh_building or "Not Assigned",
                wh_category=wh_category or "Regular",
                user_building=self.user_building,
                action="source stock" if warehouse_type == 'source' else "send stock to",
                allowed_list=", ".join(sorted(list(allowed_warehouses)[:5])) + 
                    (f" and {len(allowed_warehouses) - 5} more" if len(allowed_warehouses) > 5 else "")
            ))
    
    def validate_document(self, doc):
        """
        Validate warehouse access for a document
        Routes to appropriate validator based on doctype
        """
        doctype = doc.doctype
        
        if doctype == "Stock Entry":
            self._validate_stock_entry(doc)
        elif doctype == "Purchase Receipt":
            self._validate_purchase_receipt(doc)
        elif doctype == "Purchase Invoice":
            self._validate_purchase_invoice(doc)
        elif doctype == "Sales Invoice":
            self._validate_sales_invoice(doc)
        elif doctype == "Delivery Note":
            self._validate_delivery_note(doc)
        elif doctype == "Subcontracting Receipt":
            self._validate_subcontracting_receipt(doc)
        elif doctype == "Stock Reconciliation":
            self._validate_stock_reconciliation(doc)
        elif doctype == "Material Request":
            self._validate_material_request(doc)
    
    def _validate_stock_entry(self, doc):
        """Validate Stock Entry - has both source and target warehouses"""
        # Special handling for "Send to Subcontractor" - only validate source
        if doc.purpose == "Send to Subcontractor":
            for idx, item in enumerate(doc.items, start=1):
                if item.s_warehouse:
                    self.validate_warehouse(item.s_warehouse, 'source', idx, doc.name)
            return
        
        # Regular Stock Entry - validate both source and target
        for idx, item in enumerate(doc.items, start=1):
            if item.s_warehouse:
                self.validate_warehouse(item.s_warehouse, 'source', idx, doc.name)
            if item.t_warehouse:
                self.validate_warehouse(item.t_warehouse, 'target', idx, doc.name)
    
    def _validate_purchase_receipt(self, doc):
        """Validate Purchase Receipt - warehouse is TARGET (receiving stock)"""
        for idx, item in enumerate(doc.items, start=1):
            if item.warehouse:
                self.validate_warehouse(item.warehouse, 'target', idx, doc.name)
            if item.rejected_warehouse:
                self.validate_warehouse(item.rejected_warehouse, 'target', idx, doc.name)
    
    def _validate_purchase_invoice(self, doc):
        """Validate Purchase Invoice - warehouse is TARGET (if update_stock is enabled)"""
        if not doc.update_stock:
            return  # No stock impact, skip validation
        
        for idx, item in enumerate(doc.items, start=1):
            if item.warehouse:
                self.validate_warehouse(item.warehouse, 'target', idx, doc.name)
    
    def _validate_sales_invoice(self, doc):
        """Validate Sales Invoice - warehouse is SOURCE (if update_stock is enabled)"""
        if not doc.update_stock:
            return  # No stock impact, skip validation
        
        for idx, item in enumerate(doc.items, start=1):
            if item.warehouse:
                self.validate_warehouse(item.warehouse, 'source', idx, doc.name)
    
    def _validate_delivery_note(self, doc):
        """Validate Delivery Note - warehouse is SOURCE (issuing stock)"""
        for idx, item in enumerate(doc.items, start=1):
            if item.warehouse:
                self.validate_warehouse(item.warehouse, 'source', idx, doc.name)
    
    def _validate_subcontracting_receipt(self, doc):
        """Validate Subcontracting Receipt - warehouse is TARGET, reserve_warehouse is SOURCE"""
        for idx, item in enumerate(doc.items, start=1):
            if item.warehouse:
                self.validate_warehouse(item.warehouse, 'target', idx, doc.name)
            if item.rejected_warehouse:
                self.validate_warehouse(item.rejected_warehouse, 'target', idx, doc.name)
        
        # Validate supplied items (reserve warehouse is SOURCE)
        for idx, supplied_item in enumerate(doc.supplied_items, start=1):
            if supplied_item.reserve_warehouse:
                self.validate_warehouse(supplied_item.reserve_warehouse, 'source', idx, doc.name)
    
    def _validate_stock_reconciliation(self, doc):
        """Validate Stock Reconciliation - warehouse is TARGET (can increase/decrease)"""
        for idx, item in enumerate(doc.items, start=1):
            if item.warehouse:
                self.validate_warehouse(item.warehouse, 'target', idx, doc.name)
    
    def _validate_material_request(self, doc):
        """Validate Material Request - only Material Transfer type has warehouses"""
        if doc.material_request_type != "Material Transfer":
            return  # Only validate Material Transfer type
        
        for idx, item in enumerate(doc.items, start=1):
            if item.from_warehouse:
                self.validate_warehouse(item.from_warehouse, 'source', idx, doc.name)
            if item.warehouse:
                self.validate_warehouse(item.warehouse, 'target', idx, doc.name)
