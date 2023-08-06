# -----------------
# SMNet
# Written by smarsu
# -----------------

"""Convolutional nerual network layer"""

import math
import numpy as np
from ..blob import Tensor
from .. import layer as nn
from ..net import sm


class RawConv2D(nn.Layer):
    """Conv2D without padding.
    TODO(smarsu): Add dilations.
    """

    def __init__(self, input, filter, strides, stop_grad=False, name='raw_conv2d'):
        super(RawConv2D, self).__init__(stop_grad=stop_grad, name=name)
        self._prebuilt(input, filter, strides)

    
    def _prebuilt(self, input, filter, strides):
        self.input = input
        self.filter = filter
        self.strides = strides
        self.res = Tensor()

    
    def forward(self):
        # 1. Prepare data
        input = self.input.data
        filter = self.filter.data
        strides = self.strides

        # 2. Compute result
        ni, hi, wi, ci = input.shape
        ns, hs, ws, cs = strides
        hf, wf, _, co = filter.shape

        cf = hf * wf * ci
        ho, wo = (hi - hf) // hs + 1, (wi - wf) // ws + 1

        input_patches = []
        for _h in range(ho):
            for _w in range(wo):
                _h_start = _h * hs
                _w_start = _w * ws
                input_patche = np.reshape(input[:, _h_start:_h_start+hf, _w_start:_w_start+wf, :], [ni, 1, cf])
                input_patches.append(input_patche)
        input_patches = np.concatenate(input_patches, axis=1)
        input_patches = np.reshape(input_patches, [ni, ho, wo, cf])

        flatten_fliter = np.reshape(filter, [cf, co])
        self.flatten_fliter = flatten_fliter

        feature_map = np.matmul(input_patches, flatten_fliter)

        # 3. Feed result
        self.res.feed(feature_map)

    
    def backward(self):
        grad = self.res.grad
        self._compute_grad_input(grad)
    

    def _compute_grad_input(self, grad):
        # 1. Prepare data
        flatten_fliter = self.flatten_fliter
        strides = self.strides

        # 2. Compute grad
        grad = np.matmul(grad, flatten_fliter.T)

        n, ho, wo, cf = grad.shape
        ns, hs, ws, cs = strides
        hf, wf, _, co = self.filter.shape
        
        collect_grad = np.zeros(self.input.shape)
        for _h in range(ho):
            for _w in range(wo):
                _h_start = _h * hs
                _w_start = _w * ws
                collect_grad[:, _h_start:_h_start+hf, _w_start:_w_start+wf, :] += np.reshape(grad[:, _h, _w, :], [n, ]
        


class Conv2d():
    def __init__(self):
        pass

    
    def __call__(self, feature_map, filters, strides, padding):
        """Compute result use matrix multiple.
        
        Now do it in a simple way.
        TODO(smarsu): Difficult
        """
        res = Tensor()
        sm.set_tensor_flow(feature_map, res, lambda :self._op(feature_map=feature_map, filters=filters, strides=strides, padding=padding, res=res))
        return res

    
    def _op(self, feature_map, filters, strides, padding, res):
        """We consider a kernel of feature_map is one feature vector, and concat them.
        
        Args:
            feature_map: Tensor, shape like [batch_size, high, weight, channel]
        """
        feature_map_tensor = feature_map
        feature_map = feature_map.data
        filters = filters.data

        ni, hi, wi, ci = feature_map.shape
        hf, wf, cf, co = filters.shape
        ns, hs, ws, cs = strides

        if padding == 'SAME':
            n2, h2, w2, c2 = ni, math.ceil(hi / hs), math.ceil(wi / ws), co  # Compute new shape
        if padding == 'VALID':
            n2, h2, w2, c2 = ni, (hi - (hf - 1) - 1) // hs + 1, (wi - (wf - 1) - 1) // ws + 1, co  # Compute new shape

        if padding == 'SAME':
            p_h = hs * (h2 - 1) + (hf - 1) + 1 - hi
            p_w = ws * (w2 - 1) + (wf - 1) + 1 - wi
            feature_map = np.pad(feature_map, ((0, 0), (p_h // 2, p_h - p_h // 2), (p_w // 2, p_w - p_w // 2), (0, 0)), 'constant', constant_values=0)


        new_feature_map = np.empty(
            [n2 * h2 * w2,
             hf * wf * ci]
        )

        cnt = 0
        for _n in range(ni):
            for _h in range(h2):
                for _w in range(w2):
                    cur_h = _h * hs
                    cur_w = _w * ws
                    new_feature_map[cnt, ...] = np.reshape(feature_map[_n, cur_h:cur_h+hf, cur_w:cur_w+wf, :], [-1])
                    cnt += 1

        new_filters = np.reshape(filters, [-1, co])

        output = np.matmul(new_feature_map, new_filters)
        output_NCHW = np.reshape(output, [ni, h2, w2, co])

        feature_map_tensor._matrix_data = new_feature_map
        res.feed(output_NCHW)

    
    def _compute_diff_a(self, feature_map, filters):
        filters = filters.data
        filters = np.reshape(filters, [-1, co])
        hf, wf, cf, co = filters.shape

        grad = np.reshape(grad, [-1, co])
        grad = np.matmul(grad, filters.T)


    def _compute_diff_b(self, feature_map, filters):
        """Reshape left_1 and right to make it computable."""


conv2d = Conv2d()


def matrix_conv2d(feature_map, filters, strides, padding):
    """Compute result use matrix multiple."""
    assert feature_map.shape[-1] == filters.shape[-2], 'feature map channel {} must equal to filter in channel {}'.format(feature_map.shape[-1], filters.shape[-2])
    
    N, H, W, C = feature_map.shape
    f_h, f_w, i_c, o_c = filters.shape
    _, h_str, w_str, _ = strides
    if padding == 'SAME':
        n2, h2, w2, c2 = N, math.ceil(H / h_str), math.ceil(W / w_str), o_c  # Compute new shape
    # VALID new shape function: (old_h - (filter_h - 1) - 1) // 2 + 1
    if padding == 'VALID':
        n2, h2, w2, c2 = N, (H - (f_h - 1) - 1) // 2 + 1, (W - (f_w - 1) - 1) // 2 + 1, o_c  # Compute new shape
    fm2 = np.empty((n2, h2, w2, c2))  # Create a `empty` array is fast.

    # If padding is SAME, we will pad feature map to keep shape.
    # Pad function: stride * (new_h - 1) + (filter_h - 1) + 1 - old_h
    if padding == 'SAME':
        p_h = h_str * (h2 - 1) + (f_h - 1) + 1 - H
        p_w = w_str * (w2 - 1) + (f_w - 1) + 1 - W
        feature_map = np.pad(feature_map, ((0, 0), (p_h // 2, p_h - p_h // 2), (p_w // 2, p_w - p_w // 2), (0, 0)), 'constant', constant_values=0)

    filters_matrix = np.reshape(filters, (f_h * f_w * i_c, o_c))
    
    f_map_matrix = np.empty((n2, h2, w2, f_h * f_w * i_c))
    for h in range(h2):
        for w in range(w2):
            # Gusses Christ, change here, it become right???
            # TODO(smarsu): batch
            f_map_matrix[0, h, w, :] = feature_map[0, h * h_str: h * h_str + f_h, w * w_str: w * w_str + f_w, :].flatten()
            #for c in range(i_c):
                #f_map_matrix[h * w2 + w, c * f_h * f_w: (c + 1) * f_h * f_w] = feature_map[0, h * h_str: h * h_str + f_h, w * w_str: w * w_str + f_w, c].flatten()

    for _ in range(10):
        t1 = time.time()
        fm2 = np.matmul(f_map_matrix, filters_matrix)
        t2 = time.time()
        print('cal t:', t2 - t1)
    #fm2 = fm2.T
    #fm2 = np.reshape(fm2, (n2, h2, w2, c2))
    return fm2
