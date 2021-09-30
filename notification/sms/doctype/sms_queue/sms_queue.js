// Copyright (c) 2021, Upande LTD. and contributors
// For license information, please see license.txt

frappe.ui.form.on('SMS Queue', {
	// refresh: function(frm) {
	// }
});

//functions that runs when the confirm_readings button is clicked
frappe.ui.form.on("SMS Queue", "resend", function(frm){
	//mark check resend so that sms tries to resend
	cur_frm.set_value('resending',1)
	cur_frm.save()
})