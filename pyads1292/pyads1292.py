from __future__ import division
from deltasigma import *
import math
import numpy as np
import matplotlib.pyplot as plt
import scipy as sci


class Pyads1292():
    def __init__(self):
        self.clk = 512000
        self.fmod = 128000
        self.fb = 100
        self.OSR = 64
        self.order = 2
        self.H = synthesizeNTF(self.order, self.OSR, 1)
        self.gain = 1
        self.fsps = 500

    def pga(self,u, fs):
        u = u*self.gain
        sos = sci.signal.butter(2, 8400, 'lowpass', fs=fs, output='sos')
        filtered = sci.signal.sosfilt(sos, u)
        return filtered

    def modulacion(self, u, fs):
        u = self.pga(u, fs)
        t_max = len(u)/fs
        if fs>=self.fmod:
            m = math.ceil(fs / self.fmod)
            u_fmod = u[::m]
            print(m)
            print(len(u))
            print(len(u_fmod))
        else:
            u_fmod = sci.signal.resample(u, int(128000 * t_max))

        return simulateDSM(u_fmod, self.H, 4)


    def decimate(self, u, fs):
        v, xn, xmax, y = self.modulacion(u, fs)
        if self.fsps==125:
            DecFact = 1024
        elif self.fsps==250:
            DecFact = 512
        elif self.fsps==500:
            DecFact = 256
        elif self.fsps==1000:
            DecFact = 128
        elif self.fsps==2000:
            DecFact = 64
        elif self.fsps==4000:
            DecFact = 32
        else:
            DecFact = 16
        ydec = sinc_decimate(v, 3, DecFact)
        print(len(ydec))
        return ydec




    def osr(self, u, ftest, fs):
        #v, xn, xmax, y = self.simulateDSM(u, fs)
        v = self.decimate(u, fs)
        N = len(v)

        f = np.linspace(0, 0.5, N // 2 + 1)
        spec = np.fft.fft(v * ds_hann(N)) / (N / 4)
        plt.plot(f, dbv(spec[:N // 2 + 1]), 'b', label='Simulation')

        figureMagic([0, 0.5], 0.05, None, [-160, 0], 20, None, (16, 6), 'Output Spectrum')
        plt.xlabel('Normalized Frequency')
        plt.ylabel('dBFS')
        snr = calculateSNR(spec[2:self.fb + 1], ftest - 2)
        plt.text(0.05, -10, 'SNR = %4.1fdB' % (snr), verticalalignment='center')
        NBW = 1.5 / N
        Sqq = 4 * evalTF(self.H, np.exp(2j * np.pi * f)) ** 2 / 3.
        plt.text(0.49, -90, 'NBW = %4.1E x $f_s$' % NBW, horizontalalignment='right')
        plt.legend(loc=4)
        plt.show()

        ENOB = (snr-1.76)/6.02
        return ENOB

    def adc(self, u, fs):
        v_decimated = self.decimate(u, fs)
        return v_decimated


