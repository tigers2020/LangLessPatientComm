# admin.py
from django.contrib import admin

from .models import TeamMember, MissionContent


class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'role')
    search_fields = ('name', 'surname', 'role')


admin.site.register(TeamMember)

admin.site.register(MissionContent)
