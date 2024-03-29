// Copyright (c) 2019, Frappe Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on("Event Sync Log", {
	refresh: function (frm) {
		// todo: if it is Client Box - the logic should be reversed
		if (frm.doc.status == "Failed") {
			frm.add_custom_button(__("Resync"), function () {
				frappe.call({
					method: "data_sync.data_sync.doctype.event_producer.event_producer.resync",
					args: {
						update: frm.doc,
					},
					callback: function (r) {
						if (r.message) {
							frappe.msgprint(r.message);
							frm.set_value("status", r.message);
							frm.save();
						}
					},
				});
			});
		}
	},
});
