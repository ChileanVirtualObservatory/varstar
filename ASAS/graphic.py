"""
Demo of spines using custom bounds to limit the extent of the spine.
"""
import numpy as np
import scipy.optimize as sp_opt
import matplotlib.pyplot as plt
from math import pi

def asTuplarray(star_dictionary,
		outliner_decay= lambda x:np.minimum(1,np.maximum(0,(x-2.5)/1.0)),
		grade_decay= lambda g: min(1,(ord(g)-65)*0.45)
		):
	xx= np.array(star_dictionary['HJD'])
	yy= np.array(star_dictionary['MAG_3'])

	decay= np.array(map(grade_decay,star_dictionary['GRADE']))
	weight= 1-decay

	mean= np.mean(yy)
	vari= np.var(yy)
	if vari==0:
		raise ValueError('Cannot work with data with variation 0.')
	individual_vari_coef= (yy-mean)**2/vari
	weight= weight*(1-outliner_decay(individual_vari_coef))

	return (xx,yy,weight)


def show(star_tuplarray):
	# Graph all the points and xranges
	plt.plot(star_tuplarray[0],star_tuplarray[1],'go')
	px_large= np.arange(min(star_tuplarray[0])-1, max(star_tuplarray[0])+1, .01)


	xx= star_tuplarray[0][:30] #:30 just for testing.
	yy= star_tuplarray[1][:30] #:30 just for testing.
	ww= star_tuplarray[2][:30]
	plt.plot(xx,yy,'ro')


	# Calculation of the phase using the vertex of a cuadratic fit
	# to make the optimization more accurate
	pf= np.polyfit(xx, yy, 2, rcond=None, full=False, w=ww, cov=False)
	px= np.arange(min(xx)-1, max(xx)+1, .01)
	pv= np.polyval(pf, px)

	# SECOND METHOD (works with a half of a cycle):
	guessed_start= -pf[1]/(2.0*pf[0])
	# Calculation of the guessed mean
	guessed_mean= np.average(yy,weights=ww)
	# Calculation of the guessed ponderated standart deviation
	guessed_std= (np.sum(((yy-guessed_mean)**2)*ww)/float(np.sum(ww)))**0.5
	# Guessed amplittude
	guessed_amp= 2*(-1 if pf[2]>0 else 1)*guessed_std
	#guessed_mean-= guessed_amp/2.0
	# Guessed expantion
	guessed_expan= pi/(2*abs(guessed_amp/float(pf[0]))**0.5)

	print "guess:"
	print guessed_amp,0.0,guessed_mean,guessed_expan
	# Function to optimize:
	optimize_func= lambda x: (x[0]*np.cos(x[3]*(xx-guessed_start)+x[1])+x[2]-yy)*ww
	# Fitting, and get the estimations:
	est_amp, est_phase, est_mean, est_expan= sp_opt.leastsq(optimize_func,
		[guessed_amp,0.0,guessed_mean,guessed_expan])[0]
	data_fit= est_amp*np.cos(est_expan*(px_large-guessed_start)+est_phase)+est_mean
	data_guess= guessed_amp*np.cos(guessed_expan*(px_large-guessed_start)+0.0)+guessed_mean
	print "estimated:"
	print est_amp, est_phase, est_mean, est_expan

	"""
	# FIRST METHOD (works with a whole of a cycle (or a two semi-halfs)):
	guessed_phase= -pf[1]/(2.0*pf[0])/4.0*2.0*pi
	# Calculation of the guessed mean
	guessed_mean= np.average(yy,weights=ww)
	# Calculation of the guessed ponderated standart deviation
	guessed_std= np.sum(((yy-guessed_mean)*ww)**2)**0.5
	# Guessed amplittude
	guessed_amp= (-1 if pf[2]>0 else 1)*guessed_std
	# Function to optimize:
	optimize_func= lambda x: x[0]*np.sin(xx+x[1])+x[2]-yy
	# Fitting, and get the estimations:
	est_amp, est_phase, est_mean= sp_opt.leastsq(optimize_func,
		[guessed_amp,guessed_phase,guessed_mean])[0]
	data_fit= est_amp*np.sin(px+est_phase)+est_mean
	"""

	plt.plot(px_large,data_fit,label='after fitting')
	plt.plot(px_large,data_guess,label='first guess')
	plt.plot(px,pv,'k--',label='quadratic fit')
	plt.legend()
	plt.show()




	"""
	guess_mean = np.mean(data)
	guess_std = 3*np.std(data)/(2**0.5)
	guess_phase = 0

	# we'll use this to plot our first estimate. This might already be good enough for you
	data_first_guess = guess_std*np.sin(t+guess_phase) + guess_mean

	# Define the function to optimize, in this case, we want to minimize the difference
	# between the actual data and our "guessed" parameters
	optimize_func = lambda x: x[0]*np.sin(t+x[1]) + x[2] - data
	est_std, est_phase, est_mean = leastsq(optimize_func, [guess_std, guess_phase, guess_mean])[0]

	# recreate the fitted curve using the optimized parameters
	data_fit = est_std*np.sin(t+est_phase) + est_mean

	plt.plot(data, '.')
	plt.plot(data_fit, label='after fitting')
	plt.plot(data_first_guess, label='first guess')
	plt.legend()
	plt.show()
	"""
	"""
	x = np.linspace(0, 2*np.pi, 50)
	y = np.sin(x)
	y2 = y + 0.1 * np.random.normal(size=x.shape)

	#pts= np.array(star_dictionary['HJD'],star_dictionary['MAG_3'])

	fig, ax = plt.subplots()
	ax.plot(x, y, 'k--')
	ax.plot(x, y2, 'ro')

	# set ticks and tick labels
	ax.set_xlim((0, 2*np.pi))
	ax.set_xticks([0, np.pi, 2*np.pi])
	ax.set_xticklabels(['0', '$\pi$','2$\pi$'])
	ax.set_ylim((-1.5, 1.5))
	ax.set_yticks([-1, 0, 1])

	# Only draw spine between the y-ticks
	ax.spines['left'].set_bounds(-1, 1)
	# Hide the right and top spines
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)
	# Only show ticks on the left and bottom spines
	ax.yaxis.set_ticks_position('left')
	ax.xaxis.set_ticks_position('bottom')
	"""

	plt.show()
