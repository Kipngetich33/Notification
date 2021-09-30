from __future__ import unicode_literals
from frappe import _
import frappe


def get_data():
    config = [
		{
			"label": _("SMS Queue"),
			"items": [
				{
					"type": "doctype",
					"name": "SMS Queue",
					"description": _("SMS Queue"),
					"onboard": 1,
				},
				{
					"type": "doctype",
					"name": "Notifications Settings",
					"description": _("Notifications Settings"),
					"onboard": 1,
				}
            ]
        }]
    return config