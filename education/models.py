# File: education/models.py

from django_ckeditor_5.fields import CKEditor5Field
from django.db import models

class Scenario(models.Model):
    """
    Model representing a scenario.
    """
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/scenario/')  # Images will be uploaded to 'images/scenario/'
    description = CKEditor5Field()  # Rich text field for scenario description
    created_at = models.DateTimeField(auto_now_add=True)  # Set to now when the object is first created
    updated_at = models.DateTimeField(auto_now=True)  # Set to now every time the object is saved

    def __str__(self):
        """
        String representation of the Scenario model.
        """
        return self.title

class Page(models.Model):
    """
    Model representing a page within a scenario.
    """
    scenario = models.ForeignKey(Scenario, related_name='pages', on_delete=models.CASCADE)
    content = CKEditor5Field()  # Rich text field for page content
    order = models.IntegerField(default=0)

    def __str__(self):
        """
        String representation of the Page model.
        """
        return f"{self.scenario.title} - Page {self.order}"

class Image(models.Model):
    """
    Model representing an image associated with a page.
    """
    page = models.ForeignKey(Page, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/scenario_images/')  # Images will be uploaded to 'images/scenario_images/'
    caption = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        """
        String representation of the Image model.
        """
        return f"Image for {self.page} - Order {self.order}"

class Choice(models.Model):
    """
    Model representing a choice within a page.
    """
    page = models.ForeignKey(Page, related_name='choices', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/choice/')  # Images will be uploaded to 'images/choice/'
    text = models.CharField(max_length=200)
    next_page = models.ForeignKey(Page, related_name='leading_choices', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        """
        String representation of the Choice model.
        """
        return f"Choice on {self.page} - {self.text}"

class Outcome(models.Model):
    """
    Model representing an outcome of a page.
    """
    page = models.OneToOneField(Page, related_name='outcome', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/outcome/')  # Images will be uploaded to 'images/outcome/'
    description = models.TextField()
    next_scenario = models.ForeignKey(Scenario, related_name='next_outcome', on_delete=models.SET_NULL, null=True, blank=True)
    is_end = models.BooleanField(default=False)

    def __str__(self):
        """
        String representation of the Outcome model.
        """
        return f"Outcome for {self.page}"
