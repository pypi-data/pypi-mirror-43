import requests
import logging
import datetime
from threading import Thread

from django.contrib.sessions.models import Session
from django.db import models
from django.conf import settings
from djangoldp.fields import LDPUrlField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.admin.models import LogEntry
from djangoldp.models import Model

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='inbox')
    author_user = LDPUrlField()
    object = LDPUrlField()
    type = models.CharField(max_length=255)
    summary = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField()
    class Meta:
        permissions = (
            ('view_notification', 'Read'),
            ('control_notification', 'Control'),
        )
        ordering = ['date']

    def __str__(self):
        return '{}'.format(self.type)

class Subscription(models.Model):
    object = models.URLField()
    inbox = models.URLField()

    class Meta:
        permissions = (
            ('view_notification', 'Read'),
            ('control_notification', 'Control'),
        )

    def __str__(self):
        return '{}'.format(self.object)

# --- SUBSCRIPTION SYSTEM ---
@receiver(post_save, dispatch_uid="callback_notif")
def send_notification(sender, instance, **kwargs):
    if (sender != Notification and sender != LogEntry and sender != Session):
        threads = []
        url = settings.BASE_URL + Model.resource_id(instance) + '/'
        for subscription in Subscription.objects.filter(object=url):
            process = Thread(target=send_request, args=[subscription.inbox, url])
            process.start()
            threads.append(process)
def send_request(target, object_iri):
    try:
        req=requests.post(target,
            json={"@context":"https://cdn.happy-dev.fr/owl/hdcontext.jsonld",
                "object": object_iri, "type": "update"},
            headers={"Content-Type": "application/ld+json"})
    except:
        logging.error('Djangoldp_notifications: Error with request')
    return True