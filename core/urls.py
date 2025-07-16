
from django.urls import path
from . import views
from core.views.authed.dashboard.dashboard import DashboardView
from core.views.authed.profile.profile import ProfileView
from core.views.authed.favorites.favorites import FavoritePlacesView
from core.views.authed.favorites.remove import remove_favorite
from core.views.authed.saved.saved import SavedPlacesView
from core.views.authed.saved.togglefavorite import ToggleFavoritePlaceView
from core.views.authed.saved.unsave import UnsavePlaceView
from core.views.authed.recent.recent import RecentsView
from core.views.authed.details.details import PlaceDetailsView
from core.views.authed.search.search import SearchPlacesView
from core.views.authed.search.togglesave import ToggleSavePlaceView

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
    # AUTHED VIEWS (CBVs)
    path('dashboard/', DashboardView.as_view(), name='dashboard_view'),
    path('search/places/', SearchPlacesView.as_view(), name='search_places_view'),
    path('favorite/places/', FavoritePlacesView.as_view(), name='favorite_places_view'),
    path('recents/', RecentsView.as_view(), name='recents_view'),
    path('saved/places/', SavedPlacesView.as_view(), name='saved_places_view'),
    path('profile/', ProfileView.as_view(), name='profile_view'),
    # OPERATION VIEWS (CBVs for POST actions)
    path('weather/saved/favorite/<int:city_id>/', ToggleFavoritePlaceView.as_view(), name='toggle_favorite_place'),
    path('weather/remove/saved/<int:city_id>/', UnsavePlaceView.as_view(), name='remove_saved_place'),
    path('weather/remove/favorite/<int:city_id>/', views.remove_favorite, name='remove_favorite'),
    path('search/places/save/<int:city_id>/', ToggleSavePlaceView.as_view(), name='toggle_save_place'),
    path('search/places/view/<int:city_id>/', PlaceDetailsView.as_view(), name='place_details'),
]
