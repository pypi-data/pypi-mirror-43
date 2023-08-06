# -----------------
# SMNet
# Written by smarsu
# -----------------

"""Helper for RNN"""

import numpy as np
from ..blob import Tensor, Variable
from .. import layer as nn


class Embedding_lookup():
    def __init__(self):
        pass

    
    def __call__(self, idxs, weight):
        """Look up @weight at @idx with axis 1.

        Embedding_lookup will auto pad zeros.
        
        Args:
            idx: [Tensor(), ...], Tensro shape like: [batch, num_voca]
            weight: Tensor(), embedding weight shape like: [num_voca, feature]
        """
        #length = len(idxs)
        #index = nn.concat(idxs, axis=0, stop_grad=True)

        num_voca, feature = weight.shape
        pad = Tensor(data=np.zeros([1, feature]))
        weight = nn.concat([weight, pad], axis=0)

        res = [nn.matmul(index, weight) for index in idxs]
        #res = nn.slice(res, length)

        return res


embedding_lookup = Embedding_lookup()
