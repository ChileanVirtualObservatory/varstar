from parser import get_file_data,get_files_data,save_to_fits

from detector import *
import os

if __name__=="__main__":
	# A test:
	# Read some files:
	dirname="../test/"
	data_file_names=[]
	for file in os.listdir(dirname):
	    if not file.endswith(".fits"):
	        data_file_names.append(file)
	data_files= map((lambda x: dirname+x),data_file_names)
	dictionary_list= get_files_data(data_files)
	k=1
	for num in xrange(len(dictionary_list)):
		star= dictionary_list[num]
		# Pass it to an auxiliar format to do the fit later (in development):
		tuplarray= asTuplarray(star)
		# And show the fit.
		test_variability(tuplarray)
		# Save the stars on a FITS
		#save_to_fits(dictionary_list,"../output/"+str(k)+"."+star['ORIGIN'].split('/')[-1])
		k+=1
	print "Tests done!"
