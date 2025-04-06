from django.urls import path
from .views import *

urlpatterns = [
    # path('music/', get_music_data, name='music-data'),
    path('', home, name='home'),
    path('contact/', contact, name='contact'),
]