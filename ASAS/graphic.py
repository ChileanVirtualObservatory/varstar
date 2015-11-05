"""
Demo of spines using custom bounds to limit the extent of the spine.
"""
import numpy as np
import matplotlib.pyplot as plt

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
	individual_vari_coef= (yy-mean)**2/vari
	weight= weight*(1-outliner_decay(individual_vari_coef))

	return (xx,yy,weight)
	#print weight
	#print vari


def show(star_tuplarray):
	xx= star_tuplarray[0][:25] #:25 just for testing.
	yy= star_tuplarray[1][:25] #:25 just for testing.
	ww= star_tuplarray[2][:25]
	#xx= star_dictionary['HJD']
	#yy= star_dictionary['MAG_3']
	plt.plot(xx,yy,'ro')

	pf= np.polyfit(xx, yy, 2, rcond=None, full=False, w=ww, cov=False)
	px= np.arange(min(xx)-1, max(xx)+1, .01)
	pv= np.polyval(pf, px)

	plt.plot(px,pv,'k--')
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
