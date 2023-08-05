#Luca Pinello 2019, @lucapinello
#GPLv3 license

from scipy import optimize, interpolate
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter
from collections import OrderedDict
import numpy as np
import scipy as sp
import warnings
warnings.filterwarnings("ignore")

import argparse
import sys
import matplotlib
matplotlib.use('Qt5Agg')
import pylab as plt
from pylab import plot, ginput, show, axis

import json

import intervaltree
from scipy.interpolate import UnivariateSpline

from matplotlib.widgets import Cursor


flat_list = lambda l: [item for sublist in l for item in sublist]

def write_artisan_alarm_profile(alarm_filename,seconds,temp_profile,fan_profile,decimate=1,preheat_time=29):

    profile=OrderedDict()
    if decimate>1:
        seconds=seconds[::decimate]
        temp_profile=temp_profile[::decimate]
        fan_profile=fan_profile[::decimate]


    len_profile=len(temp_profile)*2

    #alarmactions
    #16 charge
    #6 temp
    #4 fan
    #13 drop
    #14 cool end

    profile['alarmactions']=[16]+[6,4]*len(temp_profile)+[13,14,15,-1,-1]


    #alarmstrings contains the temperature and fan values,
    #here we assume that temp and fan are alternating
    profile['alarmstrings']=list(map(str,['charge']+flat_list(list(zip(temp_profile,fan_profile)))+['drop','cool end','off','temp Manual','fan manual']))


    #alarmconds always 1
    profile['alarmconds']=[1]+[1]*(len_profile)+[1]*5

    idx_alrm_temp_manual=len(profile['alarmconds'])-2
    idx_alrm_fan_manual=len(profile['alarmconds'])-1

    #alarmnegguards and alarmguards  and alarmtimes  -1
    profile['alarmnegguards']=[-1]+ [idx_alrm_temp_manual,idx_alrm_fan_manual]*len(temp_profile) +[-1]*5
    profile['alarmguards']=[-1]*(len_profile+6)
    profile['alarmtimes']=[-1]*(len_profile+6)

    #alarmflags and alarmsources 1
    profile['alarmflags']=[1]*(len_profile+6)
    profile['alarmsources']=[1]+[1,1]*len(temp_profile)+[1]*3+[2,3]

    #alarmtemperatures always 500
    profile['alarmtemperatures']=[500]+[500]*(len_profile)+[500]*3+[0.5,0.5]

    #alarmoffsets is the time, we need to add 30 for accounting the preheat phase
    last_time=max(seconds)
    profile['alarmoffsets']=list(map(int,[preheat_time]+flat_list([ (a,a) for a in seconds])+[last_time+1,last_time+1+60*3,last_time+5+60*3,0,0]))

    #alarmbeep always 0
    profile['alarmbeep']=[0]*(len_profile+6)

    json.dump(profile,open(alarm_filename,'w+'))

def read_csv(csv_filename):
    pts=[]
    with open(csv_filename) as infile:
        for line in infile:
            pts.append(tuple(map(int,line.strip().split(','))))
        return pts

def write_csv(pts,csv_filename):
    with open(csv_filename,'w+') as outfile:
        for p in pts:
            outfile.write('%d,%d\n' %p)


