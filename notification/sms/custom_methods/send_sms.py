import frappe
import africastalking
from water.custom_methods.reusable_methods import get_settings
from decouple import config


class SMSClass:
    '''
    This is the SMS sending class that uses Africa's talking 
    API to send sms
    '''
    def __init__(self):
        '''
        Class constructor
        '''
        #check if app is in production
        notification_settings = get_settings("Notifications Settings")
        if notification_settings.production:
            # upande credentials
            africastalking.initialize(
                username= config('africastalking_username_prod'),
                api_key=config('africastalking_api_key_prod')
            )
        else:
            # sandbox credetails
            africastalking.initialize(
                username= config('africastalking_username_test'),
                api_key=config('africastalking_api_key_test')
            )
        #add sms as an isinstance of the class
        self.sms_instance = africastalking.SMS

    def validate_message(self,message):
        '''
        Function that checks that the given message is valid and can be sent
        '''
        if message:
            return {'status':True}
        else:
            return {
                'status':False, 
                'message':'Message to send is not defined'
            }

    def validate_recipient_numbers(self,list_of_recipients):
        '''
        Function that checks that the given list of recipients is valid
        input:
            list_of_recipients - list
        '''
        invalid_recipients = []
        valid_recipients = []
        for recipient in list_of_recipients:
            #checks that the numbers start with +
            if type(recipient) != str:
                invalid_recipients.append(recipient)
                continue #to next recipient
            #check if the list starts with a +
            if recipient[0] != '+':
                invalid_recipients.append(recipient)
                continue #to next recipient
            #check the length of recipient numbers
            if len(recipient) != 13: #code + 
                invalid_recipients.append(recipient)
                continue #to next recipient
            #if all rules passed
            valid_recipients.append(recipient)
        
        #return list of both valid and invalid recipients
        return {
                'invalid_recipients':invalid_recipients,
                'valid_recipients':valid_recipients
            }

    def send_sms(self,message,list_of_recipients):
        '''
        Function that sends a given message a list of recipients
        input:
            message - str
            list_of_recipients - list
        '''
        try:
            response = self.sms_instance.send(message, list_of_recipients)
            #return the response message
            return response
        except Exception as e:
            #return and error is any was found
            return 'Sending Failed with the Error: {}'.format(e)

    def create_sms_queue(self,recipients,message,status):
        '''
        Function that create an email queue documents
        from lit of recipients and given message
        '''
        #loop through given list
        for recipient in recipients:
            #create sms queue documents
            sms_queue_doc = frappe.new_doc("SMS Queue")
            sms_queue_doc.recipient = recipient
            sms_queue_doc.message = message
            sms_queue_doc.status = status
            #save the document
            sms_queue_doc.save(ignore_permissions = True)
            frappe.db.commit()

    def message_sending_handler(self,message,recipients):
        #validate message
        message_validation = self.validate_message(message)
        if not message_validation['status']:
            frappe.msgprint("Message to send is not defined") 
        #validate recipients
        recipients_validation = self.validate_recipient_numbers(recipients)
        if len(recipients_validation['invalid_recipients']) > 0:
            #add functionality to track failed message here
            self.create_sms_queue(recipients_validation['invalid_recipients'],message,"Sending Failed")
        #send message for all valid recipients
        if len(recipients_validation['valid_recipients']) > 0:
            self.send_sms(message,recipients_validation['valid_recipients'])
