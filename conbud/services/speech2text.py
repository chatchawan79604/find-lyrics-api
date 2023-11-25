import requests
import django.core.files.uploadedfile
import os
import faker

from conbud.services.fingerprint import convert_to_wav

lyric_idx = 0
lyric_dummies = [
    "He is",
    "This is",
    "Yes, your ex-friend's sister",
    "Yes, my ex-friend's sister met someone at a club and he kissed her",
    "Your ex-friend's sister, met someone at a club and he kissed her turns out it was that guy you hooked up",
    "Bet someone at a club and he kissed her Turns out it was that guy who hooked up with ages ago, some wanna be",
    "It turns out it was that guy you hooked up with ages ago, some wanna be z-lister And all the outfits were",
    "With ages ago someone a busy-lister and all the outfits were terrible two thousand",
    "C-lister and all the outfits were terrible 2003 unbearable, did you see?",
    "Three unbearable, did you see the photos? No, I didn't but thanks, though. I'm so in love",
    "I see the photos, no I didn't but thanks, though I'm soin' love that I might stop breathing, true, I'm",
    "I never think so I'm so in love that I might stop breathing drew a map on your bedroom ceiling, oh I",
    "That I might stop breathing through a map on your bedroom ceiling, no I didn't see the news",
    "I'm on your bed from ceiling, no, I didn't see the news, cause we were somewhere else",
    "Yes, didn't see the news, cause we were somewhere else, don't put down pretend alleyways cheap",
    "We were somewhere else, don't put down, pretend alleyways, cheap white, make-believe, it's Champagne",
    "And for down pretend alleyways, cheap wine, make-believe it's champagne I was taken by the few",
    "Why make believe it's champagne? I was taken by the pure like we were in",
    "I was taken by the pure life we were in town",
    "But like we were in town Like we were some",
    "This Like we were somewhere else",
    "Like we were somewhere else Like we were in",
    "Where else? Like we were in Paris",
    "Yes, like we were in Paris, ah",
    ", Paris, I, we were somewhere else",
    "Yes We were somewhere else",
    "' '",
    "This This time I see sound on the door and on my paper",
    "Yes, I'm a legacy song on the door and on my page and on the whole of your mances",
    "Yes I'm not a whole year, your mance is nothing You can keep it just yours",
    "If you keep it just yours Never date above all the messes made sit quiet",
    "Yes, yes, never date above all the messes made Sit quiet by my side in the shade and mouth",
    "Yes I'll miss me Sit quiet by my side in the shade I know the time is time, I mean it's kinda",
    "Yes, my side and the shade And not the kind of town, I mean, I kinda hear a dream of town",
    "I'm not trying this town, I'm not gonna play it like she has done I'm so lucky that I'm not stopping",
    "Yes, I say that a tree has been I'm soin' out that I might stop breathing, but I'm not, stop breathing, but, I'm",
    "Yes, I'm so glad that I might stop breathing Tope about when your bed from ceiling, no I didn't see that",
    "I didn't tell them about when you got from ceiling No, I didn't see the nose, cause we were soft",
    "S S",
    "Yes I know us best We were somewhere else done, but don't pretend alleyways to find make-believe",
    "Ferem stone but don't pretend alleyways to find Make believe it's champagne, I was the dickin'",
    "Longs, Is she'd one make-believe, it's champagne I was taken by the fuel like we were",
    "Champagne, I was taken by the fuel like we were in Paris",
    "By the view like we were in Paris For you like we were in Paris",
    "In Paris Oh, I know like we were somewhere else",
    "Like we were some friends",
    "For someone else Like you were in",
    "Like we were in Parisa",
    "We were in, baby, we were in, we were so",
    "There is a song We were song",
    "Yes We were so many problems fore runs",
    "I want a break once you into love",
    "I wanna bring one to you into loving me forever",
    "I want you into loving me forever, I wanna transport you to someone",
    "This thing me forever, I wanna transport you to somewhere the culture's clever",
    "I'm not gonna transport you to somewhere the culture's clever confess my truth",
    "Where the culture's clever, confess my truth is swooping, soap, cursive letter",
    "This morning, this morning truth is swooping, hoping cursive letters, let the only flush",
    "This This swooping, cursive letters Let the only flashing lights get the tower at midnight",
    "This Let the only flashing lights get the tower at midnight in my mind",
    "The lights get the tower at midnight And my mind We drew a muffin",
    "This night in my mind We drew a mouth on your bedroom ceiling",
]

API_URL = ""
headers = {
    "Authorization": "Bearer " + os.getenv('HF_ACCESS_TOKEN', ''),
    "Content-Type": "audio/flac",
}


def transcript_service(
        audio_file: django.core.files.uploadedfile.InMemoryUploadedFile,
        start_at: int,
        timestamp: str
):
    file_extention = audio_file.name.rsplit('.', maxsplit=1)[1]

    audio_path = 'requestdata/audio/audio-tr-{}.{}'.format(
        hash(audio_file), file_extention)

    with open(audio_path, 'wb+') as destination:
        for chunk in audio_file.chunks():
            destination.write(chunk)

    audio_file = convert_to_wav(audio_path, start_at)

    data = transcript(audio_path)
    data.update({
        "timestamp": timestamp
    })

    # remove the file
    os.remove(audio_path)

    return {
        'data': data
    }


def transcript(filename):
    global lyric_idx
    lyric = lyric_dummies[lyric_idx]
    lyric_idx = (lyric_idx + 1) % len(lyric_dummies)
    return {"text": lyric}
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()
