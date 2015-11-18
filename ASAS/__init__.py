from parser import get_file_data,get_files_data,save_to_fits

from graphic import *

if __name__=="__main__":
	# A test:
	# Read some files:
	dictionary_list= get_files_data(["../test/000006+2553.2","../test/000007+1844.3"])
	num=8 #also valid: 8,20,25
	print dictionary_list[num]
	# Print the keys of a dictionary list (a file contains many):
	print dictionary_list[0].keys()
	# Save the stars on a FITS
	save_to_fits(dictionary_list,"../test/output.fits")
	# Pass it to an auxiliar format to do the fit later (in development):
	tuplarray= asTuplarray(dictionary_list[num])
	# And show the fit.
	show(tuplarray)
	print "Tests done!"
