from django.db import models
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
from django.conf import settings


class Invitation(models.Model):
    name = models.CharField(max_length=100)
    organization = models.CharField(max_length=100)
    email = models.EmailField()
    code = models.CharField(max_length=20)
    accepted = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.name

    def send_invite(self):
        subject = 'Invitation to join 360MedNet'
        link = 'http://%s/join/%s/' % (
            settings.SITE_HOST,
            self.code
        )
        template = get_template('invitation/invitation_email.txt')
        context = Context({
            'name': self.name,
            'organization': self.organization,
            'link': link,
        })
        message = template.render(context)
        send_mail(
            subject, message,
            settings.EMAIL_HOST_USER, [self.email]
        )


