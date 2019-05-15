from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify, safe
from unidecode import unidecode
from uuid import uuid4
from django.shortcuts import reverse
from location_field.models.plain import PlainLocationField


# Create your models here.

class Event(models.Model):
    CATEGORY = (
        (None, 'Lütfen Seçiniz'), ('diğer', 'DİĞER'), ('yazılım', 'YAZILIM'), ('grafik tasarım', 'GRAFIK TASARIM'))

    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, verbose_name="Yazar", default=1)
    title = models.CharField(max_length=50, verbose_name="Başlık")
    content = RichTextField()
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    starter_date = models.DateTimeField(null=True, blank=True, verbose_name='Başlangıç tarihi')
    finish_date = models.DateTimeField(null=True, blank=True, verbose_name='Bitiş Tarihi')
    size = models.IntegerField(verbose_name='Katılımcı sayısı', null=True, default=0)
    city = models.CharField(max_length=255, null=True)
    location = PlainLocationField(based_fields=['City'], zoom=7, null=True)
    slug = models.SlugField(null=True, unique=True, editable=False, verbose_name='Slug')
    category = models.CharField(choices=CATEGORY, blank=True, null=True, max_length=53, verbose_name='Kategori')

    def __str__(self):
        return self.title

    def get_come_event_count(self):
        etkinlige_gelen = self.event_member.count()
        return etkinlige_gelen

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug': self.slug})

    def get_come_event_object(self):
        data_list = []
        qs = self.event_member.all()
        for obj in qs:
            data_list.append(obj.user)
        return data_list

    def get_unique_slug(self):
        sayi = 0
        slug = slugify(unidecode(self.title))
        new_slug = slug
        while Event.objects.filter(slug=new_slug).exists():
            sayi += 1
            new_slug = "%s-%s" % (slug, sayi)
        slug = new_slug
        return slug

    def save(self, *args, **kwargs):
        if self.id is None:
            self.unique_id = str(uuid4())
            self.slug = self.get_unique_slug()
        else:
            event = Event.objects.get(slug=self.slug)
            if event.title != self.title:
                self.slug = self.get_unique_slug()

        super(Event, self).save(*args, **kwargs)


class EventMember(models.Model):
    user = models.ForeignKey(User, null=True, default=1, related_name='event_member', on_delete=True)
    event = models.ForeignKey(Event, null=True, on_delete=True, related_name='event_member')

    class Meta:
        verbose_name_plural = 'Etkinliğe gelen katılımcılar'

    def __str__(self):
        return "{} {}".format(self.user, self.event)
