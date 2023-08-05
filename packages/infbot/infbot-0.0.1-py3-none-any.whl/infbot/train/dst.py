# -*- coding: utf-8 -*-
"""训练DST部分"""

from ..dst.dst import DialogStateTracker


def train_dst(x_dst, y_dst):
    dst = DialogStateTracker()
    dst.fit(x_dst, y_dst)

    print('\n' + '-' * 30)
    print('DST: trained')
    return dst
