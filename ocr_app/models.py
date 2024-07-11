from django.db import models


class ImageUpload(models.Model):
    """
    A Django model representing an image upload.

    Stores an image and the time it was uploaded.
    """
    # An uploaded image file. 'upload_to' tells Django to save uploaded images under 'media/images/'.
    image = models.ImageField(upload_to='images/')

    # The time when the image was uploaded. 'auto_now_add'
    # tells Django to save the current date/time when an image is uploaded.
    uploaded_at = models.DateTimeField(auto_now_add=True)
