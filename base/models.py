import calendar
import json
from datetime import datetime, timedelta

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, SendAt

# Create your models here.


class Lead(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    created_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name


@receiver(post_save, sender=Lead)
def send_lead_email(sender, instance, created, **kwargs):
    if created:
        hour = datetime.now() + timedelta(minutes=15)

        send_time = calendar.timegm(hour.timetuple())

        first, *last = instance.name.split()

        message = Mail(
            from_email=settings.DEFAULT_FROM_EMAIL,
            to_emails=instance.email,
            subject='FFN Enquiry',
            plain_text_content="Hi {},\n\nThank you for expressing interest in getting started with us. Have you ever receivec any nutritional coaching before?\n\nRegards,\n\nLindsey, Female Fight Nutritionist".format(first))
        message.reply_to = {settings.DEFAULT_FROM_EMAIL}
        message.send_at = SendAt(send_time)

        try:
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            response = sg.send(message)
        except Exception as error:
            print(error)
