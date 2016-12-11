import numpy as np
from scipy.io import wavfile
import scipy.io as sc
import os

def detect_spike(search_res,song_dictionary):
    mx = -99999999999
    song_number = -1
    for i in range(len(search_res)):
        index_of_max = np.argmax(search_res[i])
        if search_res[i][index_of_max] > mx:
            mx=search_res[i][index_of_max]
            song_number = i
    return song_dictionary[song_number]


def conv(samples, songs):
    search_res = []
    for i in range(len(songs)):
        search_res.append(np.fft.ifft(np.multiply(samples[i],songs[i])))
    return search_res


def getSamples(sample_dir, songs_data):
    sample_for_song = []
    fs, data = sc.wavfile.read(sample_dir)
    for song in songs_data:
        data_pad = np.pad(data,(0,len(song)-len(data)),"constant",constant_values=(0))
        sample_for_song.append(np.conjugate(np.fft.fft(data_pad)))
    return sample_for_song

def getSignal(songsDir):
    songs_dictionary = []
    songs_data = []
    for file in os.listdir(songsDir):
        if file.endswith(".wav") and 'sample' not in file:
            song_dir = os.path.join(songsDir,file)
            fs, data = sc.wavfile.read(song_dir)
            songs_dictionary.append(os.path.basename(song_dir))
            freq_domain = np.fft.fft(data)
            songs_data.append(freq_domain)
    return songs_dictionary, songs_data

a,b = getSignal('/home/ewais/PycharmProjects/dspProject')
c = getSamples('/home/ewais/PycharmProjects/dspProject/sample1.wav', b)
print(detect_spike(conv(c,b),a))
