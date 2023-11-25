from django.http import HttpResponse, JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import JSONParser
from conbud.services.findlyric import find_song_by_lyric_service

from conbud.services.speech2text import transcript_service


@csrf_exempt
def transcript_handler(request: HttpRequest):
    if request.method == 'POST':
        if not request.session.session_key:
            request.session.create()

        file = request.FILES.get('audio')
        start_at = request.POST.get('start_at')
        timestamp = request.POST.get('timestamp')

        if not file:
            return JsonResponse(status=400, data={"error": "audio file is required"})
        try:
            song_lyric = transcript_service(file, start_at, timestamp)
            lyric_lines = request.session.get('lyric_lines', []) + [song_lyric['data']]
            songs = find_song_by_lyric_service(lyric_lines)

            request.session['lyric_lines'] = lyric_lines[:5]
        except Exception as e:
            return JsonResponse(status=400, data={"error": "%s" % e})

        return JsonResponse(dict(
            data=songs
        ), status=201,)

    # not supported
    return HttpResponse(status=404)
