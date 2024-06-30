from django.db import models
from tinymce.models import HTMLField


class TeamMember(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    description = HTMLField()
    image_src = models.ImageField(upload_to='team_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name}  {self.last_name}"


class MissionContent(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True, null=True)
    content = HTMLField()
    image = models.ImageField(upload_to='mission_images/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
