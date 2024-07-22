# models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Unique category name
    slug = models.SlugField(max_length=100, unique=True)  # URL-friendly identifier
    description = CKEditor5Field(blank=True)  # Rich text description

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']  # Alphabetical ordering

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('article_app:category_detail', args=[self.slug])

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)  # Unique tag name
    slug = models.SlugField(max_length=50, unique=True)  # URL-friendly identifier

    class Meta:
        ordering = ['name']  # Alphabetical ordering

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('article_app:tag_detail', args=[self.slug])

class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique_for_date='publish_date')  # Unique slug per publish date
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    content = CKEditor5Field()
    publish_date = models.DateTimeField(default=timezone.now)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=(('draft', 'Draft'), ('published', 'Published')), default='draft')

    # Relationships
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='articles')
    tags = models.ManyToManyField(Tag, blank=True, related_name='articles')
    featured_image = models.ImageField(upload_to='article_images/', blank=True, null=True)
    summary = CKEditor5Field(max_length=500, blank=True)
    views_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-publish_date']  # Most recent first
        indexes = [models.Index(fields=['-publish_date'])]  # Optimize queries on publish_date

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.slug])

    def increment_views(self):
        self.views_count += 1
        self.save()