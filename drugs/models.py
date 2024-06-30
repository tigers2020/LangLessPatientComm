from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.html import mark_safe
from tinymce.models import HTMLField


class Condition(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='conditions/', blank=True, null=True)
    is_side_effect = models.BooleanField(default=True)  # False for symptom, True for side effect

    def __str__(self):
        return self.name.capitalize()

    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        super().save(*args, **kwargs)

    @property
    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="50" height="50" />')
        return "No Image"


class Route(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = HTMLField(blank=True, null=True)

    class Meta:
        verbose_name = 'Route'
        verbose_name_plural = 'Routes'

    def __str__(self):
        return f"{self.name.capitalize()}: {self.description[:40] if self.description else ''}..."

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


@receiver(pre_save, sender=Route)
def capitalize_name_on_presave(sender, instance, **kwargs):
    instance.name = instance.name.capitalize()

    def __repr__(self):
        return f"Route(name={self.name}, description={self.description})"


class Drug(models.Model):
    # Basic Information
    brand_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='drugs/', null=True, blank=True)

    # Route Information
    route = models.ForeignKey(Route, on_delete=models.CASCADE)

    # Drug Details
    description = models.TextField()
    uses = models.ManyToManyField(Condition, related_name='drugs_as_symptom')
    dosage = HTMLField()
    ingredients = HTMLField()
    side_effects = models.ManyToManyField(Condition, related_name='drugs_as_side_effect',
                                          limit_choices_to={'is_side_effect': True})
    full_product_details = models.FileField(upload_to='product_details/', null=True, blank=True)

    def __str__(self):
        return self.brand_name.capitalize()

    def save(self, *args, **kwargs):
        self.brand_name = self.brand_name.capitalize()
        super().save(*args, **kwargs)
