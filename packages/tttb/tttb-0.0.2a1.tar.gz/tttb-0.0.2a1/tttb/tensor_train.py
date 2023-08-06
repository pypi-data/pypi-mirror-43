'''
    TTT TensorTrain subclass for Tensor Train Approximations
    
    [1] I. V. Oseledets. "Tensor-Train Decomposition" SIAM J. Sci. Comput., 33(5), 2295–2317. https://doi.org/10.1137/090752286

    Tim Molteno. tim@elec.ac.nz
'''

import logging
import numpy as np

from tttb.tensor import BaseTensor
from tttb.tensor import Tensor
from tttb.util import truncated_svd, print_svd

class TensorTrain(BaseTensor):
    """
        Tensor Train Approximation:
        
        In d-dimesions a tensor of shape :math:`[n1, n2, n3, ... nd]`
        
        Represent an array as the matrix product of d cores :math:`G_k (k \in [1..d])`
        each element of the tensor is represented as a product of cores...
        
        :math:`A(i_1, ... i_d) = G_1(i_1) * G_2(i_2) * ... * G_d(i_d)`
        
        each core is a 3D array where :math:`G_k` is  :math:`r_{k-1} \\times n_k \\times r_k` in size.
        
        where :math:`G_1 \\sim 1 \\times n_1 \\times r_1`
              :math:`G_d \\sim r_d \\times n_d \\times 1`
    """
    
    def __init__(self, shape):
        BaseTensor.__init__(self, shape)
        self._cores = []  # List of the cores
        self.r = []  # List of the core shapes [r_0 ... r_d]
    
    def __repr__(self):
        ret = "TensorTrain d={} lr={}:\n".format(self.d, self.r)
        for k in range(1, self.d+1):
            c = self.get_core(k)
            if c is None:
                ret += "  core {} {}\n".format(k, None)
            else:
                ret += "  core {} {}\n".format(k, self.get_core(k).shape)
            
        ret += "Storage: {}".format(self.get_storage())
        return ret

    def get_storage(self):
        ret = 0
        for k in range(1, self.d+1):
            ret += self.get_core(k).size
        return ret
    
    def get_core(self, k):
        assert(k >= 1)
        assert(k <= self.d)
        return self._cores[k-1]
    
    def set_core(self, k, c):
        assert(k >= 1)
        assert(k <= self.d)
        logging.debug("core.shape = {}".format(c.shape))

        self._cores[k-1] = c
    
    @classmethod
    def from_tensor(self, a, eps=1e-14):
        """
            Construct from another tensor. Accurate to eps. This performs the tt_svd algorithm
            if the parameter a is a Tensor object.
        """
        if isinstance(a, TensorTrain):
            # copy from tensor
            ret = TensorTrain(a.shape())
    
            raise NotImplementedError("Constructing from an existing TT not implemented yet")
            return ret
        
        if isinstance(a, Tensor):
            ret = TensorTrain(a.shape())
        
            ret.tt_svd(a, eps)
            
        return ret


    def tt_svd(self, a, eps):
        """
            TT-SVD Algorithm 1 from Oseledetes
        """
        if not isinstance(a, Tensor):
            raise ValueError("Input Tensor A must be array-backed")
        
        logging.debug("tt_svd: a = {}".format(a))
        delta = eps / (np.sqrt(self.d - 1))
        
        C = a.data
        self.r = [1]*(self.d + 1)
        self._cores = [None]*self.d
        
        for k in range(1,self.d):
            n_k = self._shape[k-1]
            m = n_k*self.r[k-1]
            logging.debug("m = {}".format(m))
            logging.debug("C.size = {}".format(C.size))
            logging.debug("C.shape = {}".format(C.shape))
            logging.debug("self.r[k-1] = {}".format(self.r[k-1]))
            C = C.reshape(m, int(C.size / m))
            logging.debug("C.shape = {}".format(C.shape))
            u, s, vh, r1 = truncated_svd(C, delta)
            #print_svd(u, s, vh)
            self.r[k] = r1
            
            G_k = u.reshape((self.r[k-1], n_k, self.r[k],))

            self.set_core(k, G_k)
            
            C = np.matmul(np.diag(s), vh)
            
        k = self.d
        n_k = self._shape[k-1]
        G_d  = C.reshape((self.r[k-1], n_k, self.r[k],))
        self.set_core(self.d, G_d)
        
        
    def g(self, k, i):
        """
            Get the k-th core, with index i, i.e., :math:`G_k(i)`
        """
        logging.debug("g({},{})".format(k,i))
        return self.get_core(k)[:,i,:]

    

    def __getitem__(self, indices):
        """
            Indexing retrieves an item from a TT object. This is
            a little expensive as it requires a summation (eqn 1.3)
        """
        logging.debug("_tt[{}]".format(indices))
        assert(len(indices) == self.d)
        ret = self.g(1, indices[0])
        for k in range(2, self.d+1):
            ret = np.matmul(ret,self.g(k, indices[k-1]))
        return ret[0][0]
    
    @classmethod
    def from_canonical(self, a):
        """
            From canonical form to TT. Assumes the canonical form is a sum
            
            :math:`i_1, ..., i_d) = \sum_{\\alpha} U_1(i_1, \\alpha)@U_2(i_1, \\alpha) ... U_d(i_d, \\alpha)`
        """
        pass
    
    def round(self, eps):
        """
            Round the TT (assumed to have sub-optimal ranks :math:`r_k`
            to eps. This is really the same as performing a TT-SVD 
            on a tensor that is already in the TT form.
            
            Concepts required:
            
                - unfolding matrix
                - QR decomposition
                - 
            
            This is Algorithm 2 from Oseledetes
        """
        new_cores = []
        delta = eps / (np.sqrt(self.d - 1))
        # Right-left orthogonalization
        for k in range(d, 2, -1):
            G_k = self.get_core(k)
            q, r = qr_rows(G_k)
        
        
        # Compression of orthogonalised representation
        
        pass
        
