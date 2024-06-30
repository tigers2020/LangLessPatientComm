from django import forms
from django.urls import get_resolver, URLPattern, URLResolver
from .models import MenuItem

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        url_names = self.get_url_names()
        self.fields['path'].widget = forms.Select(choices=[(url, url) for url in url_names])

    def get_url_names(self):
        resolver = get_resolver()
        return self._get_url_names(resolver.url_patterns)

    def _get_url_names(self, patterns, prefix=''):
        url_names = []
        for pattern in patterns:
            if isinstance(pattern, URLPattern) and pattern.name:
                url_names.append(prefix + pattern.name)
            elif isinstance(pattern, URLResolver):
                url_names.extend(self._get_url_names(pattern.url_patterns, prefix + pattern.pattern.regex.pattern))
        return url_names
