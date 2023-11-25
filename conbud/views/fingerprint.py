from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..services.fingerprint import Fingerprint

from rest_framework.parsers import JSONParser

fingerprint_service = Fingerprint()

@csrf_exempt
def audio_fingerprint(request):
  """
  Create a new fingerprint.
  """

  if request.method == 'POST':
    file = request.FILES.get('audio')

    if file is None:
      return HttpResponse(status=400)
    try:
      song = fingerprint_service(file)
    except Exception as e:
      return HttpResponse(status=400, content='{"error": "%s"}' % e)

    return JsonResponse(song, status=201,)
  
  # not supported
  return HttpResponse(status=404)