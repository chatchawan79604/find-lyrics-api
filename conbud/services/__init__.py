import librosa

def load_audio(audio_path):
  """
  Load audio file from path and return it as a numpy array.
  """
  return librosa.load(audio_path, sr=None)