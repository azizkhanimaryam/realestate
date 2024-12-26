"""
URL configuration for realestate project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from property import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),  # Add this line for the homepage
    path('property/', include('property.urls')),
    path('properties/', views.properties, name='properties'),  # For properties page
    path('schedule-visit/', views.schedule_visit, name='schedule_visit'),
    path('property-details/<str:property_type>/<int:property_id>/', views.property_details,name='property_details'),
    path('contact/', views.contact_view, name='contact')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


