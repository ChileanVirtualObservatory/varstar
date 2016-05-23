import varstarscan as vss

from os import listdir
from random import choice
import numpy as np

def read_random_asas_test(minlen=20):
    while 1:
        #Pick a random file to get data from it.
        filename= choice(listdir("data"))
        fil= open("data/"+filename)
        reading= False
        datasets= []
        for lin in fil:
            if not reading:
                if lin[:9]=="#     HJD":
                    reading= True
                    datasets.append([])
            else:
                if lin[0]=="#":
                    reading=False
                else:
                    valid_line= list(filter(lambda x: x!='',lin.strip().split(' ')))
                    tim= float(valid_line[0])
                    lum= float(valid_line[1])
                    grade= valid_line[11]
                    if lum<=29.9 and (grade=='A' or grade=='B'):
                        datasets[-1].append((tim,lum))
        fil.close()
        if len(datasets)>0:
            final= choice(datasets)
            if len(final)>=minlen:
                break
    return final

def main():
    data= read_random_asas_test()
    fitting= vss.fit(data)
    vss.plot(data)

if __name__=="__main__":
    main()
