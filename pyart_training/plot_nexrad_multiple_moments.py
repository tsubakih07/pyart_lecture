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

# filename = 'data/RODN20180710_010241_V06'
filename = 'data/RCWF/20210912_0548_RCWF_VOL.654'
radar = pyart.io.read_nexrad_archive(filename)
display = pyart.graph.RadarDisplay(radar)
# display = pyart.graph.RadarMapDisplay(radar)
fig = plt.figure(figsize=(15, 9))

map_proj = ccrs.PlateCarree()

ax = fig.add_subplot(231)
display.plot('reflectivity', 0, ax=ax,
             title='Radar Reflectivity', colorbar_label='',
             axislabels=('East West distance from radar (km)', ''))
            #  projection=map_proj)
display.set_limits((-300, 300), (-300, 300), ax=ax)


ax = fig.add_subplot(232)
display.plot('differential_reflectivity', 0, ax=ax,
             title='Differential Reflectivity', colorbar_label='',
             axislabels=('', ''))
            #  projection=map_proj)
display.set_limits((-300, 300), (-300, 300), ax=ax)

ax = fig.add_subplot(233)
display.plot('differential_phase', 0, ax=ax,
             title='Differential Phase', colorbar_label='')
display.set_limits((-300, 300), (-300, 300), ax=ax)

ax = fig.add_subplot(234)
display.plot('cross_correlation_ratio', 0, ax=ax,
             title='Correlation Coefficient', colorbar_label='',
             axislabels=('East West distance from radar (km)', ''))
            #  projection=map_proj)
display.set_limits((-300, 300), (-300, 300), ax=ax)

ax = fig.add_subplot(235)
display.plot('velocity', 1, ax=ax, title='Doppler Velocity',
             colorbar_label='',
             axislabels=('', 'North South distance from radar (km)'))
            #  projection=map_proj)
display.set_limits((-300, 300), (-300, 300), ax=ax)

ax = fig.add_subplot(236)
display.plot('spectrum_width', 0, ax=ax,
             title='Spectrum Width', colorbar_label='',
             axislabels=('East West distance from radar (km)', ''))
            #  projection=map_proj)
display.set_limits((-300, 300), (-300, 300), ax=ax)

# adjust space between plots
plt.subplots_adjust(wspace=0.3, hspace=0.5)

plt.savefig("img/plot_all.png")