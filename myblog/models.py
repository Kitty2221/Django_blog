from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to="profile_pics", blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    facebook = models.CharField(max_length=300, blank=True, null=True)
    instagram = models.CharField(max_length=300, blank=True, null=True)
    linkedin = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return str(self.user)


class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True, default='')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profile_pics", blank=True, null=True)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return str(self.author) + " Blog Title: " + self.title

    @staticmethod
    def get_absolute_url():
        return reverse('blogs')


