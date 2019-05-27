from allauth.account.models import EmailAddress
from allauth.account.signals import user_signed_up
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

from tunga_auth.models import EmailVisitor
from tunga_auth.notifications import send_new_user_joined_email, send_new_user_password_email
from tunga_auth.tasks import sync_hubspot_contact, sync_hubspot_email
from tunga_projects.notifications.slack import notify_new_user_signup_on_platform
from tunga_utils import algolia_utils
from tunga_utils.constants import USER_TYPE_PROJECT_OWNER, USER_SOURCE_MANUAL
from tunga_utils.serializers import SearchUserSerializer


@receiver(post_save, sender=get_user_model())
def activity_handler_new_user(sender, instance, created, **kwargs):
    if created and instance.source == USER_SOURCE_MANUAL:
        if not EmailAddress.objects.filter(email=instance.email).count():
            email_address = EmailAddress.objects.add_email(
                None, instance, instance.email
            )

            email_address.verified = True
            email_address.primary = True
            email_address.save()

        send_new_user_password_email.delay(instance.id)

        if instance.is_developer:
            algolia_utils.add_objects([SearchUserSerializer(instance).data])


@receiver(user_signed_up)
def activity_handler_new_signup(request, user, **kwargs):
    notify_new_user_signup_on_platform.delay(user.id)

    if user.type == USER_TYPE_PROJECT_OWNER:
        sync_hubspot_contact.delay(user.id)


@receiver(post_save, sender=EmailVisitor)
def activity_handler_new_email_visitor(sender, instance, created, **kwargs):
    if created:
        sync_hubspot_email.delay(instance.email)
