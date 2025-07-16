
from django.urls import path
from . import views
from core.views.authed.saved import toggle_favorite_place

urlpatterns = [
    # UNAUTHED VIEWS
    path('', views.home_view, name='home_view'),
    path('about/', views.about_view, name='about_view'),
    # AUTHS
    path('login/', views.login_view, name='login_view'),
    path('signup/', views.signup_view, name='signup_view'),
    path('auth/signup/', views.signup_process, name='signup'),
    path('auth/login/', views.login_process, name='login'),
    path('auth/logout/', views.logout_process, name='logout'),
    # AUTHED VIEWS
    path('dashboard/', views.dashboard_view, name='dashboard_view'),
    path('search/places/', views.search_places_view, name='search_places_view'),
    path('favorite/places/', views.favorite_places_view, name='favorite_places_view'),
    path('recents/', views.recents_view, name='recents_view'),
    path('saved/places/', views.saved_places_view, name='saved_places_view'),
    path('profile/', views.profile_view, name='profile_view'),
    # OPERATION VIEWS
    path('weather/saved/favorite/<int:city_id>/', views.toggle_favorite_place, name='toggle_favorite_place'),
    path('weather/remove/saved/<int:city_id>/', views.unsave_place_view, name='remove_saved_place'),
    path('weather/remove/favorite/<int:city_id>/', views.remove_favorite, name='remove_favorite'),
    path('search/places/save/<int:city_id>/', views.toggle_save_place, name='toggle_save_place'),
    path('search/places/view/<int:city_id>/', views.place_details_view, name='place_details'),
]
