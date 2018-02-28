from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.management import call_command
from django.core.management.base import BaseCommand

scheduler = BlockingScheduler()


@scheduler.scheduled_job('interval', minutes=5)
def manage_task_payments_and_progress():
    # Distribute task payments to participants
    call_command('tunga_distribute_task_payments_payoneer')

    # Update periodic task progress events
    call_command('tunga_manage_task_progress')


@scheduler.scheduled_job('interval', minutes=10)
def send_message_emails():
    # Send new message emails for conversations
    call_command('tunga_send_message_emails')

    # Send new activity emails for tasks
    call_command('tunga_send_task_activity_emails')

    # Send new message emails for customer support conversations
    call_command('tunga_send_customer_emails')

@scheduler.scheduled_job('interval', minutes=1)
def invoice_reminder():
    # Send new message emails for conversations
    print "Sending reminder for 14 days"
    call_command('tunga_invoice_reminder')
    
@scheduler.scheduled_job('interval', minutes=2)
def invoice_reminder():
    # Send email and slack for notification.
    print "Sending reminder 21 days"
    call_command('tunga_invoice_reminder_3_weeks')

class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        Run tunga periodic (cron) tasks.
        """
        # command to run: python manage.py tunga_scheduler

        scheduler.start()
