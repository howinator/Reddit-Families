import numpy as np
import matplotlib.pyplot as plt

def alt_min(R,l,T=30,k=10):
    u,m = np.shape(R)
    U = np.random.randint(50,size = (u,k))
    M = np.zeros((m,k))
    for t in xrange(30):
        for j in xrange(m):
            x = np.nonzero(R[:,j])[0]
            U_j = U[x,:]
            M[j,:] = np.dot(np.linalg.inv(np.dot(U_j.transpose(),U_j)
                               +l*np.identity(k)),
                               np.dot(U_j.transpose(),R[x,j]))

        for i in xrange(u):
            y = np.nonzero(R[i,:])[0]
            M_i = M[y,:]
            U[i,:] = np.dot(np.linalg.inv(np.dot(M_i.transpose(),M_i)
                               +l*np.identity(k)),
                               np.dot(M_i.transpose(),R[i,y]))

    return np.dot(U,M.transpose())


R = np.load('Ratings.npy')
cvset = np.load('cvset.npy')
Lambda = .05*np.array(range(1,21))
RMSE = np.zeros((len(cvset),len(Lambda)))
for i in xrange(len(cvset)):
    print 'cross-validation set', i
    TrR = np.array(R)
    a,b = np.shape(TrR)
    ind = np.unravel_index(cvset[i],(a,b))
    TrR[ind[0],ind[1]] = 0
    for l in xrange(len(Lambda)):
        print 'lambda =', l
        pred = alt_min(TrR,Lambda[l])
        RMSE[i,l] = np.sqrt(np.sum(
                    np.square(pred[ind[0],ind[1]]-R[ind[0],ind[1]])))


mean_RMSE = np.mean(RMSE, axis = 0)

plt.plot(Lambda, mean_RMSE)
plt.show()
plt.savefig('RMSE_plot.png')
















