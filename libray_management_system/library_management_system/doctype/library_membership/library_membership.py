# Copyright (c) 2025, LMS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class LibraryMembership(Document):
    def before_submit(self):
        exists = frappe.db.exists(
            "Library Membership",
            {
                "member_name": self.member_name,
                "docstatus": 1,  # 1 = Submitted
                "to_date": (">", self.from_date),
            },
        )
        if exists:
            frappe.throw("There is an active membership for this member")
        # get loan period and compute to_date by adding loan_period to from_date
        loan_period = frappe.db.get_single_value("Library Settings", "loan_period")
        self.to_date = frappe.utils.add_days(self.from_date, loan_period or 30)