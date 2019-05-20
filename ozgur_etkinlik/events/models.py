from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify, safe
from unidecode import unidecode
from uuid import uuid4
from django.shortcuts import reverse
from location_field.models.plain import PlainLocationField
import os

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


def upload_to(instance, filename):
    uzanti = filename.split('.')[-1]
    new_name = "%s.%s" % (str(uuid4()), uzanti)
    unique_id = instance.unique_id
    return os.path.join('event', unique_id, new_name)


class Event(models.Model):
    CATEGORY = (
        (None, 'Lütfen Seçiniz'), ('diğer', 'DİĞER'), ('yazılım', 'YAZILIM'), ('grafik tasarım', 'GRAFIK TASARIM'))

    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, verbose_name="Yazar", default=1)
    title = models.CharField(max_length=50, verbose_name="Başlık")
    content = RichTextField()
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    starter_date = models.DateTimeField(null=True, blank=True, verbose_name='Başlangıç tarihi')
    size = models.IntegerField(verbose_name='Katılımcı sayısı', null=True, default=0)
    city = models.CharField(max_length=255, null=True)
    location = PlainLocationField(based_fields=['City'], zoom=7, null=True)
    slug = models.SlugField(null=True, unique=True, editable=False, verbose_name='Slug')
    category = models.CharField(choices=CATEGORY, blank=True, null=True, max_length=53, verbose_name='Kategori')
    image = models.ImageField(default='default/marijuana.jpg', verbose_name='Resim', upload_to=upload_to,
                              null=True, help_text='Kapak Fotoğrafı Yükleyiniz', blank=True)

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

    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return '/media/default/marijuana.jpg'

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

    def get_event_new_comment(self):
        content_type = ContentType.objects.get_for_model(self)
        object_id = self.id
        all_comment = NewComment.objects.filter(content_type=content_type, object_id=object_id)
        return all_comment

    def get_event_comment_count(self):
        return len(self.get_event_new_comment())


class EventMember(models.Model):
    user = models.ForeignKey(User, null=True, default=1, related_name='event_member', on_delete=True)
    event = models.ForeignKey(Event, null=True, on_delete=True, related_name='event_member')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi", null=True)

    class Meta:
        verbose_name_plural = 'Etkinliğe gelen katılımcılar'

    def __str__(self):
        return "{} {}".format(self.user, self.event)


class NewComment(models.Model):
    user = models.ForeignKey(User, null=True, default=1, related_name='+', on_delete=True)
    is_parent = models.BooleanField(default=False)

    content_type = models.ForeignKey(to=ContentType, null=True, on_delete=True)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    icerik = models.TextField(verbose_name='Yorum', max_length=1000, blank=False, null=True)
    comment_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        username = self.user.username
        text = "{0} {1}".format(username, self.content_type.model)
        return text

    class Meta:
        verbose_name_plural = "İç içe yorum sistemi"

    @classmethod
    def add_comment(cls, nesne, model_type, user, icerik):
        content_type = ContentType.objects.get_for_model(nesne.__class__)
        cls.objects.create(user=user, icerik=icerik, content_type=content_type, object_id=nesne.pk)
        if model_type == 'comment':
            nesne.is_parent = True
            nesne.save()

    def get_child_comment(self):
        if self.is_parent:
            content_type = ContentType.objects.get_for_model(self.__class__)
            all_child_comment = NewComment.objects.filter(content_type=content_type, object_id=self.pk)
            return all_child_comment
        return None
