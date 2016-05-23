from scipy import optimize
import numpy as np
from .pondering import proximity_ponderation,outlier_ponderation
from math import pi

def trigono_plus_lineal(A,t):
    return A[0]*np.cos(A[2]*t)+A[1]*np.sin(A[2]*t)+A[3]+A[4]*t

def error_function(A,t,y,w):
    return (trigono_plus_lineal(A,t)-y)*w

def jac_errfunc(A,t,y,w):
    jac_err= np.zeros((5,t.shape[0]))
    jac_err[0,:]= np.cos(A[2]*t)
    jac_err[1,:]= np.sin(A[2]*t)
    jac_err[2,:]= (-A[0]*np.sin(A[2]*t)+A[1]*np.cos(A[2]*t))*t
    jac_err[3,:]= 1.0
    jac_err[4,:]= t
    return jac_err*w

def fit(data,cycles_guess=2.0):
    data= np.array(data)
    xdata= data[:,0]
    ydata= data[:,1]
    ponderation= proximity_ponderation(xdata)*outlier_ponderation(ydata)
    mean= np.sum(ydata*ponderation)/np.sum(ponderation)
    stdev= np.std(ydata*ponderation)/np.sum(ponderation)
    rangx= np.amax(xdata)-np.amin(xdata)
    w0= cycles_guess*2*pi/rangx
    A0= [stdev,stdev,w0,mean,0.0]
    fit= optimize.leastsq(error_function, A0, args=(xdata,ydata,ponderation), Dfun=jac_errfunc, col_deriv=True)
    function= lambda t: trigono_plus_lineal(fit[0],t)
    fit= list(fit)
    fit.append(function)
    return fit
