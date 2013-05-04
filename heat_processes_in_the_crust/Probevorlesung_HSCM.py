# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Probevorlesung: Heat Processes in the Crust

# <codecell>

# Einige Einstellungen
from pylab import *
import math
import numpy
import scipy
import scipy.stats
# import sys
# sys.path.append(u'/opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/scipy')
# import interpolate
# figsize(12,8) # increase basic figure size
rc('font', family='serif', size=20) # set basic figure font size
rc('lines', markersize=10)
rc('lines', linewidth=2)

# <headingcell level=3>

# Error Function/ Fehlerfunktion

# <codecell>

x = numpy.arange(0,3,0.001)
y_erf = [math.erf(z) for z in x]
y_erfc = [math.erfc(z) for z in x]
plot(x,y_erf,label='erf')
plot(x,y_erfc,label='erfc')
legend()
grid()

# <headingcell level=3>

# Half-Space Cooling Model

# <codecell>

# Definition der Funktion
def half_space_cooling_temperature(z, t, T1, T0, kappa):
    """Return temperature at position x after time t for given initial temperature T0, temperature pulse T1, and diffusivity kappa"""
    return [math.erfc(z1 / (2 * numpy.sqrt(kappa * t))) * (T0 - T1) + T1 for z1 in z]

# <codecell>

# Definition einiger Modellparameter
my = 1E6 * 365 * 24 * 3600. # s
T0 = 300 # K
T1 = 1600 # K
kappa = 1E-6 # m^2 s^-1

# <codecell>

# Temperaturprofile fuer mehrere Alter
ts = [5*my, 25*my, 45*my, 65*my, 85*my]
z = numpy.arange(0,100000,1000)
for t in ts:
    plot(half_space_cooling_temperature(z,t,T1,T0,kappa),-z/1000.,label="%.0f Ma" % (t/my))
xlim(200,1700)
grid()
xlabel("Temperatur [K]")
ylabel("Tiefe [km]")
legend(loc="lower left")

# <headingcell level=3>

# Zusammenhang zwischen Waermefluss an der Oberflaeche und Alter

# <codecell>

# Definition der Funktion
def half_space_cooling_waermefluss(k, T0, T1, kappa, t):
    """Return expected surface heat flow under assumption of the cooling half-space model"""
    return k * (T1 - T0) / (numpy.sqrt(math.pi * kappa * t))

# <rawcell>

# Literaturdaten laden: Sclater (1976) and Lister (1990)

# <codecell>

sclater = numpy.loadtxt("heat_flow_sclater_1976.csv", skiprows=1, delimiter=",", usecols=(0,1,2))
lister = numpy.loadtxt("heat_flow_pacific_lister_1990.csv", skiprows=1, delimiter=",", usecols=(0,1,2))

# <codecell>

# Plot erstellen
t_range = numpy.arange(3*my, 200*my, my)
k = 3.3 # Basalt: 1.3-2.9, Gabbro: 1.9-4.0, Peridotit: 3-4.5
q_est = [1000*half_space_cooling_waermefluss(k, T0, T1, kappa, t) for t in t_range]
plot(t_range/my, q_est, label="Half-space model")
plot((sclater[:,0]+sclater[:,1])/2.,sclater[:,2],'gs',label="Sclater (1975)")
plot((lister[:,0]+lister[:,1])/2.,lister[:,2],'ro', label="Lister (1990)")
xlabel("Alter [Ma]")
ylabel("Waermefluss [mW/m2]")
title("Waermefluss vs. Alter der ozean. Lithosphaere")
grid()
legend()

# <codecell>


