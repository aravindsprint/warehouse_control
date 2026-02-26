# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Masters"),
			"items": [
				{
					"type": "doctype",
					"name": "Building",
					"description": _("Manage company buildings and locations")
				}
			]
		},
		{
			"label": _("Setup"),
			"items": [
				{
					"type": "doctype",
					"name": "Warehouse",
					"description": _("Assign warehouses to buildings")
				},
				{
					"type": "doctype",
					"name": "User",
					"description": _("Assign users to buildings")
				}
			]
		}
	]
