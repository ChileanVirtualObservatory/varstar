from parser import get_file_data,get_files_data,save_to_fits

if __name__=="__main__":
	dictionary_list= get_files_data(["../test/000006+2553.2","../test/000007+1844.3"])
	print dictionary_list
	save_to_fits(dictionary_list,"../test/output.fits")
	print "Tests done!"
