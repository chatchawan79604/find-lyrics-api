from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import JSONParser

from ..serializers import SongSerializer
from ..models import Song

@csrf_exempt
def song_index(request):
  """
  List all songs, or create a new song.
  """

  if request.method == 'GET':
    songs = Song.objects.all()
    serializer = SongSerializer(songs, many=True)
    return JsonResponse(serializer.data, safe=False)
  
  elif request.method == 'POST':
    data = JSONParser().parse(request)
    serializer = SongSerializer(data=data)
    if serializer.is_valid():
      serializer.save()
      return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)
  
  # not supported
  return HttpResponse(status=404)


