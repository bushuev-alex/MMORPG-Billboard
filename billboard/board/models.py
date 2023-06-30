from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime
from django.utils.translation import gettext


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}"


class Category(models.Model):
    tanks = 'TA'
    hills = 'HI'
    dds = 'DD'
    traders = 'TR'
    gildmasters = 'GD'
    qwestgivers = 'QG'
    blacksmiths = 'BS'
    tanners = 'TN'
    cookers = 'CO'
    masters = 'MA'

    POSITIONS = [
        (tanks, 'Танки'),
        (hills, 'Хилы'),
        (dds, 'ДД'),
        (traders, 'Торговцы'),
        (gildmasters, 'Гилдмастеры'),
        (gildmasters, 'Квестгиверы'),
        (qwestgivers, 'Уборщик'),
        (blacksmiths, 'Кузнецы'),
        (tanners, 'Кожевники'),
        (cookers, 'Зельевары'),
        (masters, 'Мастера заклинаний')
    ]
    name = models.CharField(max_length=2, unique=True, choices=POSITIONS, default=masters)
    subscribers = models.ManyToManyField(User, blank=True, null=True, related_name='categories')

    def __str__(self):
        return f"{self.name}"


class Advertisement(models.Model):

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='AdvertisementCategory')
    title = models.TextField()
    text = models.TextField()

    def preview(self):
        if len(self.text) < 124:
            return self.text[:len(self.text)]
        return self.text[:124] + "..."

    def __str__(self):
        return f"{self.title}: {self.text[:124]}"

    def get_absolute_url(self):
        return reverse('ad_detail', args=[str(self.id)])


class AdvertisementCategory(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Feedback(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

