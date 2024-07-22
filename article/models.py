from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field

class Category(models.Model):
    """
    Model representing a category for articles.
    """
    name = models.CharField(max_length=100, unique=True)  # Name of the category, must be unique
    slug = models.SlugField(max_length=100, unique=True)  # URL-friendly identifier for the category
    description = CKEditor5Field(blank=True)  # Rich text description using CKEditor5

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']  # Order categories alphabetically by name

    def __str__(self):
        """
        String representation of the Category model.
        """
        return self.name

    def get_absolute_url(self):
        """
        Returns the URL to access a particular category instance.
        """
        return reverse('article_app:category_detail', args=[self.slug])

class Tag(models.Model):
    """
    Model representing a tag for articles.
    """
    name = models.CharField(max_length=50, unique=True)  # Name of the tag, must be unique
    slug = models.SlugField(max_length=50, unique=True)  # URL-friendly identifier for the tag

    class Meta:
        ordering = ['name']  # Order tags alphabetically by name

    def __str__(self):
        """
        String representation of the Tag model.
        """
        return self.name

    def get_absolute_url(self):
        """
        Returns the URL to access a particular tag instance.
        """
        return reverse('article_app:tag_detail', args=[self.slug])

class Article(models.Model):
    """
    Model representing an article.
    """
    title = models.CharField(max_length=200)  # Title of the article
    slug = models.SlugField(max_length=200, unique_for_date='publish_date')  # URL-friendly identifier, unique for each publish date
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')  # Author of the article
    content = CKEditor5Field()  # Rich text content using CKEditor5
    publish_date = models.DateTimeField(default=timezone.now)  # Date and time when the article is published
    created_date = models.DateTimeField(auto_now_add=True)  # Date and time when the article is created
    updated_date = models.DateTimeField(auto_now=True)  # Date and time when the article is last updated
    status = models.CharField(max_length=10, choices=(('draft', 'Draft'), ('published', 'Published')), default='draft')  # Status of the article

    # Relationships
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='articles')  # Category of the article
    tags = models.ManyToManyField(Tag, blank=True, related_name='articles')  # Tags associated with the article
    featured_image = models.ImageField(upload_to='article_images/', blank=True, null=True)  # Optional featured image for the article
    summary = CKEditor5Field(max_length=500, blank=True)  # Optional summary of the article
    views_count = models.PositiveIntegerField(default=0)  # View count of the article

    class Meta:
        ordering = ['-publish_date']  # Order articles by most recent publish date first
        indexes = [models.Index(fields=['-publish_date'])]  # Add index on publish date for performance

    def __str__(self):
        """
        String representation of the Article model.
        """
        return self.title

    def get_absolute_url(self):
        """
        Returns the URL to access a particular article instance.
        """
        return reverse('article:article_detail', args=[self.slug])

    def increment_views(self):
        """
        Increment the view count for the article.
        """
        self.views_count += 1
        self.save()
