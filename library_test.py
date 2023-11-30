import math

import matplotlib.pyplot as plt
import numpy as np
from pyads1292 import *
import scipy as sci
from scipy.interpolate import interp1d

def get_derivation1_raw(derivation2_raw, derivation3_raw):
    derivation1_raw = derivation2_raw - derivation3_raw
    return derivation1_raw

def filter_signal(signal, filter1, filter2, fs):
    filtered_signal_f1 = sci.signal.sosfilt(filter1, signal)
    filtered_signal_f2 = sci.signal.sosfilt(filter2, filtered_signal_f1)
    return filtered_signal_f2[30*fs:]

caminando_tsv = '../ECG-Dataset/ECG_caminando.tsv'
#Cargado de datos
caminando_unfiltered_ecg_dat = np.loadtxt(caminando_tsv)
#obtencion de derivaciones 2 y 3 para cada condicion
caminando_derivation2_raw = caminando_unfiltered_ecg_dat[:, 1]
caminando_derivation3_raw = caminando_unfiltered_ecg_dat[:, 2]
N0 = len(caminando_derivation2_raw)
fs = 128000

# 1.a) Primera derviacion a partir de la derivacion dos y tres.

caminando_derivation1_raw = get_derivation1_raw(caminando_derivation2_raw, caminando_derivation3_raw)


# Filtro pasa alto
butter_order = 4
butter_bandwidth = 0.1
butter_type = "highpass"
butter_analog = True
butter_output = "ba"
# Filtro elimina banda
butter_EB_order = 4
butter_EB_bandwidth = [48, 52]
butter_EB_type = "bandstop"
butter_EB_analog = True
butter_EB_output = "ba"
highpass_filter = sci.signal.butter(butter_order, butter_bandwidth, butter_type, False, "sos", fs)
bandstop_filter = sci.signal.butter(butter_EB_order, butter_EB_bandwidth, butter_EB_type, False, "sos", fs)
#SENTADO

t_max = len(caminando_derivation1_raw) / 250
caminando_derivation1_raw = sci.signal.resample(caminando_derivation1_raw, int(128000*t_max))

sentado_derivation1_bandstop = filter_signal(caminando_derivation1_raw, highpass_filter, bandstop_filter, fs)

t = np.linspace(0, N0/fs, len(sentado_derivation1_bandstop))
plt.figure()
plt.plot(t,sentado_derivation1_bandstop)
plt.show()

r = int(128000/fs)

caminando_derivation1_fmod = sentado_derivation1_bandstop

# t_max = len(sentado_derivation1_bandstop) / fs
# caminando_derivation1_fmod = sci.signal.resample(sentado_derivation1_bandstop, int(128000*t_max))

# caminando_derivation1_fmod = []
# for i in sentado_derivation1_bandstop:
#     for j in range(r):
#         caminando_derivation1_fmod.append(i)

fs = 128000
caminando_derivation1_fmod_5seg=caminando_derivation1_fmod[0:128000]
t = np.linspace(0, len(caminando_derivation1_fmod_5seg) / 128000, len(caminando_derivation1_fmod_5seg))

plt.figure()
plt.plot(t,caminando_derivation1_fmod_5seg)
plt.show()

pyads1292 = Pyads1292()
pyads1292.fsps = 1000

################### funcion de teste0 ###############

ftest = 60
N = 256000
fs = N
t = np.linspace(0, N/fs, N)
u_sen = 0.9*np.sin(2*np.pi*ftest*t)      #Senal de testeo
u= u_sen
#u = caminando_derivation1_fmod_5seg//3300
#u = caminando_derivation1_fmod_5seg*100

##################### test only pga ##############

signal_pga = pyads1292.pga(u, fs)

t = np.linspace(0, len(u) / fs, len(u))
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
ax1.plot(t, u)
ax1.set_title('10 Hz and 20 Hz sinusoids')
ax1.axis([0, 1, -2, 2])
ax2.plot(t, signal_pga)
ax2.set_title('After 15 Hz high-pass filter')
ax2.axis([0, 1, -2, 2])
ax2.set_xlabel('Time [seconds]')
plt.tight_layout()
plt.show()

##################### test only modulation ##############

plt.figure(figsize=(15, 4))
v, xn, xmax, y = pyads1292.modulacion(u, fs)
t = np.linspace(0, len(v)/pyads1292.fmod, len(v))
#t = np.arange(N)
plt.step(t, u[::math.ceil(len(u)/len(v))],'r')
plt.step(t, v, 'g')
#plt.xlim((0,0.016/2))
#plt.xlim((0,0.016/2))
plt.xlabel('Sample Number')
plt.ylabel('u, v')
plt.title('Modulator Input & Output')
plt.show()

######## test ADC #########

ydem = pyads1292.adc(u, fs)
fsps = 800
Ndem = max(ydem.shape)
print(Ndem)
t = np.linspace(0, Ndem/fsps, Ndem)
plt.subplot(211)
plt.step(t, ydem)
plt.plot(t, u[::math.ceil(len(u)/len(ydem))])
plt.ylabel('$w$')
#plt.xlim((0,0.02))
plt.subplot(212)
plt.plot(t, u[::math.ceil(len(u)/len(ydem))] - ydem, 'g')
plt.ylabel('$u-w$')
plt.xlabel('t [s]')
#plt.xlim((0,0.02))
plt.suptitle('Output and conversion error')
plt.show()

print(ydem[123])
print(np.min(ydem))
print(np.min(ydem)*32768)

########## OSR ###############
pyads1292.fsps = 8000
pyads1292.gain = 1

ENOB = pyads1292.osr(u, 60, fs)
print(ENOB)