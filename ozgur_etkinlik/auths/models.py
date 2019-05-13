from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True, blank=False, verbose_name='User', on_delete=True)

    class Meta:
        verbose_name_plural = 'Kullanıcı Profilleri'

    def __str__(self):
        return '{} Profile'.format(self.get_screen_name())

    def get_screen_name(self):
        user = self.user
        if user.get_full_name():
            return user.get_full_name()
        return user.username

    def create_profile(sender, created, instance, *args, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

        post_save.connect(create_profile, sender=User)