# -----------------
# SMNet
# Written by smarsu
# -----------------

"""Reccurent nerual network layer"""

import numpy as np
from ..blob import Tensor, Variable
from .. import layer as nn
from ..ops.param_op import *

class Rnn():
    def __init__(self):
        pass
        self.act_map = {
            'relu': nn.relu,
            'tanh': nn.tanh,
        }

    
    def __call__(self, inputs, state, hidden_size=None, input_size=None, act='tanh'):
        """
        Args:
            inputs: List of Tensor(), e.g. [Tensor(), ..., Tensor()]
                Every times input of RNN.
            state: The initial state of RNN, in default, it should be zeros.
            hidden_size: The hidden units size of RNN.
        Returns:
            outputs:
            states:
        """
        assert len(inputs) >= 1, 'you must need inputs, inputs length is {}'.format(len(inputs))
        weight = Variable(data=np.random.uniform(-0.01, 0.01, (hidden_size + input_size, hidden_size)))  # TODO(smarsu): Another init way
        bias = Variable(data=np.zeros((hidden_size, )))
        outputs = []
        states = []
        for inp in inputs:
            output, state = self.op(inp, state, weight, bias)
            outputs.append(output)
            states.append(state)
        return outputs, states


    def op(self, inp, state, weight, bias):
        """TODO(smarsu): Add bias to matmul"""
        data_x = nn.concat([inp, state], axis=-1)
        data_y = nn.add(nn.matmul(data_x, weight), bias)
        data_y = nn.tanh(data_y)
        return data_y, data_y  # Note: Did here need duplicate?


rnn = Rnn()


class Lstm():
    def __init__(self):
        pass

    
    def __call__(self, inputs, state, hidden_size=None, input_size=None, forget_bias=1.):
        """TODO(smarsu): One matmul; initializers.glorot_uniform()
        """
        assert len(inputs) >= 1, 'you must need inputs, inputs length is {}'.format(len(inputs))
        glorot_data = glorot_uniform((hidden_size + input_size, hidden_size * 4))
        
        w1 = Variable(data=glorot_data[:, :hidden_size])
        b1 = Variable(data=np.zeros((hidden_size, )))

        w2 = Variable(data=glorot_data[:, hidden_size: hidden_size * 2])
        b2 = Variable(data=np.zeros((hidden_size, )))

        w3 = Variable(data=glorot_data[:, hidden_size * 2: hidden_size * 3])
        b3 = Variable(data=np.zeros((hidden_size, )))

        w4 = Variable(data=glorot_data[:, hidden_size * 3: hidden_size * 4])
        b4 = Variable(data=np.zeros((hidden_size, )))
        outputs = []
        states = []
        for inp in inputs:
            output, state = self.op(inp, state, w1, b1, w2, b2, w3, b3, w4, b4, forget_bias)
            outputs.append(output)
            states.append(state)
        return outputs, states

    
    def op(self, inp, state, w1, b1, w2, b2, w3, b3, w4, b4, forget_bias):
        c, h = state
        data_x = nn.concat([inp, h], -1)

        # i, j, f, o
        i = nn.sigmoid(nn.add(nn.matmul(data_x, w1), b1))
        j = nn.tanh(nn.add(nn.matmul(data_x, w2), b2))
        f = nn.add(nn.matmul(data_x, w3), b3)
        o = nn.sigmoid(nn.add(nn.matmul(data_x, w4), b4))

        #f = nn.add(nn.matmul(data_x, w1), b1)
        #i = nn.sigmoid(nn.add(nn.matmul(data_x, w2), b2))
        #j = nn.tanh(nn.add(nn.matmul(data_x, w3), b3))
        #o = nn.sigmoid(nn.add(nn.matmul(data_x, w4), b4))
        forget_bias = Tensor(data=np.full(f.shape, forget_bias))
        f = nn.sigmoid(nn.add(f, forget_bias))
        new_c = nn.add(
            nn.multiply(c, f),
            nn.multiply(i, j),
        )
        new_h = nn.multiply(o, nn.tanh(new_c))
        return new_h, (new_c, new_h)


lstm = Lstm()
