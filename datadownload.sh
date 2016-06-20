#!/bin/bash

echo "Downloading data from ASAS..."

cd data
rm -rf *
for file in {0..23}; do
	printf -v file "%02d" $file
	wget http://www.astrouw.edu.pl/asas/data/$file.tgz
	tar -xvf $file.tgz
	mv $file/* .
	rmdir $file
	rm $file.tgz
done
for filename in *; do
	echo "$filename"
	cd ..
	python3 -c "import varstarscan as vss; filename= \"$filename\"; data= vss.get_file_data(\"data/\"+filename); vss.save_to_fits(data,\"fits/\"+filename+\".fits\");"
	cd data
done