def main():

    print(\
'''
      _____ _____  ______ ___   ___
     / ____|  __ \|____  / _ \ / _ \\
    | (___ | |__) |   / / | | | | | |
     \___ \|  _  /   / /| | | | | | |
     ____) | | \ \  / / | |_| | |_| |
    |_____/|_|  \_\/_/   \___/ \___/
     /\        | | (_)
    /  \   _ __| |_ _ ___  __ _ _ __
   / /\ \ | '__| __| / __|/ _` | '_ \\
  / ____ \| |  | |_| \__ \ (_| | | | |
 /_/  __\_\_|   \__|_|___/\__,_|_| |_|
     |  __ \          / _(_) |
     | |__) | __ ___ | |_ _| | ___
     |  ___/ '__/ _ \|  _| | |/ _ \\
     | |   | | | (_) | | | | |  __/
    _|_|   |_|  \___/|_|_|_|_|\___|
   |  _ \      (_) |   | |
   | |_) |_   _ _| | __| | ___ _ __
   |  _ <| | | | | |/ _` |/ _ \ '__|
   | |_) | |_| | | | (_| |  __/ |
   |____/ \__,_|_|_|\__,_|\___|_|
''')

    print('SR700 Artisan Profile Builder - Luca Pinello 2019 (@lucapinello)\n\n')
    print('Send bugs, suggestions or *green coffee* to lucapinello AT gmail DOT com\n\n')

    parser = argparse.ArgumentParser(description='Parameters',formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--n_points_temp',  type=int,  default=4)
    parser.add_argument('--n_points_fan',  type=int,  default=8)
    parser.add_argument('-n','--profile_filename',  help='Output name', default='artisan_profile_alarms.alrm')
    parser.add_argument('--start_time',  type=int,  default=30)
    parser.add_argument('--end_time',  type=int,  default=720)
    parser.add_argument('--min_temp',  type=int,  default=120,choices=range(120,200))
    parser.add_argument('--max_temp',  type=int,  default=500,choices=range(400,550))
    parser.add_argument('--fit_curve',  type=str,  default='spline',choices=['log','spline'])
    parser.add_argument('--use_precomputed_fan',  action='store_true')
    parser.add_argument('--temp_file',  type=str, default=None)
    parser.add_argument('--fan_file',  type=str, default=None)








    args = parser.parse_args()

    n_points_temp=args.n_points_temp
    n_points_fan=args.n_points_fan

    if args.fit_curve=='log' or args.n_points_temp==2:
        use_log=True
    else:
        use_log=False

    print(use_log)
    min_time=args.start_time
    max_time=args.end_time

    x_min=min_time-30
    x_max=max_time+30
    y_min_temp=args.min_temp-50
    y_max_temp=args.max_temp+50
    y_min_fan=0
    y_max_fan=100
    y_min_ror=0
    y_max_ror=50

    if args.temp_file:
        pts=read_csv(args.temp_file)
    else:
        #plot to get points for temp
        fig = plt.figure(figsize=(11, 7))
        ax = fig.add_subplot(1, 1, 1)
        ax.set_title('\nArtisan Profile Builder - Luca Pinello 2019\n\nPress the spacebar to add sequentially %d points inside the dotted area\nUse mouse right click to undo last point added' % n_points_temp)

        axis([x_min, x_max, y_min_temp, y_max_temp])

        plt.xticks(np.arange(x_min,x_max,30),np.arange(x_min,x_max,30)/60,rotation = 45, ha="right")

        ax.set_xlabel('Minutes')
        ax.set_ylabel('Temperature in F°')

        cursor = Cursor(ax, useblit=False, color='k', linewidth=1)
        plt.plot([args.start_time,args.start_time],[y_min_temp,y_max_temp],'--k')
        plt.plot([args.end_time,args.end_time],[y_min_temp,y_max_temp],'--k')
        plt.plot([x_min,x_max],[args.min_temp,args.min_temp],'--k')
        plt.plot([x_min,x_max],[args.max_temp,args.max_temp],'--k')
        plt.grid(True)
        pts = ginput(n_points_temp,show_clicks=True, mouse_pop=True,timeout=0) # it will wait for three clicks
        print ("The points selected are:\n")
        print(pts) # ginput returns points as tuples
        plt.close()

    #sort points
    x_temp=list(map(lambda x: x[0],pts)) # map applies the function passed as
    y_temp=list(map(lambda x: x[1],pts)) # first parameter to each element of pts
    idxs_sort=np.argsort(x_temp)

    x_temp=list(np.array(x_temp)[idxs_sort])
    y_temp=list(np.array(y_temp)[idxs_sort])
    xi_seconds=np.arange(x_min,x_max,1)
    seconds=list(np.arange(min_time,max_time,1))

    if use_log:

        x_pairs=[ [x_temp[i],x_temp[i+1]] for i in range(len(x_temp)-1)]
        y_pairs=[ [y_temp[i],y_temp[i+1]] for i in range(len(x_temp)-1)]

        print(x_pairs,y_pairs)

        range_tree = intervaltree.IntervalTree()

        fs_to_fit=list()

        for idx, (xp,yp) in enumerate(zip(x_pairs,y_pairs)):

            [a_f,b_f]=optimize.curve_fit(lambda t,a,b: a+b*np.log1p(t),  xp,  yp)[0]

            fs_to_fit.append(eval(''.join(map(str,['lambda x: ',eval('a_f'),'+',eval('b_f'),'*np.log1p(x)']))))

            if len(x_pairs)==1:
                range_tree[0:2000]=fs_to_fit[idx]
            elif idx==len(x_pairs)-1:
                range_tree[xp[0]:2000]=fs_to_fit[idx]
            elif idx==0:
                range_tree[0:xp[1]]=fs_to_fit[idx]
            else:
                range_tree[xp[0]:xp[1]]=fs_to_fit[idx]

        print(range_tree)
        def piecewise_log(x_values,range_tree):
            if len(x_values)==1:
                return range_tree[x_values].pop().data(x_values)
            else:
                return [range_tree[x_value].pop().data(x_value) for x_value in x_values]

    	#[a,b]=optimize.curve_fit(lambda t,a,b: a+b*np.log10(t),  x_temp,  y_temp)[0]
        #[a,b]=optimize.curve_fit(lambda t,a,b: a+b*np.log1p(t), x_temp,  y_temp)[0]
        #f_fit = lambda x: a + b*np.log1p(x)

        s = UnivariateSpline(seconds, piecewise_log(seconds,range_tree), s=len(seconds),k=2)
        temp_profile=np.clip(s(seconds),args.min_temp,args.max_temp)
        #temp_profile=np.clip(piecewise_log(seconds,range_tree),150,550)
        #temp_profile=np.clip(f_fit(seconds),150,550)

    else:
    	#tck_temp = interpolate.splrep(x_temp, y_temp, s=0)
        #tck_temp = interpolate.splrep(x_temp, y_temp,k=2,s=1E10)
        #temp_profile= interpolate.splev(seconds, tck_temp, der=0)
        s = UnivariateSpline(x_temp,y_temp,k=2,s=0)
        temp_profile=s(seconds)

    #plot to get the obtained temp curve
    fig = plt.figure(figsize=(11, 7))
    pdf_filename='target_curve_for_%s.pdf' % args.profile_filename
    plt.title('\nArtisan Profile Builder - Luca Pinello 2019\n\nTemperature Curve')
    ax = fig.add_subplot(1, 1, 1)
    plt.xticks(np.arange(x_min,x_max,30),np.arange(x_min,x_max,30)/60,rotation = 45, ha="right")

    plt.xlabel('Minutes')
    plt.ylabel('Temperature in F°')


    axis([x_min, x_max, y_min_temp, y_max_temp])
    plt.plot([args.start_time,args.start_time],[y_min_temp,y_max_temp],'--k')
    plt.plot([args.end_time,args.end_time],[y_min_temp,y_max_temp],'--k')
    plt.plot([x_min,x_max],[args.min_temp,args.min_temp],'--k')
    plt.plot([x_min,x_max],[args.max_temp,args.max_temp],'--k')
    plt.grid(True)

    temp_profile=[min(args.max_temp,max(args.min_temp,a)) for a in map(int,temp_profile)]
    plot(seconds,temp_profile,'-')
    plt.show()

    write_csv(pts,args.profile_filename+'_temperatures.csv')


    if args.use_precomputed_fan:

        pts=[(91.05571847507332, 89.98144712430428), (120.08797653958945, 79.96289424860855), (149.99999999999997, 70.68645640074213), (179.03225806451613, 60.1113172541744), (209.82404692082113, 51.02040816326531), (240.61583577712608, 39.888682745825605), (300.43988269794716, 30.24118738404453), (360.2639296187683, 20.037105751391472)]

    elif args.fan_file:
        pts=read_csv(fan_file)
    else:
        #plot to get points for fan
        fig = plt.figure(figsize=(11, 7))
        ax = fig.add_subplot(1, 1, 1)
        plt.xticks(np.arange(x_min,x_max,30),np.arange(x_min,x_max,30)/60,rotation = 45, ha="right")

        plt.xlabel('Minutes')
        plt.ylabel('Fan Speed (10-90)')

        plt.title('\nArtisan Profile Builder - Luca Pinello 2019\n\nPress the spacebar to add sequentially %d points inside the dotted area\nUse mouse right click to undo last point added' % n_points_fan)

        axis([x_min, x_max, y_min_fan, y_max_fan])


        cursor = Cursor(ax, useblit=False, color='k', linewidth=1)
        plt.plot([args.start_time,args.start_time],[y_min_fan,y_max_fan],'--k')
        plt.plot([args.end_time,args.end_time],[y_min_fan,y_max_fan],'--k')
        plt.plot([x_min,x_max],[10,10],'--k')
        plt.plot([x_min,x_max],[90,90],'--k')
        plt.grid(True)

        pts = ginput(n_points_fan,show_clicks=True, mouse_pop=True,timeout=0) # it will wait for three clicks
        print ("The points selected are:\n")

        plt.close()

    print(pts) # ginput returns points as tuples
    x_fan=list(map(lambda x: x[0],pts)) # map applies the function passed as
    y_fan=list(map(lambda x: x[1],pts)) # first parameter to each element of pts

    #sort points

    idxs_sort=np.argsort(x_fan)

    x_fan=list(np.array(x_fan)[idxs_sort])
    y_fan=list(np.round(np.array(y_fan)[idxs_sort]))



    f=interp1d(x_fan, y_fan, kind='previous', fill_value="extrapolate")
    fan_profile = f(seconds)
    fan_profile =list(map(int,[max(10,min(90,int(a/10)*10)) for a in fan_profile ]))

    #plot to get the obtained fan curve
    fig = plt.figure(figsize=(11, 7))
    plt.title('\nArtisan Profile Builder - Luca Pinello 2019\n\nFan Curve')

    ax = fig.add_subplot(1, 1, 1)
    plt.xticks(np.arange(x_min,x_max,30),np.arange(x_min,x_max,30)/60,rotation = 45, ha="right")

    plt.xlabel('Seconds')
    plt.ylabel('Fan Speed (10-90)')

    axis([x_min, x_max, y_min_fan, y_max_fan])
    plt.plot([args.start_time,args.start_time],[y_min_fan,y_max_fan],'--k')
    plt.plot([args.end_time,args.end_time],[y_min_fan,y_max_fan],'--k')
    plt.plot([x_min,x_max],[10,10],'--k')
    plt.plot([x_min,x_max],[90,90],'--k')
    plt.grid(True)

    plot(seconds,fan_profile,'-')
    #plt.yticks(np.arange(0,100,10))
    plt.show()
    plt.close()
    write_csv(pts,args.profile_filename+'_fan.csv')


    #plot with everything
    fig = plt.figure(figsize=(8*1.2, 10*1.2),dpi=72)

    #temp
    ax1 = fig.add_subplot(3, 1, 1)
    plt.title('\nArtisan Profile Builder - Luca Pinello 2019\n\nClose this plot to save the profile in: %s\nA pdf of these curves will be also saved in: %s\n\n Temperature Curve' % (args.profile_filename,pdf_filename))

    axis([x_min, x_max, y_min_temp, y_max_temp])
    plt.xticks(np.arange(x_min,x_max,30),[])
    plt.ylabel('Temperature in F°')


    plt.yticks(np.arange(y_min_fan,y_max_temp,50))
    plt.grid(True)
    plot(seconds,temp_profile,'-r',lw=3)

    #fan
    ax2 = fig.add_subplot(3, 1, 2)
    axis([x_min, x_max, 0, 100])

    plt.ylabel('Fan Speed (10-90)')
    plt.xticks(np.arange(x_min,x_max,30),[])


    plt.yticks(np.arange(0,100,10))
    plt.title('Fan Curve')
    plt.grid(True)

    plot(seconds,fan_profile,'-g',lw=3)

    ax3 = fig.add_subplot(3, 1, 3)


    plt.xlabel('Minutes')
    plt.xticks(np.arange(x_min,x_max,30),np.arange(x_min,x_max,30)/60,rotation = 45, ha="right")
    plt.ylabel('Delta(BT)')
    plt.title('ROR Curve')
    plt.grid(True)


    ror=[ (temp_profile[i+30]-temp_profile[i]) for i in range(len(temp_profile)-30)]
    seconds_ror=seconds[:len(ror)]

    #ror = savgol_filter(ror, 61, 3)
    s_ror = UnivariateSpline(seconds_ror,ror,k=2,s=len(seconds_ror))
    ror=s_ror(seconds_ror)
    axis([x_min, x_max, 0,ror.max()+5])
    plot(seconds_ror,ror,'-b',lw=3)


    #plt.tight_layout()

    pdf_filename='target_curve_for_%s.pdf' % args.profile_filename
    plt.savefig(pdf_filename)

    plt.show()

    write_artisan_alarm_profile(args.profile_filename+'.alrm',seconds,temp_profile,fan_profile,decimate=20)

    print('\nProfile was saved in: %s.\n\nA pdf of this curve was saved in: %s!' % (args.profile_filename, pdf_filename))
    print('\nSend bugs, suggestions or *green coffee* to lucapinello AT gmail DOT com\n')
    print('Bye!\n')


if __name__ == "__main__":
    main()
