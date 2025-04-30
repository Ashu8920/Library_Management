// Copyright (c) 2025, LMS and contributors
// For license information, please see license.txt

frappe.ui.form.on("Library Member", {
    refresh: function (frm) {
        frm.add_custom_button("Create Membership", () => {
            frappe.new_doc("Library Membership", {
                member_name: frm.doc.name,
            });
        });
        frm.add_custom_button("Create Transaction", () => {
            frappe.new_doc("Library Transaction", {
                member_name: frm.doc.name,
            });
        });
    },

});
