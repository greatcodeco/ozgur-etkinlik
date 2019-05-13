from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User


# Create your models here.

class Event(models.Model):
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE, verbose_name="Yazar")
    title = models.CharField(max_length=50, verbose_name="Başlık")
    content = RichTextField()
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    starter_date = models.CharField(max_length=10, verbose_name="Bitirilmesi Gereken Tarih", default='')

    def __str__(self):
        return self.title

    def get_come_event_count(self):
        etkinlige_gelen = self.event_member.count()
        return etkinlige_gelen

    def get_come_event_object(self):
        data_list = []
        qs = self.event_member.all()
        for obj in qs:
            data_list.append(obj.user)
        return data_list


class EventMember(models.Model):
    user = models.ForeignKey(User, null=True, default=1, related_name='event_member', on_delete=True)
    event = models.ForeignKey(Event, null=True, on_delete=True, related_name='event_member')

    class Meta:
        verbose_name_plural = 'Etkinliğe gelen katılımcılar'

    def __str__(self):
        return "{} {}".format(self.user, self.event)
