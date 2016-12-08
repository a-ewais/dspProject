import numpy as np
import matplotlib.pyplot as plt
import time


def signalToTest(x):
    # has two freq components at 10.7Hz and 50.5Hz
    return 0.5*np.sin(2*np.pi*10.7*x)+ np.sin(2*np.pi*50.5*x)


def rect(x,N):
    return 1


def hamming(x,N):
    return 0.54 - 0.46 * np.cos(2*np.pi*x/N)


def hanning(x,N):
    return 0.5 - 0.5 * np.cos(2 * np.pi * x / N)


def withWindow(x,func):
    N = len(x)
    return x*func(np.arange(N),N)

def DFT(y):
    samplesNum = len(y)
    W = np.fromfunction(lambda m, n: np.exp(-2j * np.pi * n * m / samplesNum), (samplesNum,samplesNum),dtype=int)
    X = W.dot(y)
    return X


def FFT(a):
    size = len(a)
    if size==1:
        return a
    yEven = FFT(a[::2])
    yOdd = FFT(a[1::2])
    wk= np.exp(-2j*np.pi*np.arange(size//2)/size)
    return np.concatenate([yEven + wk*yOdd, yEven - wk * yOdd])

def draw(fs,samplesNum,mag, log):
    frequencies = np.array([fs * m / samplesNum for m in range(samplesNum)])
    plt.xlim([-5,frequencies[-1]+10])
    plt.xlabel("Frequencies (Hz)")
    plt.ylabel("magnitude")
    if log:
        plt.plot(frequencies,20*np.log(mag))
    else:
        plt.plot(frequencies, mag)
    plt.title("frequency components")
    plt.show()

def DFTandFFT(fs,samplesNum, window=hanning, log=False, FFTonly=False):

    points = withWindow(signalToTest(np.arange(samplesNum) / fs), window)
    start = time.clock()
    mag = np.absolute(FFT(points))
    end = time.clock()
    print("FFT time:", (end - start))
    draw(fs, samplesNum, mag, log)
    timeFFT = end - start
    if FFTonly:
        return timeFFT
    start = time.clock()
    mag = np.absolute(DFT(points))
    end = time.clock()
    print("DFT time:", (end - start))
    draw(fs, samplesNum, mag, log)
    timeDFT = end -start
    return timeDFT,timeFFT


## plot the signal int he time domain
plt.axis([0,1,-1.5,1.5])
plt.plot(np.arange(1024)/1024,signalToTest(np.arange(1024) / 1024),'r-')
plt.show()


## to show the effect of the window we use log scale and try it once with
plt.ylim([-100,100])
DFTandFFT(128,128,window=rect, log=True,FFTonly=True)
plt.ylim([-100,100])
DFTandFFT(128,128,window=hamming, log=True,FFTonly=True)
plt.ylim([-100,100])
DFTandFFT(128,128,window=hanning, log=True,FFTonly=True)


## computing the FFT and DFT for 128, 512, 2048 and 8192 points and comparing the times
timeFFT=[]
timeDFT=[]
s=DFTandFFT(128,128)
timeDFT.append(s[0])
timeFFT.append(s[1])
s=DFTandFFT(512,512)
timeDFT.append(s[0])
timeFFT.append(s[1])
s=DFTandFFT(2048,2048)
timeDFT.append(s[0])
timeFFT.append(s[1])
s=DFTandFFT(8192,8192)
timeDFT.append(s[0])
timeFFT.append(s[1])

## plotting the processing times for DFT and FFT

t = [128,512,2048,8192]
plt.plot(t,np.log(timeDFT),'r-',t,np.log(timeFFT),'b-')
plt.show()