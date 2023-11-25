import librosa
import django.core.files.uploadedfile
import os
import numpy as np
import sklearn.neighbors

def convert_to_wav(filename, start_at_sec=0):
  basename = filename.rsplit('.')[0]
  new_filename = f'{basename}.wav'
  if os.system(f'ffmpeg -v 0 -ss {start_at_sec} -i {filename}  -ac 1 -ar 16000 -y {new_filename}') != 0:
    raise Exception('Error converting to wav')
  return new_filename

class BaseFingerprint:
  def __init__(self) -> None:
    pass

  def __call__(self, audio_file: django.core.files.uploadedfile.InMemoryUploadedFile):
    raise NotImplementedError
  
  def get_song_from_path(self, audio_path):
    raise NotImplementedError

class Fingerprint(BaseFingerprint):
  def __init__(self,):
    super().__init__()
    self.fingerprints = np.load('conbud/services/db/fps.npy')
    self.fp_n = self.fingerprints.shape[0]
    self.song_names = np.load('conbud/services/db/songs.npy')
    self.model = self.build_model()

    self.current_song_id = 0

  def build_model(self):
     return sklearn.neighbors.NearestNeighbors(
       n_neighbors=5, algorithm='auto',)\
          .fit(self.fingerprints.reshape(self.fp_n, -1, order='F'))
  
  def preprocess(self, audio_path):
    x, sr = librosa.load(audio_path, sr=8000, mono=True, duration=4)
    chroma_x = librosa.feature.chroma_stft(y=x, sr=sr, hop_length=512)
    return chroma_x[:, :, None].reshape(1, -1, order='F')
  
  def find_neighbors(self, fp):
    scores, nbrs = self.model.kneighbors(fp)
    return scores[0].tolist(), self.song_names[nbrs[0]].tolist()

  def __call__(self,
               audio_file: django.core.files.uploadedfile.InMemoryUploadedFile):

    fext = 'webm' if not audio_file.name else audio_file.name.rsplit('.', maxsplit=1)[1]
    audio_path = 'requestdata/audio/audio-{}.{}'.format(self.current_song_id, fext)
    self.current_song_id = (self.current_song_id + 1) % 5

    # save audio file to disk
    with open(audio_path, 'wb+') as destination:
      for chunk in audio_file.chunks():
        destination.write(chunk)

    # convert to wav if needed
    if fext != 'wav':
      audio_path = convert_to_wav(audio_path)

    fp = self.preprocess(audio_path)
    neighbors = self.find_neighbors(fp)

    return {'results': [{'score': score, 'song': song} for score, song in zip(*neighbors)]}