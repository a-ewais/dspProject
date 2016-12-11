import numpy as np
import matplotlib.pyplot as plt
import time
from scipy.io import wavfile
import scipy.io as sc
import os
import matplotlib.pyplot as plt

def detect_spike(search_res):
    for res in search_res:
        print(len(res))
        print(res)
        plt.plot(np.arange(len(res))/44100,res)
        plt.show()

def conv(samples, songs):
    search_res = []
    for i in range(len(songs)):
        print(len(samples[i]))
        print(len(songs[i]))
        search_res.append(np.fft.ifft(np.multiply(samples[i],songs[i])))
    return search_res


def getSamples(sample_dir, songs_data):
    sample_for_song = []
    fs, data = sc.wavfile.read(sample_dir)
    for song in songs_data:
        sample_for_song.append(np.conjugate(np.fft.fft(data,n=len(song))))
    return sample_for_song

def getSignal(songsDir):
    songs_dictionary = []
    songs_data = []
    for file in os.listdir(songsDir):
        if file.endswith(".wav") and 'sample' not in file:
            song_dir = os.path.join(songsDir,file)
            fs, data = sc.wavfile.read(song_dir)
            songs_dictionary.append(os.path.basename(song_dir))
            print(songs_dictionary[-1])
            freq_domain = np.fft.fft(data)
            songs_data.append(freq_domain)

    ##data = np.asarray(np.fft.ifft(freq_domain),np.int32)
    ##sc.wavfile.write(os.path.join(songsDir,'out.wav'),fs,data)
    return songs_dictionary, songs_data

a,b = getSignal('/home/ewais/PycharmProjects/dspProject')

c = getSamples('/home/ewais/PycharmProjects/dspProject/sample.wav', b)

detect_spike(conv(c,b))
