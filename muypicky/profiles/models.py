from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.core.urlresolvers import reverse

from .utils import code_generator


User = settings.AUTH_USER_MODEL

class ProfileManager(models.Manager):
    def toggle_follow(self, requested_user, username_to_toggle):
        f_profile = Profile.objects.get(user__username__iexact=username_to_toggle)
        logged_user = requested_user
        is_following = False

        if logged_user in f_profile.followers.all():
            f_profile.followers.remove(logged_user)
        else:
            f_profile.followers.add(logged_user)
            is_following = True
        return f_profile, is_following


class Profile(models.Model):
    user            = models.OneToOneField(User) # user.profile
    followers       = models.ManyToManyField(User, related_name='is_following', blank=True) # user.followers.all()
    # fallowing   = models.ManyToManyField(User, related_name='following', blank=True) # user.following.all()
    activation_key  = models.CharField(max_length= 120, blank=True, null=True)
    activated       = models.BooleanField(default=False)

    objects = ProfileManager()

    def __str__(self):
        return self.user.username

    def send_activation_email(self):
        if not self.activated:
            self.activation_key = code_generator(25)
            self.save()

            path_ = reverse('activate', kwargs={"code": self.activation_key})
            subject = 'Activate Account'
            from_email = settings.DEFAULT_FROM_EMAIL
            message = 'activate {}'.format(path_)
            recipient_list = [self.user.email]
            html_message = '<h1> This is activation email {}</h1>'.format(path_)
            sent_mail = send_mail(subject, message,from_email, recipient_list, fail_silently=False)
            print(html_message)
            # sent_mail = False
            return sent_mail

def post_save_user_receiver(sender, instance, created, *args, **kwargs):
    if created:
        profile, is_created = Profile.objects.get_or_create(user=instance)

post_save.connect(post_save_user_receiver, sender=User)