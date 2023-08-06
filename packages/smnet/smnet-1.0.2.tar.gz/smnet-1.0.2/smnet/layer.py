# -----------------
# SMNet Layer
# Written by smarsu
# -----------------

"""
Some useful neural network layers.
"""

import logging
import numpy as np

from .blob import Tensor
from .ops import array_op
from .net import sm


class Layer(object):
    """Network is stacked by layers.
    
    If we want to customize layers, we need to implement the following three functions:

    _prebuilt(self, a, b, ...):
        Prepare for the computation of this layer.

    forward(self):
        Layer operate, compute output by input.

    backward(self):
        Optimizer operate, compute the gradient of the current layer by the gradient of the top layer.
    """

    _name_id = 0

    def __init__(self, stop_grad=False, name='Layer'):
        sm.add_layer(self)
        
        self.stop_grad = stop_grad
        self._name = self._get_name(name)


    def _get_name(self, name):
        Layer._name_id += 1
        return '_'.join([name, str(Layer._name_id)])


class Matmul(Layer):
    """TODO(samrsu): Merge bias to FullConnect"""

    def __init__(self, a, b):
        super(Matmul, self).__init__()
        self._prebuilt(a, b)


    def _prebuilt(self, a, b):
        self.a = a
        self.b = b
        self.res = Tensor()

    
    def forward(self):
        # 1. Prepare input data
        a = self.a.data
        b = self.b.data

        # 2. Compute and feed result
        self.res.feed(np.matmul(a, b))


    def backward(self):
        grad = self.res.grad
        self._compute_grad_a(grad)
        self._compute_grad_b(grad)


    def _compute_grad_a(self, grad):
        """
        a_grad = res_grad * b.T
        """
        # 1. Prepare data
        b = self.b.data

        # 2. Compute and add grad
        self.a.add_grad(np.matmul(grad, b.T))


    def _compute_grad_b(self, grad):
        """
        b_grad = a.T * grad
        TODO(smarsu): Understand it.
        """
        # 1. Prepare data
        a = self.a.data

        # 2. Compute and add grad
        self.b.add_grad(np.matmul(a.T, grad))


def matmul(a, b):
    return Matmul(a, b).res


class Add(Layer):
    def __init__(self, a, b):
        super(Add, self).__init__()
        self._prebuilt(a, b)
    

    def _prebuilt(self, a, b):
        self.a = a
        self.b = b
        self.res = Tensor()

    
    def forward(self):
        # 1. Prepare input data
        a = self.a.data
        b = self.b.data

        # 2. Compute and feed result
        self.res.feed(a + b)

    
    def backward(self):
        grad = self.res.grad
        self._compute_grad_a(grad)
        self._compute_grad_b(grad)


    def _compute_grad_a(self, grad):
        """For the NHWC data format, bias should collect gradients in the same way."""
        # 1. Prepare grad
        if grad.shape != self.a.shape:
            grad = np.reshape(grad, [-1] + list(self.a.shape))
            grad = np.sum(grad, axis=0)

        # 2. Add grad
        self.a.add_grad(grad)

    
    def _compute_grad_b(self, grad):
        # 1. Prepare grad
        if grad.shape != self.b.shape:
            grad = np.reshape(grad, [-1] + list(self.b.shape))
            grad = np.sum(grad, axis=0)

        # 2. Add grad
        self.b.add_grad(grad)


def add(a, b):
    return Add(a, b).res


