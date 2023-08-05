# -*- coding: utf-8 -*-
"""训练NLU部分"""

import os
from ..nlu.nlu import NaturalLanguageUnderstanding


def train_nlu(data_path):

    nlu_path = os.path.join(data_path, 'nlu')
    assert os.path.exists(nlu_path), 'Invalid NLU data path'
    print('Start train NLU')
    nlu = NaturalLanguageUnderstanding()
    nlu.fit(nlu_path)

    print('\n' + '-' * 30)
    print('NLU Intents:')
    print('\n'.join(nlu.intent_list))
    print('NLU Slots')
    print(nlu.slot_list)

    return nlu
