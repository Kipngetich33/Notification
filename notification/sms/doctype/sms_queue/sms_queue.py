# -*- coding: utf-8 -*-
# Copyright (c) 2021, Upande LTD. and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from ...custom_methods.send_sms import SMSClass

class SMSQueue(Document):
	'''
	SMS Queue document class
	'''
	def validate(self):
		'''
		Methods that validates the SMS Queue document
		before saving
		'''
		#check if user is trying to resend sms
		if not self.resending:
			#instanciate SMSClass
			self.sms_class_instance = SMSClass()
			#validate the message
			message_validation = self.sms_class_instance.validate_message(self.message)
			if not message_validation['status']:
				return frappe.throw("The given message is invalid")
			#validate recipient number
			recipient_validation = self.sms_class_instance.validate_recipient_numbers([self.recipient])
			if len(recipient_validation['invalid_recipients']) > 0:
				return frappe.throw("Invalid recipient number")

	def before_save(self):
		'''
		Function that runs before the document is saved
		'''
		#check if user is trying to resend sms
		if self.resending:
			if not hasattr(self,'sms_class_instance'):
				#instanciate SMSClass
				self.sms_class_instance = SMSClass()
			#if validation passes send message
			self.sms_class_instance.message_sending_handler(self.message,[self.recipient])
			#mark as sent
			self.status = "Sent"
			#unmark sending
			self.resending = 0
			