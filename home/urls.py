from django.urls import path, include

from home import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('emergency-contact/', views.EmergencyGuidelineView.as_view(), name='emergency-contact'),
    path('prescription/', views.PrescriptionRefillView.as_view(), name='prescription'),
    path('scanner/', views.Scanner.as_view(), name='scanner'),
    path('about-us/', views.AboutUsView.as_view(), name='about_us'),
    path('mission/', views.MissionView.as_view(), name='mission'),
]
