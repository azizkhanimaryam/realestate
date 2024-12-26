from django.urls import path
from . import views
from .views import index


app_name = 'property'

urlpatterns = [
    path('', views.index, name="home"),
    path('properties/', views.properties, name='properties'),
    path('schedule-visit/', views.schedule_visit, name='schedule_visit'),
    path('contact/', views.contact_view, name='contact'),
    # other URLs
]

