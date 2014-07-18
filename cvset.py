import numpy as np
from sklearn import cross_validation

R = np.load('Ratings.npy')
print R
m,n = np.shape(R)
known = np.nonzero(R)
num_obs = len(known[0])
print num_obs
k = 10

kf = cross_validation.KFold(n=num_obs,n_folds=k)
cvset = []
for train, test in kf:
    cvset.append(test)


np.save('cvset.npy',np.array(cvset))
#for train, test in kf:
#    print train, test
