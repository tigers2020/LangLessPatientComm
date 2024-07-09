from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.ImageUploadView.as_view(), name='upload_image'),
    path('extract/', views.ExtractTextView.as_view(), name='extract_text'),
    path('text-to-speech/', views.text_to_speech, name='text_to_speech'),

]
