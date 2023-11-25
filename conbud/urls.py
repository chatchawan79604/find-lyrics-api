from django.urls import path

from conbud.views.speech2text import transcript_handler

from .views.fingerprint import audio_fingerprint
from .views.checker import check_audio_file
from .views import song_index

urlpatterns = [
  path('songs/', song_index, name='song_index'),
  path('fp/', audio_fingerprint, name='audio_fingerprint'),
  path('check/audio_file/', check_audio_file, name='audio_fingerprint'),
  path('tr/', transcript_handler, name='transcript_handler')
]