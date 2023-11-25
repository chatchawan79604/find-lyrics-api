import django.core.files.uploadedfile
import os
def is_valid_audio_file(audio_path):
  ret = os.system(f'ffmpeg -v 0 -i {audio_path} -f null - 2>error.log')
  return ret == 0


def check_audio_file_service(audio_file: django.core.files.uploadedfile.InMemoryUploadedFile):
  file_extention = audio_file.name.rsplit('.', maxsplit=1)[1]

  audio_path = 'requestdata/audio/audio-{}.{}'.format(hash(audio_file), file_extention)
  
  with open(audio_path, 'wb+') as destination:
    for chunk in audio_file.chunks():
      destination.write(chunk)
  
  # check if the file is not corrupted
  is_valid = is_valid_audio_file(audio_path)

  # remove the file
  os.remove(audio_path)

  return {
    'data': {
      'is_valid': is_valid
    }
  }