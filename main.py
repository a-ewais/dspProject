import numpy as np
import matplotlib.pyplot as plt
import time
import scipy.io as sc
class block:
    def __init__(self, songName, blockNum, FFT):
        self.id = songName
        self.index= blockNum
        self.points = FFT

def hanning(x,N):
    return 0.5 - 0.5 * np.cos(2 * np.pi * x / N)


def withWindow(x,func):
    N = len(x)
    return x*func(np.arange(N),N)


def FFT(a):
    size = len(a)
    if size==1:
        return a
    yEven = FFT(a[::2])
    yOdd = FFT(a[1::2])
    wk= np.exp(-2j*np.pi*np.arange(size//2)/size)
    return np.concatenate([yEven + wk*yOdd, yEven - wk * yOdd])

def getSignal(songDir):
    fs, data = sc.wavfile.read(songDir)
    t = songDir.split('\')