class Subtract(Layer):
    def __init__(self, a, b):
        super(Subtract, self).__init__()
        self._prebuilt(a, b)
    

    def _prebuilt(self, a, b):
        self.a = a
        self.b = b
        self.res = Tensor()

    
    def forward(self):
        # 1. Prepare input data
        a = self.a.data
        b = self.b.data

        # 2. Compute and feed result
        self.res.feed(a - b)

    
    def backward(self):
        grad = self.res.grad
        self._compute_grad_a(grad)
        self._compute_grad_b(grad)


    def _compute_grad_a(self, grad):
        """For the NHWC data format, bias should collect gradients in the same way."""
        # 1. Prepare grad
        if grad.shape != self.a.shape:
            dim_c = self.a.shape[-1]
            grad = np.reshape(grad, [-1] + list(self.a.shape))
            grad = np.sum(grad, axis=0)

        # 2. Add grad
        self.a.add_grad(grad)

    
    def _compute_grad_b(self, grad):
        # 1. Prepare grad
        grad = -grad
        if grad.shape != self.b.shape:
            grad = np.reshape(grad, [-1] + list(self.b.shape))
            grad = np.sum(grad, axis=0)

        # 2. Add grad
        self.b.add_grad(grad)

    
def subtract(a, b):
    return Subtract(a, b).res


class Multiply(Layer):
    def __init__(self, a, b):
        super(Multiply, self).__init__()
        self._prebuilt(a, b)

    
    def _prebuilt(self, a, b):
        self.a = a
        self.b = b
        self.res = Tensor()

    
    def forward(self):
        # 1. Prepare data
        a = self.a.data
        b = self.b.data

        # 2. Compute and feed result
        self.res.feed(a * b)
    

    def backward(self):
        grad = self.res.grad
        self._compute_grad_a(grad)
        self._compute_grad_b(grad)


    def _compute_grad_a(self, grad):
        # 1. Prepare data
        b = self.b.data

        # 2. Compute grad
        grad = grad * b
        if grad.shape != self.a.shape:
            grad = np.reshape(grad, [-1] + list(self.a.shape))
            grad = np.sum(grad, axis=0)

        # 3. Add grad
        self.a.add_grad(grad)
    

    def _compute_grad_b(self, grad):
        # 1. Prepare data
        a = self.a.data

        # 2. Compute and feed result
        grad = grad * a
        if grad.shape != self.b.shape:
            grad = np.reshape(grad, [-1] + list(self.b.shape))
            grad = np.sum(grad, axis=0)

        # 3. Add grad
        self.b.add_grad(grad)


def multiply(a, b):
    return Multiply(a, b).res


class Divide(Layer):
    def __init__(self, a, b):
        super(Divide, self).__init__()
        self._prebuilt(a, b)

    
    def _prebuilt(self, a, b):
        self.a = a
        self.b = b
        self.res = Tensor()

    
    def forward(self):
        # 1. Prepare data
        a = self.a.data
        b = self.b.data

        # 2. Compute and feed result
        self.res.feed(a / b)
    

    def backward(self):
        grad = self.res.grad
        self._compute_grad_a(grad)
        self._compute_grad_b(grad)

    
    def _compute_grad_a(self, grad):
        # 1. Prepare data
        b = self.b.data

        # 2. Compute grad
        grad = grad / b
        if grad.shape != self.a.shape:
            grad = np.reshape(grad, [-1] + list(self.a.shape))
            grad = np.sum(grad, axis=0)

        # 3. Add grad
        self.a.add_grad(grad)
    

    def _compute_grad_b(self, grad):
        # 1. Prepare data
        a = self.a.data
        b = self.b.data

        # 2. Compute grad
        grad = grad * a / (-b * b)
        if grad.shape != self.b.shape:
            grad = np.reshape(grad, [-1] + list(self.b.shape))
            grad = np.sum(grad, axis=0)

        # 3. Add grad
        self.b.add_grad(grad)


def divide(a, b):
    return Divide(a, b).res


