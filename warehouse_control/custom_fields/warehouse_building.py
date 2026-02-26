# -*- coding: utf-8 -*-
# Copyright (c) 2024, Your Company and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def setup_custom_fields():
	"""Create custom fields for Warehouse and User"""
	
	custom_fields = {
		"Warehouse": [
			{
				"fieldname": "building_section",
				"label": "Building Assignment",
				"fieldtype": "Section Break",
				"insert_after": "company",
				"collapsible": 0
			},
			{
				"fieldname": "building",
				"label": "Building",
				"fieldtype": "Link",
				"options": "Building",
				"insert_after": "building_section",
				"in_list_view": 1,
				"in_standard_filter": 1,
				"translatable": 0
			},
			{
				"fieldname": "warehouse_category",
				"label": "Warehouse Category",
				"fieldtype": "Select",
				"options": "\nRegular\nIn Transit\nWork in Progress\nSubcontractor\nFinished Goods\nScrap",
				"insert_after": "building",
				"in_list_view": 1,
				"in_standard_filter": 1,
				"default": "Regular"
			},
			{
				"fieldname": "building_column_break",
				"fieldtype": "Column Break",
				"insert_after": "warehouse_category"
			}
		],
		"User": [
			{
				"fieldname": "warehouse_control_section",
				"label": "Warehouse Control",
				"fieldtype": "Section Break",
				"insert_after": "location",
				"collapsible": 1,
				"collapsible_depends_on": "assigned_building"
			},
			{
				"fieldname": "assigned_building",
				"label": "Assigned Building",
				"fieldtype": "Link",
				"options": "Building",
				"insert_after": "warehouse_control_section",
				"description": "User will only be able to transfer stock within this building and to In Transit warehouses of other buildings"
			}
		]
	}
	
	create_custom_fields(custom_fields, update=True)
	
	frappe.db.commit()
	print("Custom fields created successfully!")
