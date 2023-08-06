# -----------------
# SMNet
# Written by smarsu
# -----------------

"""Convolutional nerual network layer"""

import math
import numpy as np
from ..blob import Tensor, Variable
from .. import layer as nn
from ..net import sm

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
