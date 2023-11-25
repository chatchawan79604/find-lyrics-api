from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import JSONParser

from conbud.services.checker import check_audio_file_service

@csrf_exempt
def check_audio_file(request):
  if request.method == 'POST':
    file = request.FILES.get('audio')

    if file is None:
      return HttpResponse(status=400)
    try:
      song = check_audio_file_service(file)
    except Exception as e:
      return HttpResponse(status=400, content='{"error": "%s"}' % e)

    return JsonResponse(song, status=201,)
  
  # not supported
  return HttpResponse(status=404)