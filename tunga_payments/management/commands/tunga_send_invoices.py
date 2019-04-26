import datetime

from django.core.management.base import BaseCommand

from tunga_payments.models import Invoice
from tunga_payments.notifications.email import notify_new_invoice_email_client
from tunga_utils.constants import INVOICE_TYPE_SALE


class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        Schedule progress updates and send update reminders
        """
        # command to run: python manage.py tunga_send_invoices

        today_end = datetime.datetime.utcnow().replace(hour=23, minute=59, second=59, microsecond=999999)

        invoices = Invoice.objects.filter(
            type=INVOICE_TYPE_SALE, paid=False, issued_at__lte=today_end,
            last_sent_at__isnull=True, legacy_id__isnull=True, finalized=True
        )
        for invoice in invoices:
            notify_new_invoice_email_client.delay(invoice.id)
