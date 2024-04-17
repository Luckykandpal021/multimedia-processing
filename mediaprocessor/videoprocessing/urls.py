from django.urls import path
from .views import *

urlpatterns = [
    path('books/',view=Book_Title,name='books'),
    path('extract-audio/', view=video_extract_audio, name='extract-audio'),
]