class Sigmoid(Layer):
    def __init__(self, a):
        super(Sigmoid, self).__init__()
        self._prebuilt(a)

    
    def _prebuilt(self, a):
        self.a = a
        self.res = Tensor()

    
    def forward(self):
        """Shall we add limit here to avoid overflow?"""
        # 1. Prepare data
        a = self.a.data

        # 2. Compute and feed result
        self.res.feed(array_op.sigmoid(a))
    

    def backward(self):
        grad = self.res.grad
        self._compute_grad_a(grad)


    def _compute_grad_a(self, grad):
        # 1. Prepare data
        res = self.res.data

        # 2. Compute grad
        grad = grad * res * (1 - res)

        # 3. Add grad
        self.a.add_grad(grad)


def sigmoid(a):
    return Sigmoid(a).res


class Relu(Layer):
    def __init__(self, a):
        super(Relu, self).__init__()
        self._prebuilt(a)

    
    def _prebuilt(self, a):
        self.a = a
        self.res = Tensor()

    
    def forward(self):
        # 1. Prepare data
        a = self.a.data

        # 2. Compute and feed result
        self.res.feed(np.maximum(0, a))

    
    def backward(self):
        grad = self.res.grad
        self._compute_grad_a(grad)

    
    def _compute_grad_a(self, grad):
        # 1. Prepare data
        a = self.a.data

        # 2. Compute grad
        grad = np.where(a > 0, grad, 0)
        
        # 3. Add grad
        self.a.add_grad(grad)


def relu(a):
    return Relu(a).res


class Tanh(Layer):
    def __init__(self, a):
        super(Tanh, self).__init__()
        self._prebuilt(a)

    
    def _prebuilt(self, a):
        self.a = a
        self.res = Tensor()


    def forward(self):
        # 1. Prepare data
        a = self.a.data

        # 2. Compute and feed result
        self.res.feed(array_op.tanh(a))


    def backward(self):
        grad = self.res.grad
        self._compute_grad_a(grad)


    def _compute_grad_a(self, grad):
        # 1. Prepare data
        res = self.res.data

        # 2. Compute grad
        grad = (1 - np.square(res)) * grad

        # 3. Add grad
        self.a.add_grad(grad)


def tanh(a):
    return Tanh(a).res


class Mse(Layer):
    def __init__(self, a, b):
        super(Mse, self).__init__()
        self._prebuilt(a, b)

    
    def _prebuilt(self, a, b):
        logging.warning('sm.nn.mse actually calculates L2_loss instead of MSE.')

        self.a = a
        self.b = b
        self.res = Tensor()

    
    def forward(self):
        # 1. Prepare data
        a = self.a.data
        b = self.b.data

        # 2. Compute and feed result
        self.res.feed(0.5 * np.square(a - b))


    def backward(self):
        grad = self.res.grad
        self._compute_grad_a(grad)
        self._compute_grad_b(grad)

    
    def _compute_grad_a(self, grad):
        # 1. Prepare data
        a = self.a.data
        b = self.b.data

        # 2. Compute grad
        grad = (a - b) * grad

        # 3. Add grad
        self.a.add_grad(grad)

    
    def _compute_grad_b(self, grad):
        # 1. Prepare data
        a = self.a.data
        b = self.b.data

        # 2. Compute grad
        grad = (b - a) * grad

        # 3. Add grad
        self.b.add_grad(grad)


def mse(a, b):
    return Mse(a, b).res


class Concat(Layer):
    def __init__(self, values, axis):
        super(Concat, self).__init__()
        self._prebuilt(values, axis)

    
    def _prebuilt(self, values, axis):
        self.values = values
        self.axis = axis
        self.res = Tensor()
    

    def forward(self):
        # 1. Prepare data
        values = [v.data for v in self.values]
        axis = self.axis

        # 2. Compute and feed result
        self.res.feed(np.concatenate(values, axis))


    def backward(self):
        grad = self.res.grad
        self._compute_grad_values(grad)
        

    def _compute_grad_values(self, grad):
        # 1. Prepare data
        axis = self.axis

        # 2. Compute grad
        split_idx = []
        cur_idx = 0
        for blob in self.values:
            cur_idx += blob.shape[axis]
            split_idx.append(cur_idx)
        grads = np.split(grad, split_idx, axis)
        grads.pop()

        # 3. Add grad
        for value, grad in zip(self.values, grads):
            value.add_grad(grad)


