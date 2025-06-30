
from django.urls import path
from . import views

urlpatterns = [
    # VIEWS
    path('', views.home_view, name='home_view'),
    path('about/', views.about_view, name='about_view')
]
