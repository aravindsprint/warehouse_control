# -*- coding: utf-8 -*-
# Copyright (c) 2024, Your Company and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Building(Document):
	def validate(self):
		"""Validate building data"""
		if self.building_code:
			self.building_code = self.building_code.upper()
	
	def on_trash(self):
		"""Prevent deletion if warehouses are assigned"""
		warehouses = frappe.get_all(
			"Warehouse",
			filters={"building": self.name},
			limit=1
		)
		
		if warehouses:
			frappe.throw(
				frappe._("Cannot delete Building {0} as it is assigned to warehouses. Please reassign warehouses first.").format(
					frappe.bold(self.name)
				)
			)
		
		# Check if users are assigned
		users = frappe.get_all(
			"User",
			filters={"assigned_building": self.name},
			limit=1
		)
		
		if users:
			frappe.throw(
				frappe._("Cannot delete Building {0} as it is assigned to users. Please reassign users first.").format(
					frappe.bold(self.name)
				)
			)
