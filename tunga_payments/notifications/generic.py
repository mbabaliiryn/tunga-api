from django_rq import job

from tunga_payments.notifications.email import notify_invoice_email, notify_paid_invoice_email
from tunga_payments.notifications.slack import notify_invoice_slack_admin, notify_paid_invoice_slack_admin


@job
def notify_invoice(invoice, updated=False):
    # notify_invoice_email(invoice, updated=updated)
    notify_invoice_slack_admin(invoice, updated=updated)


@job
def notify_paid_invoice(invoice):
    notify_paid_invoice_email(invoice)
    notify_paid_invoice_slack_admin(invoice)
