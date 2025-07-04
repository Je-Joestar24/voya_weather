
from django.urls import path
from . import views

urlpatterns = [
    # VIEWS
    path('', views.home_view, name='home_view'),
    path('about/', views.about_view, name='about_view'),
    path('login/', views.login_view, name='login_view'),
    path('signup/', views.signup_view, name='signup_view'),
    path('dashboard/', views.dashboard_view, name='dashboard_view'),
    path('recents/', views.recents_view, name='recents_view'),
    path('saved/places/', views.saved_places_view, name='saved_places_view'),
    path('search/places/', views.search_places_view, name='search_places_view'),
]
