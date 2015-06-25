from astropy.io import fits
import numpy

import re

GRADE_PARSING= lambda x: ord(x)-65

def get_file_data(filename):
	"""
	Reads a file from the ASAS and returns a list of dictionaries containing all the pairs key-value
	from it. For each dictionary, for the tables, each column is represented as a list on the
	dictionary's key which name matchs the column's name.
	"""
	document= open(filename,'r')
	data=[]
	pairs={'ORIGIN':filename}
	actuald=None #Will be used to save the magnitude's table
	for line in document:
		if line[0]=='#':
			key= re.match(r"#.*=",line)
			if key:
				#It's a key
				key= key.group()[1:-1]
				values= (line.strip()[len(key)+2:]).split(' ')
				values= [x for x in values if x!='']
				values= tuple(values)
				if len(values)==1:
					pairs[key]= values[0]
				else:
					pairs[key]= values
				#If a data block has been completely red, add it to the data. 
				if actuald!=None:
					pairs.update(actuald)
					data.append(pairs)
					actuald=None
					pairs={'ORIGIN':filename}
			else:
				#It's a multiple key description
				keys= re.findall(r"\s\S+",line)
				keys= map(lambda x: x[1:],keys)
				#Restart the current dictionary
				actuald={}
				for k in keys:
					actuald[k]=[]
		else:
			#Extract the values and append them to the dictionary of multiple keys.
			values= re.findall(r"\S+[\s$]",line)
			values= map(lambda x: x[:-1],values)
			values_final=[]
			for value in values:
				try: values_final.append(float(value))
				except: values_final.append(GRADE_PARSING(value))
			for i in xrange(len(values_final)):
				actuald[keys[i]].append(values_final[i])
	pairs.update(actuald)
	data.append(pairs)
	return data


def get_files_data(filenames):
	"""
	The same as get_file_data but receibes multiple files.
	"""
	dict_list=[]
	for fip in filenames:
		dict_list= dict_list+ get_file_data(fip)
	return dict_list

def save_to_fits(dictionary_list,filename):
	"""
	Saves all the dictionaries of the list onto a FITS file.
	"""
	first=True
	hdus=[]
	for dictionary in dictionary_list:
		data_matrix=[]
		hdu = fits.PrimaryHDU()
		line_number=0
		for key,val in dictionary.items():
			if type(val) == list:
				hdu.header['LIN'+'0'*(5-len(str(line_number)))+str(line_number)]= key
				line_number+=1
				data_matrix.append(val)
			else:
				if type(val)!=tuple:
					hdu.header[key]= val 
				else:
					val= tuple(map(lambda x: ' '.join(x),' '.join(val).split(';')))
					hdu.header[key]= val
		#Saving the hdu:
		array= numpy.asarray(data_matrix)
		hdu.data= array
		hdus.append(hdu)
	output_file= open(filename,"w")
	final= fits.HDUList()
	for hdu in hdus:
		final.append(hdu)
	final.writeto(output_file)
	output_file.close()

if __name__=="__main__":
	dictionary_list= get_files_data(["test/000006+2553.2"])
	save_to_fits(dictionary_list,"test/output.fits")
	print "Tests done!"
