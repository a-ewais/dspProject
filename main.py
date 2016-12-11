import numpy as np
import matplotlib.pyplot as plt
import time
from scipy.io import wavfile
import scipy.io as sc
import os
import matplotlib.pyplot as plt

def detect_spike(search_res):
    for res in search_res:
        print(res)
        plt.plot(np.arange(len(res))/44100,res)
        plt.show()

def conv(samples, songs):
    search_res = []
    for i in range(len(songs)):
        search_res.append(np.fft.ifft(np.multiply(samples[i],songs[i])))
    return search_res


def getSamples(sample_dir, songs_data):
    sample_for_song = []
    fs, data = sc.wavfile.read(sample_dir)
    plt.plot(np.arange(len(data)) / 44100, data)
    plt.show()
    for song in songs_data:
        data_pad = np.pad(data,(0,len(song)-len(data)),"constant",constant_values=(0))
        print(len(data_pad))
        print(len(song))
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
            print(songs_dictionary[-1])
            freq_domain = np.fft.fft(data)
            songs_data.append(freq_domain)
    return songs_dictionary, songs_data

a,b = getSignal('/home/ewais/PycharmProjects/dspProject')
c = getSamples('/home/ewais/PycharmProjects/dspProject/sample1.wav', b)

detect_spike(conv(c,b))

'''songsDir = '/home/ewais/PycharmProjects/dspProject'
songs_dictionary = []
songs= []
for file in os.listdir(songsDir):
    if file.endswith(".wav") and 'sample' not in file:
        song_dir = os.path.join(songsDir,file)
        fs, data = sc.wavfile.read(song_dir)
        songs_dictionary.append(os.path.basename(song_dir))
        print(songs_dictionary[-1])
        freq_domain = np.fft.fft(data)
        songs.append(freq_domain)
samples = []
fs, data = sc.wavfile.read('/home/ewais/PycharmProjects/dspProject/sample.wav')
for song in songs:
    samples.append(np.conjugate(np.fft.fft(data,n=len(song))))
search_res = []
for i in range(len(songs)):
    print(samples[i])
    print(songs[i])
    search_res.append(np.absolute((np.fft.ifft(np.multiply(samples[i],songs[i])))))
for res in search_res:
    print(len(res))
    print(res)
    plt.plot(np.arange(len(res)) / 44100, res)
    plt.show()'''
