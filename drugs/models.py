from django.db import models
from django.utils.html import mark_safe
from django_ckeditor_5.fields import CKEditor5Field


class Condition(models.Model):
    """
    Represents a medical Condition. It can be a side effect or a symptom depending on the is_side_effect flag.
    """
    name = models.CharField(max_length=100)  # The name of the condition
    image = models.ImageField(upload_to='conditions/', blank=True, null=True)  # The image of the condition (optional)
    is_side_effect = models.BooleanField(default=True)  # Flag indicating if the condition is a side effect

    def __str__(self):
        return self.name.capitalize()

    def save(self, *args, **kwargs):
        """
        Overrides the save method to auto capitalize the name of the condition before saving.
        """
        self.name = self.name.capitalize()
        super().save(*args, **kwargs)

    @property
    def image_tag(self):
        """
        Custom property that returns an HTML img tag containing the image of the condition (if it exists).
        Can be used in Django Admin to display the image of the condition.
        """
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="50" height="50" />')
        return "No Image"


class Route(models.Model):
    """
    Represents a Route of administration for a Drug.
    """
    name = models.CharField(max_length=100, unique=True)  # The name of the route (must be unique)
    description = CKEditor5Field(blank=True, null=True)  # The description of the route (optional)

    def __str__(self):
        return f"{self.name.capitalize()}: {self.description[:40] if self.description else ''}..."

    def save(self, *args, **kwargs):
        """Overrides the save method."""
        super().save(*args, **kwargs)

    def __repr__(self):
        """Representation string for Route object"""
        description = f", description={self.description}" if self.description is not None else ""
        return f"Route(name={self.name}{description})"


class Drug(models.Model):
    """
    Represents a Drug.
    """
    # Basic Information
    brand_name = models.CharField(max_length=255)  # The name of the drug
    image = models.ImageField(upload_to='drugs/', null=True, blank=True)  # The image of the drug (optional)

    # Route Information
    route = models.ForeignKey(Route, on_delete=models.CASCADE)  # The route of administration of the drug

    # Drug Details
    description = CKEditor5Field()  # The description of the drug
    uses = models.ManyToManyField(Condition,
                                  related_name='drugs_as_symptom')  # The conditions that the drug can be used to treat
    dosage = CKEditor5Field()  # The dosage instructions for the drug
    ingredients = CKEditor5Field()  # The active ingredients in the drug
    side_effects = models.ManyToManyField(Condition, related_name='drugs_as_side_effect',
                                          limit_choices_to={
                                              'is_side_effect': True})  # The potential side effects of the drug
    full_product_details = models.FileField(upload_to='product_details/', null=True,
                                            blank=True)  # The full details of the product (optional)

    def __str__(self):
        return self.brand_name.capitalize()

    def save(self, *args, **kwargs):
        """
        Overrides the save method to auto capitalize the brand name of the drug before saving.
        """
        self.brand_name = self.brand_name.capitalize()
        super().save(*args, **kwargs)
