import numpy as np

def SaveRecarray(Arr,Fname):
	'''
	Thie function will save the data from a numpy.recarray to a binary
	file.
	
	Inputs:
		Arr: numpy.recarray to save
		Fname: string containing the path and file name of the resulting
			binary file.
	'''
	
	N = np.int32(Arr.size)
	f = open(Fname,'wb')
	N.tofile(f)
	Dnames = Arr.dtype.names
	Nn = np.size(Dnames)
	for i in range(0,Nn):
		Arr[Dnames[i]].tofile(f)
	f.close()
