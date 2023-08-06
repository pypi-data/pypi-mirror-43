# Tensor Train Toolbox

This is a pure python library that handles Tensor Train decomposition of tensors. This library. The module contains two main classes Tensor, and TensorTrain. Both of these inherit from an abstract base class BaseTensor that provides a common API. 

Author: Tim Molteno tim@elec.ac.nz. Elec Research Group, Department of Physics. University of Otago.

## The Tensor Class

This class is a wrapper around a numpy ndarray.

## The TensorTrain Class


This class is a Tensor Train Decomposition of a tensor (see reference [1])/ The magic property of these decompositions is that their storage requirements and their computation requirements to not scale exponentially with the tensor dimension N. Thus for high-dimensional or very find grids, TensorTrain decompositions of tensors are far more efficient. 

The tradeoff is accuracy. Creating a TT representation of a tensor does not preserve perfect accruacy for high rank tensors. 

Will have a class Heirarchy so that Tensors are a class, and TensorTrain is a subclass.


## References

[1] I. V. Oseledets. "Tensor-Train Decomposition" SIAM J. Sci. Comput., 33(5), 2295–2317. https://doi.org/10.1137/090752286
