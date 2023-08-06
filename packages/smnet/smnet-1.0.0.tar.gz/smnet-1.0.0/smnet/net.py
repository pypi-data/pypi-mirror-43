# -----------------
# SMNet Network
# Written by smarsu
# -----------------

import numpy as np
from .ops import array_op


def Singleton(cls, _instance={}):
    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]
    return _singleton


@Singleton
class Net(object):
    """
    SMNet can only built one graph at a time
    TODO(smarsu): Built multi-graph.
    """

    def __init__(self):
        self._layers = []
        self._backlayers = []

        self._variable = set()
        self._tensor = set()

        self._variable_momentum = {}


    def add_layer(self, layer):
        self._layers.append(layer)
        self._backlayers.insert(0, layer)

    
    def add_tensor(self, v):
        self._tensor.add(v)

    
    def add_variable(self, v):
        self._variable.add(v)


    def _set_feed_dict(self, feed_dict):
        for k, v in feed_dict.items():
            k.feed(v)


    def forward(self, feed_dict=None):
        if feed_dict is None: feed_dict = {}
        self._set_feed_dict(feed_dict)

        for layer in self._layers:
            layer.forward()


    def backward(self, blobs, lr=1., momentum=0., weight_decay=0.):
        """
        TODO(smarsu): Check out why momentum affect the converge. 
        """
        grad = lr
        for blob in blobs:
            blob.set_grad(np.full(blob.shape, grad))

        for layer in self._backlayers:
            if not layer.stop_grad:
                layer.backward()

        self._momentum_update(momentum)
        self._weight_norm(weight_decay)


    def _momentum_update(self, momentum):
        """Reference: https://arxiv.org/abs/1706.02677v1
        
        Ut+1 = m * Ut + grad
        Wt+1 = Wt - lr * Ut+1
        """
        for v in self._variable:
            self._variable_momentum[v] = v.add_grad(momentum * self._variable_momentum.get(v, 0))
        
    
    def _weight_norm(self, weight_decay):
        for v in self._variable:
            v.add_grad(weight_decay * array_op.l2_loss(v.data))

    
    def update(self):
        for v in self._variable:
            v.update()
        
        for v in self._variable:
            v.clear_grad()

        for v in self._tensor:
            v.clear_grad()


    def optimize(self, blobs, lr=1., momentum=0., weight_decay=0.):
        self.backward(blobs, lr, momentum, weight_decay)
        self.update()


sm = Net()
