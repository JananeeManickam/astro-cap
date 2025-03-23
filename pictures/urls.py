from django.urls import path
from rest_framework.routers import DefaultRouter
from pictures.views.asteroids import asteroid_list
from pictures.views.constellations import constellations_view
from pictures.views.home import PicturesHome
from pictures.views.planets import PlanetListView, get_planet_photo
from pictures.views.stellarium import StellariumSkyView
from pictures.views.telescopes import TelescopeListView, get_telescope_view

router = DefaultRouter()

urlpatterns = [
    # 🏠 Home Page
    path('', PicturesHome.as_view(), name='pictures_home'),

    # 🌃 Stellarium WebApp
    path('stellarium/', StellariumSkyView.as_view(), name='stellarium_sky'),
    
    # 🌍 Planets Module
    path('planets/', PlanetListView.as_view(), name='planets_list'),
    path('planets/<str:planet_name>/', get_planet_photo, name='get_planet_photo'),

    # 🔭 Telescopes Module (UPDATED for `/pictures/telescopes/` route)
    path('telescopes/', TelescopeListView.as_view(), name='telescopes_list'),
    path('telescopes/<str:telescope_name>/', get_telescope_view, name='get_telescope_view'),
    
    # 🗿 Asteroids
    path('asteroids/', asteroid_list, name='asteroid_list'),
    
    # ✨ Constellations
    path('constellations/', constellations_view, name='constellations'),
]
