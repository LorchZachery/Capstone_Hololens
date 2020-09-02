import numpy as np
a = np.array([[1,2,3,4,5],
					[6,7,8,9,10],
					[12,13,14,15,16]])
array = np.pad(a, [(0,4),(0,4)], 'constant', constant_values=(0))

print(array)
col = array.shape[0]
row = array.shape[1]

ar_del = np.delete(array, 0, 0)
print(ar_del)
ra_del = np.delete(ar_del, 0,1)
print(ra_del)