"""
====================================================
Create a plot of multiple moments from a NEXRAD file
====================================================

An example which creates a plot containing multiple moments taken from a
NEXRAD Archive file.

"""
print(__doc__)

# Author: Jonathan J. Helmus (jhelmus@anl.gov)
# License: BSD 3 clause

import matplotlib.pyplot as plt
import pyart
import cartopy.crs as ccrs

# read raw data
# filename = 'data/RODN20180710_010241_V06'
filename = 'data/RCWF/20210912_0548_RCWF_VOL.654'
radar = pyart.io.read_nexrad_archive(filename)

display = pyart.graph.RadarDisplay(radar)
# display = pyart.graph.RadarMapDisplay(radar)

# set sweep no. to plot (0~17 for RCWF)
sweep = 0

# set range to plot
rmax = 150

# start plotting
fig = plt.figure(figsize=(15, 9))

ax = fig.add_subplot(231)
display.plot('reflectivity',sweep, ax=ax,vmin=0., vmax=60.,
             title='Radar Reflectivity', colorbar_label='dBZ',
             axislabels=('Distance from radar (km)', ''))
            #  projection=map_proj)
display.set_limits((-rmax, rmax), (-rmax, rmax), ax=ax)

ax = fig.add_subplot(232)
display.plot('differential_reflectivity',sweep, ax=ax,
             title='Differential Reflectivity', colorbar_label='dB',
             axislabels=('Distance from radar (km)', ''))
            #  projection=map_proj)
display.set_limits((-rmax, rmax), (-rmax, rmax), ax=ax)

ax = fig.add_subplot(233)
display.plot('differential_phase',sweep, ax=ax,
             title='Differential Phase', colorbar_label='deg',
             axislabels=('Distance from radar (km)', ''))
display.set_limits((-rmax, rmax), (-rmax, rmax), ax=ax)

ax = fig.add_subplot(234)
display.plot('cross_correlation_ratio',sweep, ax=ax,
             title='Correlation Coefficient', colorbar_label='',
             axislabels=('Distance from radar (km)', ''))
            #  projection=map_proj)
display.set_limits((-rmax, rmax), (-rmax, rmax), ax=ax)

ax = fig.add_subplot(235)
display.plot('velocity', 1, ax=ax, title='Doppler Velocity',
             colorbar_label='m/s',vmin=-50., vmax=50.,cmap='jet',
             axislabels=('', 'North South distance from radar (km)'))
            #  projection=map_proj)
display.set_limits((-rmax, rmax), (-rmax, rmax), ax=ax)

ax = fig.add_subplot(236)
display.plot('spectrum_width',sweep, ax=ax,vmin=0., vmax=20.,
             title='Spectrum Width', colorbar_label='m/s',cmap='cool',
             axislabels=('Distance from radar (km)', ''))
            #  projection=map_proj)
display.set_limits((-rmax, rmax), (-rmax, rmax), ax=ax)

# adjust space between plots
plt.subplots_adjust(wspace=0.3, hspace=0.5)

plt.savefig("img/plot_all-"+sweep+".png")