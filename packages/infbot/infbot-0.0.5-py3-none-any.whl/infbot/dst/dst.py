# -*- coding: utf-8 -*-
"""
对话状态跟踪
"""

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from ..common.dialog_state import DialogState
from ..common.user_action import UserAction
from ..common.build_dialog_train_data import make_new_state


class DialogStateTracker(object):

    def __init__(self):
        """初始化DST
        """
        self.clf = None

    def forward(self,
                init_state: DialogState,
                state: DialogState,
                user_action: UserAction):
        """
        input:
            state: current state
            user_action: action from this turn
        return: new_state DialogState
        """
        state = state.clone()
        new_state = make_new_state(
            init_state,
            user_action.domain,
            user_action.intent,
            user_action.slots,
            user_action.utterance
        )
        x0 = state.vec
        x1 = new_state.vec
        x = np.concatenate([x0, x1])
        pred = self.clf.predict(np.array([x])).flatten()
        state.user_domain = new_state.user_domain
        state.user_intent = new_state.user_intent
        state.utterance = new_state.utterance
        # if state.utterance == '再见':
        #     import pdb;pdb.set_trace()
        for i, slot in enumerate(new_state.slots):
            if pred[i]:
                state.slots[i] = slot
        return state

    def __len__(self):
        return len(self.slots)

    def fit(self, x, y):
        clf = RandomForestClassifier(n_estimators=100)
        clf.fit(x, y)
        self.clf = clf
