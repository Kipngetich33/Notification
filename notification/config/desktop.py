# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"module_name": "Notification",
			"color": "grey",
			"icon": "octicon octicon-megaphone",
			"type": "module",
			"label": _("Notification")
		}
	]
