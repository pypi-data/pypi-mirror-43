import numpy as np

def ReadRecarray(Fname,dtype):
	'''
	Reads binary file into np.recarray object
	
	Args:
		Fname:	Full path and file name of binary file to be read.
		dtype:	list of data types (and optionally shapes) stored in Fname.
				e.g.:
					dtype = [('Date','int32'),('ut','float32'),('x','float64',(10,))]
	
	Returns:
		np.recarray object
	
	'''
	f = open(Fname,'rb')
	N = np.fromfile(f,dtype='int32',count=1)
	data = np.recarray(N,dtype=dtype)
	Nd = len(dtype)
	for i in range(0,Nd):
		if len(dtype[i]) == 2:
			Ne = np.array(N)
			shape = (Ne[0],)
		else:
			s = dtype[i][2] 
			Ns = len(s)
			Ne = np.array(N)
			shape = (N[0],)
			for j in range(0,Ns):
				Ne *= s[j]
				shape += (s[j],)
		if len(shape) == 1:
			data[dtype[i][0]] = np.fromfile(f,dtype=dtype[i][1],count=Ne[0])
		else:
			tmp = np.fromfile(f,dtype=dtype[i][1],count=Ne[0])	
			data[dtype[i][0]] = tmp.reshape(shape)
			
	f.close()
	return data
	
