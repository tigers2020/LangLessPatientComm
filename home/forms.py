# File: home/forms.py

from django import forms
from django.urls import get_resolver, URLPattern, URLResolver
from .models import MenuItem

class MenuItemForm(forms.ModelForm):
    """
    Custom form for the MenuItem model.
    Dynamically populates the 'path' field with available URL patterns.
    """
    class Meta:
        model = MenuItem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        """
        Initialize the form and dynamically set the choices for the 'path' field.
        """
        super().__init__(*args, **kwargs)
        url_names = self.get_url_names()
        self.fields['path'].widget = forms.Select(choices=[(url, url) for url in url_names])

    def get_url_names(self):
        """
        Retrieve all URL names from the URL resolver.

        Returns:
            list: A list of all URL names in the project.
        """
        resolver = get_resolver()
        return self._get_url_names(resolver.url_patterns)

    def _get_url_names(self, patterns, prefix=''):
        """
        Recursively retrieve URL names from a list of URL patterns.

        Args:
            patterns (list): List of URL patterns to inspect.
            prefix (str): Prefix to prepend to URL names.

        Returns:
            list: A list of URL names.
        """
        url_names = []
        for pattern in patterns:
            if isinstance(pattern, URLPattern) and pattern.name:
                # Add URL name with prefix
                url_names.append(prefix + pattern.name)
            elif isinstance(pattern, URLResolver):
                # Recursively process URL resolvers
                url_names.extend(self._get_url_names(pattern.url_patterns, prefix + pattern.pattern.regex.pattern))
        return url_names
