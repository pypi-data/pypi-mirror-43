# -*- coding: utf-8 -*-
"""训练DPL部分"""

from ..dpl.dpl import DialogPolicy


def train_dpl(x_dpl, y_dpl):
    dpl = DialogPolicy()
    dpl.fit(x_dpl, y_dpl)

    print('\n' + '-' * 30)
    print('DPL: trained')
    return dpl
