from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


class TeamMember(models.Model):
    """
    The TeamMember model contains information about each individual member of the team.

    Attributes:
        first_name (CharField): The first name of the team member.
        last_name (CharField): The last name of the team member.
        role (CharField): The role of the team member.
        description (CKEditor5Field): A rich-text description of the team member.
        image_src (ImageField): The member's photo (can be optional).
    """

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    description = CKEditor5Field()
    image_src = models.ImageField(upload_to='team_images/', blank=True, null=True)

    def __str__(self):
        """Return the full name of the team member."""
        return f"{self.first_name} {self.last_name}"


class MissionContent(models.Model):
    """
    The MissionContent model contains information about each piece of mission content.

    Attributes:
        title (CharField): The title of the mission content.
        subtitle (CharField): The subtitle of the mission content.
        content (CKEditor5Field): A rich-text field containing the mission content.
        image (ImageField): Image related to the mission content (can be optional).
        order (PositiveIntegerField): The order in which the mission content should be displayed.

    Meta:
        ordering (list): A list of fields for the default ordering.
    """

    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True, null=True)
    content = CKEditor5Field()
    image = models.ImageField(upload_to='mission_images/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        """Special attribute of a model class that provides metadata to Django."""
        ordering = ['order']

    def __str__(self):
        """Return the title of the mission content."""
        return self.title
