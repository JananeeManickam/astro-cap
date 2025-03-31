from django.urls import path
from .views import OnThisDateView, onthisdate_interface

urlpatterns = [
    path('', onthisdate_interface, name='onthisdate-interface'),
    path('events/', OnThisDateView.as_view(), name='astronomical-events'),
]