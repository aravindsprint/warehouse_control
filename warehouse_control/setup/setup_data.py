# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe

def setup_warehouse_control_data():
	"""Setup initial buildings, warehouses, and users"""
	
	print("\n" + "="*80)
	print("WAREHOUSE CONTROL - INITIAL DATA SETUP")
	print("="*80)
	
	# 1. Create Buildings
	print("\n1. Creating Buildings...")
	buildings_data = [
		{
			"building_name": "Building A",
			"building_code": "BLD-A",
			"company": "Your Company",
			"city": "Mumbai"
		},
		{
			"building_name": "Building B",
			"building_code": "BLD-B",
			"company": "Your Company",
			"city": "Delhi"
		},
		{
			"building_name": "Building C",
			"building_code": "BLD-C",
			"company": "Your Company",
			"city": "Bangalore"
		}
	]
	
	for building_data in buildings_data:
		if not frappe.db.exists("Building", building_data["building_name"]):
			building = frappe.get_doc({
				"doctype": "Building",
				**building_data
			})
			building.insert(ignore_permissions=True)
			print(f"  ✓ Created: {building_data['building_name']}")
		else:
			print(f"  - Already exists: {building_data['building_name']}")
	
	frappe.db.commit()
	
	# 2. Update Warehouses with Building Assignment
	print("\n2. Assigning Buildings to Warehouses...")
	warehouse_mapping = {
		# Building A Warehouses
		"Stores - YC": {"building": "Building A", "warehouse_category": "Regular"},
		"Work In Progress - YC": {"building": "Building A", "warehouse_category": "Work in Progress"},
		"Finished Goods - YC": {"building": "Building A", "warehouse_category": "Finished Goods"},
		
		# Create In Transit warehouses if they don't exist
		"In Transit - A": {
			"building": "Building A",
			"warehouse_category": "In Transit",
			"company": "Your Company",
			"create_if_not_exists": True
		},
		"In Transit - B": {
			"building": "Building B",
			"warehouse_category": "In Transit",
			"company": "Your Company",
			"create_if_not_exists": True
		},
		"In Transit - C": {
			"building": "Building C",
			"warehouse_category": "In Transit",
			"company": "Your Company",
			"create_if_not_exists": True
		}
	}
	
	for warehouse_name, data in warehouse_mapping.items():
		create_if_not_exists = data.pop("create_if_not_exists", False)
		
		if frappe.db.exists("Warehouse", warehouse_name):
			frappe.db.set_value("Warehouse", warehouse_name, {
				"building": data.get("building"),
				"warehouse_category": data.get("warehouse_category")
			})
			print(f"  ✓ Updated: {warehouse_name}")
		elif create_if_not_exists:
			wh = frappe.get_doc({
				"doctype": "Warehouse",
				"warehouse_name": warehouse_name,
				**data
			})
			wh.insert(ignore_permissions=True)
			print(f"  ✓ Created: {warehouse_name}")
		else:
			print(f"  ⚠ Warehouse not found: {warehouse_name}")
	
	frappe.db.commit()
	
	# 3. Assign Buildings to Users (Optional - uncomment to use)
	# print("\n3. Assigning Buildings to Users...")
	# user_building_map = {
	# 	"user1@yourcompany.com": "Building A",
	# 	"user2@yourcompany.com": "Building B"
	# }
	#
	# for user_email, building in user_building_map.items():
	# 	if frappe.db.exists("User", user_email):
	# 		frappe.db.set_value("User", user_email, "assigned_building", building)
	# 		print(f"  ✓ Assigned {building} to {user_email}")
	# 	else:
	# 		print(f"  ⚠ User not found: {user_email}")
	#
	# frappe.db.commit()
	
	print("\n" + "="*80)
	print("✓ SETUP COMPLETED SUCCESSFULLY!")
	print("="*80)
	print("\nNext Steps:")
	print("1. Review Buildings: Warehouse Control > Building")
	print("2. Review Warehouses: Stock > Warehouse")
	print("3. Assign users to buildings: Users > User > Assigned Building")
	print("="*80 + "\n")

# Run from Frappe Console:
# bench --site your-site.local console
# >>> from warehouse_control.setup.setup_data import setup_warehouse_control_data
# >>> setup_warehouse_control_data()
