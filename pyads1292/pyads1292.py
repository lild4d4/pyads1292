from __future__ import division
from deltasigma import *

#Pines:

# Numero    | Nombre    | Function              | Description

############# NO IMPLEMENTADOS

# 1 | PGA1N     | Analog Output         | PGA1 inverting output
# 2 | PGA1P     | Analog Output         | PGA1 noninverting output
# 7 | PGA2N     | Analog Output         | PGA2 inverting output
# 8 | PGA2P     | Analog Output         | PGA2 noninverting output

# 12| AVDD      | Supply                | Analog supply
# 13| AVSS      | Supply Analog         | ground
# 15| PWDN/RESET| Digital input         | Power-down or system reset; active low
# 23| DVDD      | Supply Digital        | power supply
# 24| DGND      | Supply Digital        | ground

############# SI IMPLEMENTADOS
# 3 | IN1N      | Analog Input          | Differential analog negative input 1
# 4 | IN1P      | Analog Input          | Differential analog positive input 1
# 5 | IN2N      | Analog Input          | Differential analog negative input 2
# 6 | IN2P      | Analog Input          | Differential analog positive input 2

# 9 | VREFP     | Analog input/output   | Positive reference voltage
# 1 | VREFN     | Analog input Negative | reference voltage; must be connected to AVSS
# 27| VCAP2     | —                     | Analog bypass capacitor
# 14| CLKSEL    | Digital input         | Master clock select
# 16| START     | Digital input         | Start conversion
# 17| CLK       | Digital input         | Master clock input
# 18| CS        | Digital input         | Chip select
# 19| DIN       | Digital input         | SPI data in
# 20| SCLK      | Digital input         | SPI clock
# 21| DOUT      | Digital output        | SPI data out
# 22| DRDY      | Digital output        | Data ready; active low

# 25| GPIO2/RCLK2| Digital input/output | General-purpose I/O 2 or resp clock 2 (ADS1292R)
# 26| GPIO1/RCLK1| Digital input/output | General-purpose I/O 1 or resp clock 1 (ADS1292R)

# 28| RLDINV    | Analog input          | Right leg drive inverting input; connect to AVDD if not used
# 29| RLDIN     | Analog input          | Right leg drive input to MUX or RLD amplifier noninverting input; connect to AVDD if not used
# 30| RLDOUT    | Analog output         | Right leg drive output
# 31| RESP_MODP | Analog output/input   | P-side respiration excitation signal for respiration (analog output) or auxiliary input 3P (analog input)
# 32| RESP_MODN | Analog output/input   | N-side respiratio

# Pines que no son necesarios:
#               - PGA1N
#               - PGA1P
#               - PGA2N
#               - PGA2P

class Pyads1292():
    def __init__(self):
        self.clk = 512000                                       #Frecuencia reloj interno
        self.fmod = 128000                                      #Frecuencia de muestreo de la modulacion sigma delta
        self.fb = 60                                            #frecuencia maxima de la señal de entrada (testeo)
        self.OSR = int(self.fmod / (2 * self.fb))
        self.order = 2
        self.H = synthesizeNTF(self.order, self.OSR, 1)

    def simulateDSM(self, u):
        return simulateDSM(u, self.H)

