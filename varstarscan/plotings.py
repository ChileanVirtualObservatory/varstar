from .pondering import proximity_ponderation,outlier_ponderation
from .fitting import fit

import numpy as np
import matplotlib.pyplot as plt

def plot(points,res=256):
    fig, ax1 = plt.subplots()

    points= np.array(points)
    xpoints= points[:,0]
    ypoints= points[:,1]
    ponder= proximity_ponderation(xpoints)*outlier_ponderation(ypoints)

    fit_res= fit(points)
    fit_func= fit_res[-1]
    xpointsfit= np.linspace(np.amin(xpoints),np.amax(xpoints),res)
    ypointsfit= fit_func(xpointsfit)

    ax1.plot(xpoints, ypoints, 'ro', label="observations")
    ax1.plot(xpointsfit, ypointsfit, 'g-',label="fitting")
    ax1.set_xlabel('date (HJD)')
    ax2 = ax1.twinx()
    ax1.set_ylabel('Magnitude')

    ax2.plot(xpoints, ponder, '-bs',label="ponderation")
    ax2.set_ylabel('Ponderation')
    ax2.set_ylim(ymin=0)

    ax1.legend(loc=3)
    ax2.legend(loc=4)
    plt.show()
