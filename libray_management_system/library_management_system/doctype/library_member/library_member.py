# Copyright (c) 2025, LMS and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class LibraryMember(Document):
		def validate(self):
        # Ensure full_name is auto-filled before saving
       		 self.full_name = f"{self.first_name or ''} {self.last_name or ''}".strip()
