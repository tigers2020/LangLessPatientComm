# src/education/models.py

# Import necessary modules
from django_ckeditor_5.fields import CKEditor5Field
from django.db import models


# Scenario model
class Scenario(models.Model):
    # Fields definition
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/scenario/')  # Images will be uploaded to 'images/scenario/'
    description = CKEditor5Field()  # Rich text field
    created_at = models.DateTimeField(
        auto_now_add=True)  # Automatically set the field to now when the object is first created
    updated_at = models.DateTimeField(
        auto_now=True)  # Automatically set the field to now every time the object is saved

    # String representation of the model
    def __str__(self):
        return self.title


# Page model
class Page(models.Model):
    # Fields definition
    scenario = models.ForeignKey(Scenario, related_name='pages', on_delete=models.CASCADE)
    content = CKEditor5Field()  # Rich text field
    order = models.IntegerField(default=0)

    # String representation of the model
    def __str__(self):
        return f"{self.scenario.title} - Page {self.order}"


# Image model
class Image(models.Model):
    # Fields definition
    page = models.ForeignKey(Page, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='images/scenario_images/')  # Images will be uploaded to 'images/scenario_images/'
    caption = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)

    # String representation of the model
    def __str__(self):
        return f"Image for {self.page} - Order {self.order}"


# Choice model
class Choice(models.Model):
    # Fields definition
    page = models.ForeignKey(Page, related_name='choices', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/choice/')  # Images will be uploaded to 'images/choice/'
    text = models.CharField(max_length=200)
    next_page = models.ForeignKey(Page, related_name='leading_choices', on_delete=models.SET_NULL, null=True,
                                  blank=True)

    # String representation of the model
    def __str__(self):
        return f"Choice on {self.page} - {self.text}"


# Outcome model
class Outcome(models.Model):
    # Fields definition
    page = models.OneToOneField(Page, related_name='outcome', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/outcome/')  # Images will be uploaded to 'images/outcome/'
    description = models.TextField()
    next_scenario = models.ForeignKey(Scenario, related_name='next_outcome', on_delete=models.SET_NULL, null=True,
                                      blank=True)
    is_end = models.BooleanField(default=False)

    # String representation of the model
    def __str__(self):
        return f"Outcome for {self.page}"
