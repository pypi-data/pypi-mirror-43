'''
    TTT Tensor base classes
    
    Tim Molteno. tim@elec.ac.nz
    
    These classes allow a heirarchical representation of tensors. The BaseTensor is an abstract base class that defines the methods that are available in various subclasses.
    
    This structure is useful for testing because we define a Tensor class that is backed by an actual multidimensional grid of numbers, and then use standard routines on this class to test the :py:class:`tttb.tensor_train.TensorTrain` subclass.
'''

import logging
import numpy as np

class BaseTensor:
    """
        Base class of a Tensor (in this case a multidimensional grid rather than a Bilinear form)
        
    """
    
    def __init__(self, shape):
        assert(isinstance(shape, list))
        self._shape = shape
        self.d = len(shape)
    
    
    def shape(self):
        return self._shape
    
    def __getitem__(self, indices):
        raise NotImplementedError("get() Must be overridden in a derived class of BaseTensor")
    


class Tensor(BaseTensor):
    """
        A Tensor backed by a grid of actual numbers. This will fail miserably to store large high dimensional objects, however is very useful for testing.
    """
    
    def __init__(self, shape):
        BaseTensor.__init__(self, shape)
        self.data = None

    def __repr__(self):
        return "Tensor shape={}".format(self.shape())
    

    @classmethod
    def from_ndarray(self, a):
        """
            Construct a Tensor object from a numpy n-dimensional array of numbers.
        """
        assert(isinstance(a, np.ndarray))
        ret = Tensor(list(a.shape))
        ret.data = a
        return ret
    
    
    def __getitem__(self, indices):
        '''
            Accessor method to retrieve an element of the Tensor
        '''
        logging.debug("tensor[{}]".format(indices))
        assert(len(indices) == self.d)
        return self.data.__getitem__(tuple(indices))
    
