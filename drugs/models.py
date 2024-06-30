from django.db import models
from tinymce.models import HTMLField


from django.db import models
from django.utils.html import mark_safe

# Symptom model to store symptoms treated by the drug, including an image
class Symptom(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='symptoms/', blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="50" height="50" />')
        return "No Image"

# SideEffect model to store possible side effects of the drug, including an image
class SideEffect(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='side_effects/', blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="50" height="50" />')
        return "No Image"


class Route(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Drug model to store drug information
class Drug(models.Model):
    # Basic Information
    brand_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='drugs/', null=True, blank=True)

    # Route Information
    route = models.ForeignKey(Route, on_delete=models.CASCADE)

    # Drug Details
    description = models.TextField()
    uses = models.ManyToManyField(Symptom, related_name='drugs')
    dosage = HTMLField()
    ingredients = HTMLField()
    side_effects = models.ManyToManyField(SideEffect, related_name='drugs')
    full_product_details = models.FileField(upload_to='product_details/', null=True, blank=True)

    def __str__(self):
        return self.brand_name
