# File: home/admin.py

from django.contrib import admin
from .models import TeamMember, MissionContent

class TeamMemberAdmin(admin.ModelAdmin):
    """
    Admin configuration for the TeamMember model.
    """
    list_display = ('first_name', 'last_name', 'role')  # Fields to display in the list view
    search_fields = ('first_name', 'last_name', 'role')  # Enable search by first name, last name, and role

# Register TeamMember model with its custom admin configuration
admin.site.register(TeamMember, TeamMemberAdmin)

# Register MissionContent model without any custom admin configuration
admin.site.register(MissionContent)
