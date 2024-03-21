// Copyright (c) 2024, CloudGCS Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on("Event Server", {
	refresh: function(frm) {
    frappe.db.get_single_value('Box Settings', 'box_type')
      .then(box_type => {
        if (box_type == "Service Box")
          // Custom buttons
          frm.add_custom_button('Sync with Server as Consumer', () => {
            frappe.call({
              method: "data_sync.data_sync.doctype.event_server.event_server.sync_server",
              args: {
                
              },
              freeze: true,
              callback: function (r) {
                frappe.msgprint("The Event Consumer for the server is updated");
              },
              error: (r) => {
                frappe.msgprint("Something went wrong, please try again later\n" + r.message);
              }
            });
          })
          frm.add_custom_button('Pull Data as Consumer', () => {
            frappe.call({
              method: "data_sync.data_sync.doctype.event_server.event_server.pull_data",
              args: {
                
              },
              freeze: true,
              callback: function (r) {
                frappe.msgprint("Data pull is scheduled, please wait for a few minutes");
              },
              error: (r) => {
                frappe.msgprint("Something went wrong, please try again later\n" + r.message);
              }
            });
          })
          // Custom buttons
          frm.add_custom_button('Push Data as Producer', () => {
            frappe.call({
              method: "data_sync.data_sync.doctype.event_server.event_server.push_data",
              args: {
                
              },
              freeze: true,
              callback: function (r) {
                frappe.msgprint("Data pull is scheduled, please wait for a few minutes");
              },
              error: (r) => {
                frappe.msgprint("Something went wrong, please try again later\n" + r.message);
              }
            });
          })
      })
  }
});
