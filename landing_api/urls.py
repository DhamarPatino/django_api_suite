from django.urls import path
from . import views

urlpatterns = [
    path('landing/api/', views.LandingAPI.as_view(), name='landing_api'),
    path("index/", views.LandingAPI.as_view(), name="landing_api_index")
]