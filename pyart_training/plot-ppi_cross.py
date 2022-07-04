import pyart
import matplotlib as mpl
import matplotlib.pyplot as plt

radar_name = 'RCWF'
# radar_name = 'RCTP'

# --- file name ---
file = '20210912_0548_RCWF_VOL.654'     # RCWF
# file = 'TIA210912055005.RAW60CY'        # RCTP

#loc is the path where you store your unzipped radar data
#des is the path where you want to store the radar figures you plot
loc='data/'+radar_name+'/'
des='img/CROSS/'

# --- set cross-section ---
#   cross-section originate from radar site
#   angle start from north = 0 deg
# --------------------------------------------
angle = [0,90,180,270]  # degree
length = 50             # km

# judge Level II or SIGMET
if radar_name == 'RCWF':
    #decode data stored in radar object
    radar = pyart.io.read_nexrad_archive(loc+file)
    name = radar.metadata['instrument_name']
    #get time label from file name
    date = file.split('_')[0]
    time = file.split('_')[1]
elif radar_name == 'RCTP':
    #decode data stored in radar object
    radar = pyart.io.read_sigmet(loc+file)
    name = 'RCTP'
    #get time label from file name
    date = file.split('TIA')[1]
    time = date.split('.')[0]
    date = ''

xsect = pyart.util.cross_section_ppi(radar,angle)
display = pyart.graph.RadarDisplay(xsect)

#colormap
radcolors = [(0.70,0.70,0.70),(0.00,1.00,1.00),(0.00,0.75,1.00),(0.00,0.50,1.00),(0.00,0.70,0.30),(0.00,0.90,0.30),(1.00,1.00,0.00),(1.00,0.70,0.00),(1.00,0.00,0.00),(0.70,0.00,0.00),(0.81,0.34,0.64),(0.85,0.63,0.80)]
clv = [0.,5.,10.,15.,20.,25.,30.,35.,40.,45.,50.,55.,60.]
cmap = mpl.colors.ListedColormap(radcolors)
cmap.set_over(radcolors[-1])
cmap.set_under(radcolors[0])
norm = mpl.colors.BoundaryNorm(clv,cmap.N)

for ang in range(len(angle)):
    
    #start plot
    fig = plt.figure(figsize=(6,4))

    #plot cross section
    display.plot('reflectivity', ang, fig=fig, cmap=cmap, norm=norm, vmin=min(clv), vmax=max(clv), ticks=clv, colorbar_label='reflectivity (dBZ)', axislabels=('Distance (km)','Altitude (km)'), title=name+' reflectivity cross section at '+str(angle[ang])+' deg')
    display.set_limits(xlim=(0,length),ylim=(0,10))

    #output setting
    figname = des+name+'_'+date+time+'_'+str(angle[ang]).zfill(3)+'_dBZ_CS.png'
    print('Output is in ',figname)
    plt.savefig(figname)