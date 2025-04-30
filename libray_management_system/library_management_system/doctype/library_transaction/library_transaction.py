# Copyright (c) 2025, LMS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.base_document import DocStatus
from frappe.model.document import Document


class LibraryTransaction(Document):
    def before_submit(self):
        if self.type == "Issue":
            self.validate_maximum_limit()
            self.validate_issue()
            
            # set the article status to be Issued
            article = frappe.get_doc("Article", self.article_name)
            article.status = "Issued"
            article.save()

        elif self.type == "Return":
            self.validate_return()
            # set the article status to be Available
            article = frappe.get_doc("Article", self.article_name)
            article.status = "Available"
            article.save()

    def validate_issue(self):
        self.validate_membership()
        article = frappe.get_doc("Article", self.article_name)
        # article cannot be issued if it is already issued
        if article.status == "Issued":
            frappe.throw("Article is already issued by another member")

    def validate_return(self):
        article = frappe.get_doc("Article", self.article_name)
        # article cannot be returned if it is not issued first
        if article.status == "Available":
            frappe.throw("Article cannot be returned without being issued first")
    
    #Validate maximum number 
    def validate_maximum_limit(self):
        max_articles = frappe.db.get_single_value("Library Settings", "article_issue_length")
        count = frappe.db.count(
        "Library Transaction",
        {"library_member": self.library_member, "type": "Issue", "docstatus": DocStatus.submitted()},
         )
        if count >= max_articles:
            frappe.throw("Maximum limit reached for issuing articles")
    def validate_membership(self):
        # check if a valid membership exists for this library member
        valid_membership = frappe.db.exists(
            "Library Membership",
            {
                "member_name": self.library_member,
                "docstatus": 1,  # 1 means Submitted
                "to_date": (">", self.transaction_date)
            },
        )
        if not valid_membership:
            frappe.throw("The member does not have a valid membership")
