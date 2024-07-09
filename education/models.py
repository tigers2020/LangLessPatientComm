# src/education/models.py
from django_ckeditor_5.fields import CKEditor5Field
from django.db import models

class Scenario(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/scenario/')
    description = CKEditor5Field()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Page(models.Model):
    scenario = models.ForeignKey(Scenario, related_name='pages', on_delete=models.CASCADE)
    content = CKEditor5Field()
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.scenario.title} - Page {self.order}"

class Image(models.Model):
    page = models.ForeignKey(Page, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/scenario_images/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"Image for {self.page} - Order {self.order}"

class Choice(models.Model):
    page = models.ForeignKey(Page, related_name='choices', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/choice/')
    text = models.CharField(max_length=200)
    next_page = models.ForeignKey(Page, related_name='leading_choices', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Choice on {self.page} - {self.text}"

class Outcome(models.Model):
    page = models.OneToOneField(Page, related_name='outcome', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/outcome/')
    description = models.TextField()
    next_scenario = models.ForeignKey(Scenario, related_name='next_outcome', on_delete=models.SET_NULL, null=True, blank=True)
    is_end = models.BooleanField(default=False)

    def __str__(self):
        return f"Outcome for {self.page}"