def concat(values, axis):
    return Concat(values, axis).res


class Split(Layer):
    def __init__(self, value, num_or_size_splits, axis):
        super(Slice, self).__init__()
        self._prebuilt(value, num_or_size_splits, axis)

    
    def _prebuilt(self, value, num_or_size_splits, axis):
        self.value = value
        self.num_or_size_splits = num_or_size_splits
        self.axis = axis

        num = num_or_size_splits if isinstance(num_or_size_splits, int) else len(num_or_size_splits)
        self.res = [Tensor() for _ in range(num)]

    
    def forward(self):
        """Splits a tensor into sub tensors.

        ```py
        >>> x = sm.Tensor(range(9))
        >>> sm.nn.split(x, 3)
        [Tensor([ 0.,  1.,  2.]), Tensor([ 3.,  4.,  5.]), Tensor([ 6.,  7.,  8.])]

        >>> x = sm.Tensor(range(8))
        >>> sm.nn.split(x, [3, 5, 6, 10])
        [Tensor([ 0.,  1.,  2.]),
        Tensor([ 3.,  4.]),
        Tensor([ 5.]),
        Tensor([ 6.,  7.]),
        Tensor([], dtype=float64)]
        ```
        
        """
        # 1. Prepare data
        value = self.values
        num_or_size_splits = self.num_or_size_splits
        axis = self.axis

        # 2. Compute result
        dim_length = value.shape[axis]
        size_splits = num_or_size_splits if isinstance(num_or_size_splits, list) else [dim_length // num_or_size_splits for _ in range(num_or_size_splits)]
        sub_values = np.split(value, size_splits, axis)
        sub_values.pop()

        # 3. Feed result
        for res, sub_value in zip(self.res, sub_values):
            res.feed(sub_value)

    
    def backward(self):
        grads = [blob.grad for blob in self.res]
        self._compute_grad_value(grads)


    def _compute_grad_value(self, grads):
        # 1. Prepare data
        axis = self.axis

        # 2. Compute and add grad
        self.value.add_grad(np.concat(grads, axis))


def split(value, num_or_size_splits, axis):
    return Split(value, num_or_size_splits, axis).res


class Embedding_lookup(Layer):
    def __init__(self, params, ids, stop_grad):
        super(Embedding_lookup, self).__init__(stop_grad=stop_grad)
        self._prebuilt(params, ids)

    
    def _prebuilt(self, params, ids):
        """
        sm.nn.embedding_lookup will automatically add a row(all zeros) at the end of params, it represents the pad character.

        Args:
            params: Tensor(), shape like [num_voca, num_feature]
            ids: Tensor(), shape like [batch, time_step] or [batch]
        Returns:
            res: Tensor(), shape like [batch(, time_step), num_feature]
        """

        logging.warning('We have not test this sm.nn.embedding_lookup for forward propagation and backward propagation.')
        logging.warning('You would better stop the grad of sm.nn.embedding_lookup.')

        self.params = params
        self.ids = ids
        self.res = Tensor()

        # Prepare pad data
        params = params.data
        num_voca, num_feature = params.shape
        self.params.feed(np.concatenate([params, np.zeros((1, num_feature))], 0))

    
    def forward(self):
        """Looks up `ids` in a list of embedding tensors.

        The params had been padded
        """
        # 1. Prepare data
        params = self.params.data
        ids = self.ids.data

        # 2. Compute and feed result
        self.res.feed(params[ids])

    
    def backward(self):
        grad = self.res.grad
        self._compute_grad_params(grad)


    def _compute_grad_params(self, grad):
        """TODO(smarsu): Remove loop
        
        grad have shape [batch(, time_step), num_feature]
        ids have shape [batch(, time_step)]
        """
        # 1. Prepare data
        ids = self.ids.data

        # 2. Compute grad
        collect_grad = np.zeros(self.params.shape)
        num_voca, num_feature = self.params.shape
        grad = np.reshape(grad, [-1, num_feature])
        for id, part_grad in zip(ids.flatten(), grad):
            if id >= num_voca: continue  # The weight of the pad will not be updated
            collect_grad[id, :] += part_grad
            #self.params._grad[id, :] += part_grad
        
        # 3. Add grad
        self.params.add_grad(collect_grad)


def embedding_lookup(params, ids, stop_grad=False):
    return Embedding_lookup(params, ids, stop_grad=stop_grad).res


class Softmax(Layer):
    def __init__(self, a):
        super(Softmax, self).__init__()
        self._prebuilt(a)
    

    def _prebuilt(self, a):
        self.a = a
        self.res = Tensor()


    def forward(self):
        # 1. Prepare data
        a = self.a.data

        # 2. Compute and feed result
        self.res.feed(array_op.softmax(a))
    

    def backward(self):
        grad = self.res.grad
        self._compute_grad_a(grad)


    def _compute_grad_a(self, grad):
        raise NotImplementedError


def softmax(a):
    return Softmax(a).res


class Softmax_log_cross_entropy(Layer):
    def __init__(self, labels, logits):
        super(Softmax_log_cross_entropy, self).__init__()
        self._prebuilt(labels, logits)
    

    def _prebuilt(self, labels, logits):
        """
        The dim always be -1
        """

        logging.warning('sm.nn.softmax_log_cross_entropy always calculates the value of the -1 dimension')

        self.labels = labels
        self.logits = logits
        self.res = Tensor()

    
    def forward(self):
        # 1. Prepare data
        labels = self.labels.data
        logits = self.logits.data

        # 2. Compute result
        softmax_logits = array_op.softmax(logits)
        neg_log_logits = -np.log(softmax_logits)
        cross_entropy = np.sum(labels * neg_log_logits, -1)

        self.softmax_logits = softmax_logits
        self.neg_log_logits = neg_log_logits

        # 3. Feed result
        self.res.feed(cross_entropy)

    
    def backward(self):
        grad = self.res.grad
        self._compute_grad_lables(grad)
        self._compute_grad_logits(grad)

    
    def _compute_grad_lables(self, grad):
        """Actually, we need not compute lables grad."""
        # 1. Prepare data
        neg_log_logits = self.neg_log_logits

        # 2. Compute and add grad
        self.labels.add_grad(neg_log_logits * grad)

    
    def _compute_grad_logits(self, grad):
        """
        For grad[..., i], it affect grad[..., :] by the way [a, ..., k - 1, ..., n]
        """
        # 1. Prepare data
        labels = self.labels.data
        softmax_logits = self.softmax_logits

        # 2. Compute and add grad
        for i in range(labels.shape[-1]):
            softmax_logits_i = np.copy(softmax_logits)
            softmax_logits_i[..., i] -= 1
            self.logits._diff += grad[..., i] * labels[..., i] * softmax_logits_i


    def _compute_grad_logits_v2(self, a, b, grad):
        """THIS FUNCTION IS DEPRECATED, use _compute_grad_logits instead"""
        b = b.data

        softmax_a = array_op.softmax(a.data)

        diff = np.zeros(a.shape)

        for i in range(a.shape[-1]):
            _softmax_a = np.copy(softmax_a)
            _softmax_a[..., i:i+1] = _softmax_a[..., i:i+1] - 1
            diff += b[..., i:i+1] * _softmax_a

        # Here grad maybe 1
        diff = diff * grad

        diff = np.where(softmax_a > 1e-10, diff, 0)

        self._add_diff(a, diff)
        return diff


def softmax_log_cross_entropy(labels, logits):
    return Softmax_log_cross_entropy(labels, logits).res
