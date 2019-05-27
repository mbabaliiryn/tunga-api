from actstream import action
from django.db.models.signals import post_save
from django.dispatch import receiver

from tunga_activity import verbs
from tunga_payments.models import Invoice, Payment
from tunga_payments.notifications.generic import notify_invoice


@receiver(post_save, sender=Invoice)
def activity_handler_new_invoice(sender, instance, created, **kwargs):
    if created:
        if not instance.legacy_id:
            action.send(instance.created_by, verb=verbs.CREATE, action_object=instance, target=instance.project)

        if not instance.number:
            # generate and save invoice number
            invoice_number = instance.generate_invoice_number()
            instance.number = invoice_number
            Invoice.objects.filter(id=instance.id).update(number=invoice_number)

        notify_invoice.delay(instance.id, updated=False)


@receiver(post_save, sender=Payment)
def activity_handler_new_payment(sender, instance, created, **kwargs):
    if created and not instance.legacy_id:
        action.send(
            instance.created_by or instance.invoice.created_by,
            verb=verbs.CREATE, action_object=instance, target=instance.invoice
        )
