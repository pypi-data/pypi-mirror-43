'''
    TTT utility functions
    
    Tim Molteno. tim@elec.ac.nz
'''

import numpy as np

def min_rank(diagonal, eps):
    # Truncation by absolute precision in the Frobenius 
    # norm. Finds minimal possible R such that :math:`\sqrt(sum(SV(R:n)^2)) < EPS`
    # The diagonal are the singular values in descending order.

    s_norm = np.sqrt(np.sum(diagonal**2))   
    # S is diagonal so the frobenius norm is trace(A*A) 
    # s_norm = np.linalg.norm(np.diag(s), 'fro')
    #print("s_norm = {}".format(s_norm))
    
    if s_norm*eps == 0.0:
        return 1

    sv0 = np.cumsum(diagonal[::-1]**2)[::-1]

    threshold = (eps*s_norm)**2
    
    loc = np.where(sv0 < threshold)[0]
    if 0 == len(loc):
        return diagonal.size
    
    return loc[0]


def reconstruct_svd(u, s, vh):
    return np.matmul(u, np.matmul(np.diag(s), vh))

def print_svd(u, s, vh):
    '''
        Simple helper function to print out an svd
    '''
    print("SVD = [{}]x[{}]x[{}]".format(u.shape, np.diag(s).shape, vh.shape))
    print(u)
    print(np.diag(s))
    print(vh)
    print(reconstruct_svd(u, s, vh))


def truncated_svd(A, eps):
    """
        Generate a simple truncated SVD approximation :math:`B`
        to a matrix :math:`A`. Where the Frobenius norm 
        :math:`\\frac{|(B - A)|}{|A|} < eps`
        
    """
    u, s, vh = np.linalg.svd(A, full_matrices=False)
    #print_svd(u, s, vh)
    
    r1 = min_rank(s, eps);
    #print("min_rank = {}".format(r1))
    
    u_trunc = u[:, 0:r1]
    s_trunc = s[0:r1]
    vh_trunc = vh[0:r1, :]
    return u_trunc, s_trunc, vh_trunc, r1


if __name__=="__main__":
    diagonal = np.array([9,8,7,6,5,4,3,2,1,0])
    min_rank(diagonal, 5.0)
    
    a = np.random.randn(4, 6) # + 1j*np.random.randn(4, 6)
    print(a)
    
    ut, st, vht, r1 = truncated_svd(a, 2e-1)
    print_svd(ut, st, vht)
    #print("Truncated SVD = [{}]x[{}]x[{}]".format(ut.shape, st.shape, vht.shape))
    #print ut
    #print np.diag(st)
    #print vh
    #print np.dot(ut, np.dot(np.diag(st), vht))
