# File: drugs/models.py

from django.db import models
from django.utils.html import mark_safe
from django_ckeditor_5.fields import CKEditor5Field

class Condition(models.Model):
    """
    Represents a medical condition, which can be either a side effect or a symptom.
    """
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='conditions/', blank=True, null=True)
    is_side_effect = models.BooleanField(default=True)  # True if condition is a side effect, False if it's a symptom

    def __str__(self):
        """
        Returns the name of the condition, capitalized.
        """
        return self.name.capitalize()

    def save(self, *args, **kwargs):
        """
        Override the save method to auto-capitalize the name before saving.
        """
        self.name = self.name.capitalize()
        super().save(*args, **kwargs)

    @property
    def image_tag(self):
        """
        Returns an HTML img tag for displaying the image in the admin interface.
        """
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="50" height="50" />')
        return "No Image"

class Route(models.Model):
    """
    Represents a drug administration route (e.g., oral, intravenous).
    """
    name = models.CharField(max_length=100, unique=True)
    description = CKEditor5Field(blank=True, null=True)

    def __str__(self):
        """
        Returns a string representation of the route.
        """
        return f"{self.name.capitalize()}: {self.description[:40] if self.description else ''}..."

    def __repr__(self):
        """
        Returns a detailed string representation for debugging purposes.
        """
        description = f", description={self.description}" if self.description is not None else ""
        return f"Route(name={self.name}{description})"

class Drug(models.Model):
    """
    Represents a pharmaceutical drug.
    """
    brand_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='drugs/', null=True, blank=True)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)  # Administration route
    description = CKEditor5Field()
    uses = models.ManyToManyField(Condition, related_name='drugs_as_symptom')  # Conditions this drug treats
    dosage = CKEditor5Field()
    ingredients = CKEditor5Field()
    side_effects = models.ManyToManyField(
        Condition,
        related_name='drugs_as_side_effect',
        limit_choices_to={'is_side_effect': True}  # Ensure only side effects can be selected
    )
    full_product_details = models.FileField(upload_to='product_details/', null=True, blank=True)

    def __str__(self):
        """
        Returns the brand name of the drug, capitalized.
        """
        return self.brand_name.capitalize()

    def save(self, *args, **kwargs):
        """
        Override the save method to auto-capitalize the brand name before saving.
        """
        self.brand_name = self.brand_name.capitalize()
        super().save(*args, **kwargs)
