import numpy as np
import scipy.optimize as sp_opt
from math import pi,log,e
import matplotlib.pyplot as plt

def asTuplarray(star_dictionary,
		outliner_decay= lambda x:np.minimum(1,np.maximum(0,(x-2.5)/1.0)),
		grade_decay= lambda g: min(1,(ord(g)-65)*0.45)
		):
	""" Transforms a dictionary with information from a given star (as readed
	from a FITS file) on a tuple of numpy arrays, corresponding to (x,y,weight).
	The weight is calculated trying to eliminate outliers using the outliner_decay
	function. Also the grade_decay fuction also cleans the data according to the
	observation grade.
	"""
	xx= np.array(star_dictionary['HJD'])
	yy= np.array(star_dictionary['MAG_3'])

	decay= np.array(map(grade_decay,star_dictionary['GRADE']))
	weightd= 1-decay

	weight= weightd
	for k in xrange(7):
		mean= np.sum(yy*weight)/np.sum(weight)
		vari= np.sum((yy-mean)*(yy-mean)*weight)/np.sum(weight)
		if vari==0:
			weight= np.ones(len(xx))
			break
		individual_vari_coef= ((yy-mean))**2/vari
		weight= weightd*(1-outliner_decay(individual_vari_coef))
	print(sum(weight))
	return (xx,yy,weight)


def test_variability(star_tuplarray,time_step= 0.1,display=True):

	px_large= np.arange(min(star_tuplarray[0])-1, max(star_tuplarray[0])+1,time_step)

	xx_tot= star_tuplarray[0]
	yy_tot= star_tuplarray[1]
	ww_tot= star_tuplarray[2]

	# @@@@ Create the first guest:
	s,f= detect_cuadratic_start_and_end_indexes(xx_tot,yy_tot,ww_tot)
	if s==False and f==False:
		return False
	xx= xx_tot[s:f+1]
	yy= yy_tot[s:f+1]
	ww= ww_tot[s:f+1]

	# Calculation of the phase using the vertex of a cuadratic fit
	# to make the optimization more accurate
	pf= np.polyfit(xx, yy, 2, rcond=None, full=False, w=ww, cov=False)
	px= np.arange(min(xx)-1, max(xx)+1, .01)
	pv= np.polyval(pf, px)

	# Calculate the parameters of the guessed wave:
	guessed_start_x= -pf[1]/(2.0*pf[0])
	gussed_start_y= pf[0]*guessed_start_x**2+pf[1]*guessed_start_x+pf[2]
	# Calculation of the guessed mean
	guessed_mean= np.average(yy,weights=ww)
	# Calculation of the guessed ponderated standart deviation
	guessed_std= (np.sum(((yy-guessed_mean)**2)*ww)/float(np.sum(ww)))**0.5
	# Guessed amplittude
	guessed_amp= 2*(-1 if pf[2]>0 else 1)*guessed_std
	#guessed_mean-= guessed_amp/2.0
	# Guessed expantion
	guessed_expan= pi/(2*abs(guessed_amp/float(pf[0]))**0.5)

	# Function to optimize:
	def optimize_func(val,xx,yy,ww):
		ret= (val[0]*np.cos(val[3]*(xx-guessed_start_x)+val[1])+val[2]-yy)*ww
		return ret
	# Function gradient:
	def optimize_func_grad(val,xx,yy,ww):
		ret= [
			np.cos(val[3]*(xx-guessed_start_x)+val[1])*ww,
			-val[0]*np.sin(val[3]*(xx-guessed_start_x)+val[1])*ww,
			ww,
			-val[0]*np.sin(val[3]*(xx-guessed_start_x)+val[1])*ww*(xx-guessed_start_x)
		]
		return ret
	# Fitting, and get the estimations:
	est_amp, est_phase, est_mean, est_expan= sp_opt.leastsq(optimize_func,
		[guessed_amp,0.0,guessed_mean,guessed_expan],
		args=(xx_tot,yy_tot,ww_tot), Dfun=optimize_func_grad, col_deriv=1)[0]
	data_fit= est_amp*np.cos(est_expan*(px_large-guessed_start_x)+est_phase)+est_mean
	data_guess= guessed_amp*np.cos(guessed_expan*(px_large-guessed_start_x)+0.0)+(gussed_start_y-guessed_amp)

	if display:
		plt.clf()
		plt.plot(star_tuplarray[0],star_tuplarray[1],'go')
		plt.plot(xx_tot,yy_tot,'ro')
		plt.plot(xx,yy,'bo')
		plt.plot(px_large,data_fit,label='after fitting')
		plt.plot(px_large,data_guess,label='first guess')
		plt.plot(px,pv,'k--',label='quadratic fit')
		plt.legend()
		plt.show()


def detect_cuadratic_start_and_end_indexes(xx,yy,ww):
	best_score=0
	best_i=0
	best_f=0
	available= False

	while best_i<len(xx)-1:
		if ww[best_i]!=1.0:
			best_i+=1
		else:
			break
	ix=best_i

	while ix<len(xx):
		if ww[ix]<1.0:
			ix+=1
			continue
		yys= yy[0:ix+1]
		xxs= xx[0:ix+1]
		wws= ww[0:ix+1]
		if xxs[-1]!=xxs[0]:
			coefs= (xxs-xxs[0])/float(xxs[-1]-xxs[0])
		else:
			coefs= 0
		line= yys[-1]*coefs+yys[0]*(1.0-coefs)
		score= np.sum(wws*(yys-line)**2/float(np.sum(wws)))**0.5
		if score>best_score:
			best_score= score
			best_f= ix
			available=True
		ix+=1
	if not available: return False,False

	ix=best_i
	while ix<best_f:
		if ww[ix]<1.0:
			ix+=1
			continue
		yys= yy[ix:best_f+1]
		xxs= xx[ix:best_f+1]
		wws= ww[ix:best_f+1]
		coefs= (xxs-xxs[0])/float(xxs[-1]-xxs[0])
		line= yys[-1]*coefs+yys[0]*(1.0-coefs)
		score= np.sum(wws*(yys-line)**2/float(np.sum(wws)))**0.5
		if score>best_score:
			best_score= score
			best_i= ix
			available=True
		ix+=1
	if not available: return False,False

	return (best_i,best_f)
