import math
import pyart
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import warnings

print('1:Reflectivity, 2:Radial Velocity')
var = input('please input the variable you want to plot:')

print('plot cross-section line?')
print('0:no, 1:yes')
cross = input('need cross-section?:')

#ignore warning
warnings.filterwarnings('ignore')

radar_name = 'RCWF'
# radar_name = 'RCTP'

# file name
file = '20210912_0548_RCWF_VOL.654'   # RCWF
# file = 'TIA210912055005.RAW60CY'        # RCTP

#loc is the path where you store your unzipped radar data
#des is the path where you want to store the radar figures you plot
loc='data/'+radar_name+'/'
des='img/PPI/'


# for file in [loc+'RCWF/20210912_0548_RCWF_VOL.654',loc+'RCTP/TIA210912055005.RAW60CY']:
#judge Level II or SIGMET
if radar_name == 'RCWF':
    #decode data stored in radar object
    radar = pyart.io.read_nexrad_archive(loc+file)
    name = radar.metadata['instrument_name']
elif radar_name == 'RCTP':
    #decode data stored in radar object
    radar = pyart.io.read_sigmet(loc+file)
    name = 'RCTP'
display = pyart.graph.RadarMapDisplay(radar)

#basic radar information
lon = radar.longitude['data'][0]
lat = radar.latitude['data'][0]

for swp in range(radar.nsweeps):

    #Rmax
    stoprange = radar.instrument_parameters['unambiguous_range']['data'][0]/1000.
    dx = math.ceil(stoprange/100.)
    
    #first ray and its time and elevation in every sweep
    ray0 = radar.sweep_start_ray_index['data'][swp]
    time = str(pyart.util.datetimes_from_radar(radar)[ray0]).split(' ')
    date = time[0]
    tmlbl = str(time[1]).split(':')
    hh = tmlbl[0]
    mm = tmlbl[1]
    sec = tmlbl[2]

    elev = radar.elevation['data'][ray0]
    
    #colorbar
    if var == '1':
        dataname = 'reflectivity'
        varname = 'Reflectivity'
        savename = 'dBZ'
        unit = 'dBZ'
        radcolors = [(0.70,0.70,0.70),(0.00,1.00,1.00),(0.00,0.75,1.00),(0.00,0.50,1.00),(0.00,0.70,0.30),(0.00,0.90,0.30),(1.00,1.00,0.00),(1.00,0.70,0.00),(1.00,0.00,0.00),(0.70,0.00,0.00),(0.81,0.34,0.64),(0.85,0.63,0.80)]
        clv = [0.,5.,10.,15.,20.,25.,30.,35.,40.,45.,50.,55.,60.]
    elif var == '2':
        dataname = 'velocity'
        varname = 'V$_r$'
        savename = 'V'
        unit = 'm s$^{-1}$'
        radcolors = [(0.50,0.00,1.00),(0.50,0.50,1.00),(0.00,0.70,0.30),(0.00,0.90,0.30),(0.50,1.00,0.50),(0.70,1.00,0.70),(0.90,0.90,0.90),(1.00,1.00,0.00),(1.00,0.70,0.00),(0.75,0.53,0.28),(0.63,0.44,0.35),(0.87,0.37,0.47),(0.94,0.27,0.42)]
        nyq_vel = radar.instrument_parameters['nyquist_velocity']['data'][ray0]
        #auto choosing colorbar range
        if round(nyq_vel/6.) <= 1:
            dc = 1
        elif round(nyq_vel/6.) > 1:
            dc = round(nyq_vel/6.)
        clv = np.linspace(-6.,-1.,6)*dc
        if dc <= 1:
            clv = np.append(clv,np.linspace(-0.5,0.5,2))
        elif dc > 1:
            clv = np.append(clv,np.linspace(-1.,1.,2))
        clv = np.append(clv,np.linspace(1.,6.,6)*dc)
        
    print('processing sweep '+str(swp+1)+' '+dataname+' data')    
        
    #start plot
    fig = plt.figure(figsize=(10,10))
    
    #colormap
    cmap = mpl.colors.ListedColormap(radcolors)
    cmap.set_over(radcolors[-1])
    cmap.set_under(radcolors[0])
    norm = mpl.colors.BoundaryNorm(clv,cmap.N)

    #map projection based on cartopy
    map_proj = ccrs.PlateCarree()

    #ppi plot in pyart, please check pyart for more introductions of these parameter
    display.plot_ppi_map(dataname, swp, fig=fig, ax=111, projection=map_proj, resolution='10m',
                            min_lon=round(lon)-dx, max_lon=round(lon)+dx, lon_lines=np.linspace(round(lon)-dx,round(lon)+dx,2*dx+1),
                            min_lat=round(lat)-dx, max_lat=round(lat)+dx,lat_lines=np.linspace(round(lat)-dx,round(lat)+dx,2*dx+1),
                            cmap=cmap, norm=norm, vmin=min(clv), vmax=min(clv), ticks=clv, colorbar_label=varname+' ('+unit+')',
                            title='{0} of {1} {2} {3}:{4} UTC, elev={5:4.1f}$^o$'.format(varname,name,date,hh,mm,elev))

    # add circle centered radar
    display.plot_range_ring(50., linewidth=0.5,line_style='k--')
    display.plot_range_ring(100.,linewidth=0.5, line_style='k-')
    display.plot_range_ring(150.,linewidth=0.5, line_style='k--')
    display.plot_range_ring(200.,linewidth=0.5, line_style='k-')
    
    #add radar location and name
    mksize = dx
    display.plot_point(radar.longitude['data'][0], radar.latitude['data'][0], symbol='k^',label_text=radar_name,markersize=mksize)

    # add cross section line centered radar loc
    # example;

    if cross == '1':
        dirdeg = 0. # 0-360 degree
        length = 50. # in km
        print('Plotting a cross-section line...')
        xx = length*1000*math.sin(dirdeg*math.pi/180)
        yy = length*1000*math.cos(dirdeg*math.pi/180)
        display.plot_line_xy([0,xx],[0,yy],color='black',line_style='-')

    figname = des+name+'_'+date+'_'+hh+mm+'_'+savename+'_'+str(swp+1)+'.png'
    print('Output is in ',figname)
    plt.savefig(figname)