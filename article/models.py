# models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field


# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Name field, must be unique
    slug = models.SlugField(max_length=100, unique=True)  # Slug field, used in urls, must be unique
    description = CKEditor5Field(blank=True)  # Category description, CKEditor5Field provides rich text editor

    # Additional meta configuration for the model
    class Meta:
        verbose_name_plural = "Categories"  # Set verbose name in plural form
        ordering = ['name']  # Default ordering is alphabetical by category name

    def __str__(self):
        return self.name  # Return category's name when its instance is printed

    # Method to return the url of Category object
    def get_absolute_url(self):
        return reverse('article_app:category_detail', args=[self.slug])  # Using Django's reverse function to build URL


# Tag Model
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)  # Name field, must be unique
    slug = models.SlugField(max_length=50, unique=True)  # Slug field, used in urls, must be unique

    # Additional meta configuration for the model
    class Meta:
        ordering = ['name']  # Default ordering is alphabetical by tag name

    def __str__(self):
        return self.name  # Return tag's name when its instance is printed

    # Method to return the url of Tag object
    def get_absolute_url(self):
        return reverse('article_app:tag_detail', args=[self.slug])  # Using Django's reverse function to build URL


# Article Model
class Article(models.Model):
    # Defining various fields related to the Article
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique_for_date='publish_date')  # unique for each publish date
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='articles')  # Each user can have multiple articles
    content = CKEditor5Field()
    publish_date = models.DateTimeField(default=timezone.now)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=(('draft', 'Draft'), ('published', 'Published')), default='draft')

    # Relationships
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True,
                                 related_name='articles')  # Each category can have multiple articles, if a category is deleted, article's category is set to null
    tags = models.ManyToManyField(Tag, blank=True, related_name='articles')  # Article can have multiple tags,
    featured_image = models.ImageField(upload_to='article_images/', blank=True, null=True)
    summary = CKEditor5Field(max_length=500, blank=True)
    views_count = models.PositiveIntegerField(default=0)

    # Additional meta configuration for the model
    class Meta:
        ordering = ['-publish_date']  # Default ordering is by publish_date in descending order
        indexes = [models.Index(
            fields=['-publish_date']), ]  # Indexing to improve performance of queries involving publish_date

    def __str__(self):
        return self.title  # Return article's title when its instance is printed

    # Method to return the url of Article object
    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.slug])

    # Method to increment views_count of the article
    def increment_views(self):
        self.views_count += 1  # Increment the views_count
        self.save()  # Save the changes to the database
