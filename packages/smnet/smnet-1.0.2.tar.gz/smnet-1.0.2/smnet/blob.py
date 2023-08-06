# -----------------
# SMNet Blob
# Written by smarsu
# -----------------

import numpy as np
from .net import sm


class Blob(object):
    _name_id = 0

    def __init__(self, data=None, shape=None, dtype=np.float32, name='blob'):
        self._data = None
        self._shape = None
        self._grad = 0

        self._dtype = dtype

        if shape is not None:
            self._set_shape(shape)
        if data is not None:
            self.feed(data)

        self._name = self._get_name(name)


    def _get_name(self, name):
        Blob._name_id += 1
        return '_'.join([name, str(Blob._name_id)])


    def _set_shape(self, shape):
        self._shape = shape

    
    def feed(self, v):
        self._data = np.array(v, dtype=self._dtype)
        # If the data is a scalar, then its shape needs to be set to [1].
        if not self._data.shape:
            self._data = np.reshape(self._data, [-1])

        # The shape of the blob changes with its data.
        self._set_shape(self._data.shape)


    def add_grad(self, grad):
        self._grad += grad
        return self.grad


    def clear_grad(self):
        self._grad = 0
    

    # ----------------------------------------------------------------------
    # Attributes
    #

    @property
    def shape(self):
        return self._shape

    
    @property
    def data(self):
        return self._data

    
    @property
    def grad(self):
        return self._grad

    
    @property
    def name(self):
        return self._name

    
    def __str__(self):
        return self.name

    
    def __repr__(self):
        return self.__str__()

    # ----------------------------------------------------------------------

    # ----------------------------------------------------------------------
    # Overloaded operator
    #
    # TODO(smarsu): Fix the problem of `cross import`.
    #

    # Arithmetic operation

    def __add__(self, v):
        from .layer import add
        return add(self, v)

    
    def __sub__(self, v):
        from .layer import subtract
        return subtract(self, v)

    
    def __mul__(self, v):
        from .layer import multiply
        return multiply(self, v)

    
    def __truediv__(self, v):
        from .layer import divide
        return divide(self, v)
    
    # Unary operator

    def __pos__(self):
        return self
    

    def __neg__(self):
        from .layer import subtract
        return subtract(Tensor(0), self)

    # ----------------------------------------------------------------------


class Variable(Blob):
    def __init__(self, data=None, shape=None, name='Variable', dtype=np.float32):
        """
        Attention: In theory, our Variable must have initialized values, 
                    we will not provide initialization at the network level.
        """
        assert not(data is None and shape is None), 'Variable: data and shape can not both be None'
        super(Variable, self).__init__(data, shape, dtype=dtype, name=name)
        sm.add_variable(self)


    def restore(self, data):
        raise NotImplementedError
        self.feed(data)


    def update(self, lr=1):
        self._data -= self._grad


class Tensor(Blob):
    def __init__(self, data=None, shape=None, name='Tensor',  dtype=np.float32):
        super(Tensor, self).__init__(data, shape, dtype=dtype, name=name)
        sm.add_tensor(self)


    def set_grad(self, grad):
        self._grad = grad
