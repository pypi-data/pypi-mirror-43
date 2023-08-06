# ----------------------------
# SMNet Convolutional Networks
# Written by smarsu
# ----------------------------

"""Convolutional nerual network layer"""

import math
import numpy as np
from ..blob import Tensor
from .. import layer as nn


class Conv2D(nn.Layer):
    """
    TODO(smarsu): Add dilations.
    """

    def __init__(self, input, filter, strides, padding, stop_grad=False, name='Conv2D'):
        super(Conv2D, self).__init__(stop_grad=stop_grad, name=name)
        self._prebuilt(input, filter, strides, padding)

    
    def _prebuilt(self, input, filter, strides, padding):
        self.input = input
        self.filter = filter
        self.strides = strides
        self.padding = padding
        self.res = Tensor()

    
    def forward(self):
        # 1. Prepare data
        input = self.input.data
        filter = self.filter.data
        strides = self.strides
        padding = self.padding

        ni, hi, wi, ci = input.shape
        ns, hs, ws, cs = strides
        hf, wf, _, co = filter.shape

        # 2. Prepare output shape
        cf = hf * wf * ci

        if padding == 'SAME':
            ho, wo = math.ceil(hi / hs), math.ceil(wi / ws)
        if padding == 'VALID':
            ho, wo = (hi - hf) // hs + 1, (wi - wf) // ws + 1

        # 3. Pad input if `padding` is SAME
        if padding == 'SAME':
            hp = hs * (ho - 1) + (hf - 1) + 1 - hi
            wp = ws * (wo - 1) + (wf - 1) + 1 - wi
            pad_shape = ((0, 0), (hp // 2, hp - hp // 2), (wp // 2, wp - wp // 2), (0, 0))
            self.pad_shape = pad_shape
            input = np.pad(input, pad_shape, 'constant', constant_values=0)

        self.pad_input_shape = input.shape

        # 4. Extracts image patches from the input tensor to form a virtual tensor
        input_patches = []
        for _h in range(ho):
            for _w in range(wo):
                _h_start = _h * hs
                _w_start = _w * ws
                input_patche = np.reshape(input[:, _h_start:_h_start+hf, _w_start:_w_start+wf, :], [ni, 1, cf])
                input_patches.append(input_patche)
        input_patches = np.concatenate(input_patches, axis=1)
        input_patches = np.reshape(input_patches, [ni, ho, wo, cf])
        self.input_patches = input_patches

        # 5. Flattens the filter to a 2-D matrix
        flatten_fliter = np.reshape(filter, [cf, co])
        self.flatten_fliter = flatten_fliter

        # 6. Compute result
        feature_map = np.matmul(input_patches, flatten_fliter)

        # 7. Feed result
        self.res.feed(feature_map)

    
    def backward(self):
        grad = self.res.grad
        self._compute_grad_input(grad)
        self._compute_grad_filter(grad)
    

    def _compute_grad_input(self, grad):
        # 1. Prepare data
        flatten_fliter = self.flatten_fliter
        strides = self.strides
        padding = self.padding

        # 2. Compute grad
        grad = np.matmul(grad, flatten_fliter.T)

        n, ho, wo, cf = grad.shape
        ns, hs, ws, cs = strides
        hf, wf, ci, co = self.filter.shape

        collect_grad = np.zeros(self.pad_input_shape)
        for _h in range(ho):
            for _w in range(wo):
                _h_start = _h * hs
                _w_start = _w * ws
                collect_grad[:, _h_start:_h_start+hf, _w_start:_w_start+wf, :] += np.reshape(grad[:, _h, _w, :], [n, hf, wf, ci])

        if padding == 'SAME':
            collect_grad_shape = collect_grad.shape
            collect_grad = eval(
                'collect_grad[{}]'.format(
                    ','.join(['{}:{}'.format(l, collect_grad_shape[idx]-r) for idx, (l, r) in enumerate(self.pad_shape)])
                )
            )

        # 3. Add grad
        self.input.add_grad(collect_grad)


    def _compute_grad_filter(self, grad):
        # 1. Prepare data
        input_patches = self.input_patches

        # 2. Compute grad
        n, ho, wo, cf = input_patches.shape
        n, ho, wo, co = grad.shape
        input_patches = np.reshape(input_patches, (-1, cf))
        grad = np.reshape(grad, (-1, co))

        grad = np.matmul(input_patches.T, grad)
        grad = np.reshape(grad, self.filter.shape)

        # 3. Add grad
        self.filter.add_grad(grad)


def conv2d(input, filter, strides, padding='SAME', stop_grad=False, name='Conv2D'):
    return Conv2D(input, filter, strides, padding, stop_grad=stop_grad, name=name).res


class Max_pool(nn.Layer):
    def __init__(self, value, ksize, strides, padding, stop_grad, name):
        super(Max_pool, self).__init__(stop_grad=stop_grad, name=name)
        self._prebuilt(value, ksize, strides, padding)

    
    def _prebuilt(self, value, ksize, strides, padding):
        self.value = value
        self.ksize = ksize
        self.strides = strides
        self.padding = padding
        self.res = Tensor()


    def forward(self):
        # 1. Prepare data
        value = self.value.data
        ksize = self.ksize
        strides = self.strides
        padding = self.padding

        ni, hi, wi, ci = value.shape
        _, hf, wf, _ = ksize
        ns, hs, ws, cs = strides

        # 2. Prepare output shape
        if padding == 'SAME':
            ho, wo = math.ceil(hi / hs), math.ceil(wi / ws)
        if padding == 'VALID':
            ho, wo = (hi - hf) // hs + 1, (wi - wf) // ws + 1

        # 3. Pad input if `padding` is SAME
        if padding == 'SAME':
            hp = hs * (ho - 1) + (hf - 1) + 1 - hi
            wp = ws * (wo - 1) + (wf - 1) + 1 - wi
            pad_shape = ((0, 0), (hp // 2, hp - hp // 2), (wp // 2, wp - wp // 2), (0, 0))
            self.pad_shape = pad_shape
            value = np.pad(value, pad_shape, 'constant', constant_values=-np.inf)  # What value shell I pad 0/-np.inf?

        self.pad_value_shape = value.shape

        # 4. Extracts image patches
        input_patches = []
        for _h in range(ho):
            for _w in range(wo):
                _h_start = _h * hs
                _w_start = _w * ws
                #input_patche = np.max(value[:, _h_start:_h_start+hf, _w_start:_w_start+wf, :], axis=(1, 2))
                #input_patche = input_patche[:, np.newaxis, :]
                input_patche = value[:, _h_start:_h_start+hf, _w_start:_w_start+wf, :]
                input_patches.append(input_patche)
                
        #input_patches = np.concatenate(input_patches, axis=1)
        input_patches = np.stack(input_patches, axis=3)
        input_patches = np.max(input_patches, axis=(1, 2))
        input_patches = np.reshape(input_patches, (-1, ho, wo, ci))

        # 5. Feed result
        self.res.feed(input_patches)


    def backward(self):
        grad = self.res.grad
        self._compute_grad_value(grad)

    
    def _compute_grad_value(self, grad):
        # 1. Prepare data
        value = self.value.data
        ksize = self.ksize
        strides = self.strides
        padding = self.padding

        ni, hi, wi, ci = value.shape
        _, hf, wf, _ = ksize
        ns, hs, ws, cs = strides

        # 2. Prepare output shape
        if padding == 'SAME':
            ho, wo = math.ceil(hi / hs), math.ceil(wi / ws)
        if padding == 'VALID':
            ho, wo = (hi - hf) // hs + 1, (wi - wf) // ws + 1

        # 3. Compute grad
        collect_grad = np.zeros(self.pad_value_shape)
        for _h in range(ho):
            for _w in range(wo):
                _h_start = _h * hs
                _w_start = _w * ws
                patch_value = value[:, _h_start:_h_start+hf, _w_start:_w_start+wf, :]
                patch_value = np.reshape(patch_value, [-1, hf + wf, ci])
                max_index = np.argmax(patch_value, axis=1)  # shape: [batch, channel_in]
                h_index, w_index = max_index // wf, max_index % wf

                batch, channel_in = max_index.shape
                for _b in range(batch):
                    for _c in range(channel_in):
                        collect_grad[_b, _h_start+h_index[_b, _c], _w_start+w_index[_b, _c], _c] += grad[_b, _h, _w, _c]

        # 4. Depad grad
        if padding == 'SAME':
            collect_grad_shape = collect_grad.shape
            collect_grad = eval(
                'collect_grad[{}]'.format(
                    ','.join(['{}:{}'.format(l, collect_grad_shape[idx]-r) for idx, (l, r) in enumerate(self.pad_shape)])
                )
            )

        # 5. Add grad
        self.value.add_grad(collect_grad)


def max_pool(value, ksize, strides, padding, stop_grad=False, name='Max_pool'):
    return Max_pool(value, ksize, strides, padding, stop_grad, name).res
