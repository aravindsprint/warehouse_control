# -*- coding: utf-8 -*-
# Copyright (c) 2024, Your Company and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from warehouse_control.custom_fields.warehouse_building import setup_custom_fields

def after_install():
	"""
	Called after app installation
	Setup custom fields and initial configuration
	"""
	print("\n" + "="*80)
	print("Installing Warehouse Control App")
	print("="*80)
	
	# Create custom fields
	print("\n1. Creating custom fields...")
	setup_custom_fields()
	
	# Create sample buildings (optional - commented out by default)
	# create_sample_buildings()
	
	print("\n" + "="*80)
	print("Warehouse Control App installed successfully!")
	print("="*80)
	print("\nNext Steps:")
	print("1. Go to: Warehouse Control > Building")
	print("2. Create your buildings")
	print("3. Assign buildings to warehouses")
	print("4. Assign buildings to users")
	print("="*80 + "\n")

def create_sample_buildings():
	"""Create sample buildings for testing"""
	buildings = [
		{"building_name": "Building A", "building_code": "BLD-A"},
		{"building_name": "Building B", "building_code": "BLD-B"},
		{"building_name": "Building C", "building_code": "BLD-C"}
	]
	
	for building_data in buildings:
		if not frappe.db.exists("Building", building_data["building_name"]):
			building = frappe.get_doc({
				"doctype": "Building",
				**building_data
			})
			building.insert(ignore_permissions=True)
			print(f"Created Building: {building_data['building_name']}")
	
	frappe.db.commit()
