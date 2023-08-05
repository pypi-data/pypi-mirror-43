import requests
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from djangoldp.models import Model
from djangoldp_circle.models import Circle
from djangoldp_joboffer.models import JobOffer
from djangoldp_notification.models import Notification
from djangoldp_profile.models import Profile
from djangoldp_project.models import Project


@receiver(post_save, sender=Notification)
def send_email_on_notification(sender, instance, **kwargs):
    send_mail('Notification on staging.happy-dev.fr', instance.summary, 'from@example.com', [instance.user.email],
              fail_silently=False)


@receiver(post_save, sender=Profile)
def send_notification_on_new_profile(sender, instance, **kwargs):
    requests.post("https://jabber.happy-dev.fr/happydev_muc_admin/",
                  json={"@context": "https://cdn.happy-dev.fr/owl/hdcontext.jsonld",
                        "@graph": [{"object": str(instance.get_absolute_url()), "type": "Update"}]})


@receiver(post_save, sender=Project)
def send_notification_on_new_project(sender, instance, **kwargs):
    requests.post("https://jabber.happy-dev.fr/happydev_muc_admin/",
                  json={"@context": "https://cdn.happy-dev.fr/owl/hdcontext.jsonld",
                        "@graph": [{"object": str(instance.get_absolute_url()), "type": "Update"}]})


@receiver(post_save, sender=JobOffer)
def create_notifications_on_new_job_offer(sender, instance, **kwargs):
    for user in User.objects.all():
        if len(list(set(user.skills) & set(instance.skills))) > 0:
            Notification.objects.create(user=user,
                                        author_user=instance.author,
                                        object=Model.resource_id(instance),
                                        type="Job offer",
                                        summary=instance.title,
                                        read=False
                                        )


@receiver(post_save, sender=Circle)
def send_notification_on_new_circle(sender, instance, **kwargs):
    requests.post("https://jabber.happy-dev.fr/happydev_muc_admin/",
                  json={"@context": "https://cdn.happy-dev.fr/owl/hdcontext.jsonld",
                        "@graph": [{"object": str(instance.get_absolute_url()), "type": "Update"}]})
