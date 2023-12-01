import nltk
import json
import string


def generate_ngrams(s, n, m=None):
    if m is None:
        m = max(1, n-1)
    tokenizer = nltk.tokenize.NLTKWordTokenizer()
    stemmer = nltk.stem.PorterStemmer()

    tokens = map(stemmer.stem, tokenizer.tokenize(s))
    tokens = filter(lambda x: x not in string.punctuation, tokens)

    return nltk.skipgrams(tokens, n, m)

def most_frequent(List):
    dict = {}
    count, itm = 0, ''
    for item in reversed(List):
        dict[item] = dict.get(item, 0) + 1
        if dict[item] >= count :
            count, itm = dict[item], item
    return(itm)

def find_count_list(list1, list2):
    sub_list = []
    for x in list1:
        for y in list2 :
            if x == y :
                sub_list.append(y)
    list1.extend(sub_list)
    return list1
    
def find_one_word_line(words, lines):
    k_word = []
    t_word = []
    for word in words:
        for line in lines:
            if line.find(word) != -1 :
                t_word.append(line)
        t_word = list(set(t_word))
        k_word.extend(t_word)
    return k_word 

def find_first_duo_line(words, lines):
    word_n = words.copy()
    k_word = []
    word = words[0] +' ' + words[1]
    for line in lines:
        if line.find(word) != -1 :
            k_word.append(line)
        k_word = list(set(k_word))
    del word_n[0]
    word_c = word_n.copy()
    del word_c[0]
    if word_c != []:
        k_word.extend(find_first_duo_line(word_n, lines))
    return k_word

def find_line_have_word(words, list_line):
  # word_n = words.copy()
  k_word = []
  # word = words[0] +' ' + words[1]
  for line in list_line :
    ap = line.get('lyrics', {'lines': list()})
    a = 0
    for p in ap.get('lines'):
      u = str(p.get('words').lower())
      if a > 0:
        k_word.append(dict(
            start_time_ms=int(p.get('startTimeMs')),
            words=p.get('words'),
            spotify_uri=line['uri']
                ))
        a += 1
        
      if u.find(words) != -1 and a == 0 :
        # print(p.get('words'))
        k_word.append(dict(
            start_time_ms=int(p.get('startTimeMs')),
            words=p.get('words'),
            spotify_uri=line['uri']
                ))
        a = 1
    if a > 0:
      return k_word
      
  
  
  
# class NGramSongFinderLyricService:
#     def __init__(self) -> None:
#         self.lyric_to_song = {}
#         self.song_to_lyric = {}
#         self._init_lyric_to_song()

#     def _init_lyric_to_song(self,):
#         with open(r'conbud/services/db/track-lyric.json', 'r') as fp:
#             lines = fp.readlines()
#             # track_with_lyric = json.load(fp)
#             # track_with_lyric_list = list(track_with_lyric.values())

#         lyric_with_track_id = []
#         for track in lines:
#             t_lyrics = track.get('lyrics', {'lines': list()})
#             for line in t_lyrics.get('lines')[::-1]:
#                 if len(line.get('words')) < 2:
#                     continue
#                 lyric_with_track_id.append(dict(
#                     start_time_ms=int(line.get('startTimeMs')),
#                     words=line.get('words'),
#                     spotify_uri=track['uri']
#                 ))
        
        
#         word = self._to_ngram('i love you')
#         p1 = find_first_duo_line(word, lines)
#         p2 = find_one_word_line(word, lines)
#         an = find_count_list(p1, p2)
#         an = most_frequent(an)
#         for line in lines:
#             if line.find(an) != -1 :
#                 print('Line Number:', lines.index(line)+1)
#                 sorted_by_score = line

        
#         for l in lyric_with_track_id:
#             for tokens in self._to_ngram(l['words']):
#                 songs = self.lyric_to_song.get(tokens, list())
#                 songs.append(l)
#                 self.lyric_to_song[tokens] = songs
        
#         for line in lyric_with_track_id:
#             if line['spotify_uri'] not in self.song_to_lyric:
#                 self.song_to_lyric[line['spotify_uri']] = list()
#             self.song_to_lyric[line['spotify_uri']].append(line)

#     def _to_ngram(self, words):
#         return generate_ngrams(words, 3, 2)
    
#     def lyric_of_song(self, spotify_uri):
#         if spotify_uri not in self.song_to_lyric:
#             return None
#         return self.song_to_lyric[spotify_uri]

#     def __call__(self, x_lyric, k=5, possible_songs=dict()):
#         # generate ngrams
#         x_tokens = list(self._to_ngram(x_lyric))
#         for i in x_tokens:
#             possible_lines = self.lyric_to_song.get(i, list())
#             # sort by start time
#             possible_lines.sort(key=lambda x: x['start_time_ms'])
#             # for each possible line
#             for s in possible_lines:
#                 # get the song dict
#                 song_dict = possible_songs.get(s['spotify_uri'], dict())
#                 possible_songs[s['spotify_uri']] = song_dict
#                 # get the start time
#                 start_time_ms = s['start_time_ms']

#                 # check if the start time is after the last word
#                 is_after = all([t <= start_time_ms for t in song_dict.keys()])

#                 # if the start time is after the last word, add the score
#                 if is_after:
#                     song_time_score = song_dict.get(start_time_ms, 0)
#                     song_dict[start_time_ms] = song_time_score + \
#                         1 / len(x_tokens)

#         sorted_by_score = sorted(
#             possible_songs.items(),
#             key=lambda x: sum(x[1].values()), reverse=True)
#         return dict(sorted_by_score[:k])


# song_finder_lyric_service = NGramSongFinderLyricService()


def find_song_by_lyric_service(lyric_lines) -> dict:
    # possible_songs = dict()
    # sorted_by_score = None
    # for idx, line in enumerate(lyric_lines):
    #     sorted_by_score = song_finder_lyric_service(
    #         line['text'], possible_songs=possible_songs)
    word = lyric_lines[0]['text'].lower().split(' ')

    with open(r'conbud/services/db/track-lyric.json', 'r') as fp:
        ll = json.load(fp)
        list_line = list(ll.values())
    with open(r'conbud/services/db/track-lyric.json', 'r') as rp:
        lines = rp.readlines().copy()
        lines = [x.lower() for x in lines]

    p1 = find_first_duo_line(word, lines)
    p2 = find_one_word_line(word, lines)
    an = find_count_list(p1, p2)
    an = most_frequent(an).split('"words": "')[1].split('",')[0]

    sorted_by_score = find_line_have_word(an, list_line)

    return sorted_by_score

def current_lyric_line(sent_time, song_uri, lyric_line, lyric_lines):
    """
    sent_time: datetime
    lyric_line: str
    lyric_lines: list[str]
    """
    possible_songs = dict()
    song_finder_lyric_service(lyric_line, possible_songs=possible_songs)
    possible_times = possible_songs.get(song_uri, dict())
    possible_times = sorted(possible_times.items(), key=lambda t: (t[1], t[0]), reverse=True)
