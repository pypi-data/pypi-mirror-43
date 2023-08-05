
import numpy as np


def make_new_state(state, domain, intent, slots, utterance='', reset_slots=[]):
    new_state = state.clone()
    new_state.uesr_domain = domain
    new_state.user_intent = intent
    new_state.utterance = utterance
    request_fill = []
    for slot in slots:
        if isinstance(slot, str):
            slot_name = slot
            value = 1
        else:
            slot_name = slot['slot_name']
            value = slot['slot_value']
        if intent.startswith('request'):
            stype = 'requestable'
            request_fill.append(slot_name)
        else:
            stype = 'informable'
        new_state[(stype, slot_name)] = value
    for slot in new_state.slots:
        if slot['type'] == 'informable' and slot['name'] in reset_slots:
            slot['value'] = None
        elif slot['type'] == 'requestable' \
                and slot['name'] not in request_fill:
            slot['value'] = None
    return new_state


def build_dialog_train_data(dialogs, init_state):
    x_dst, y_dst = [], []
    x_dpl, y_dpl = [], []
    for dialog in dialogs:
        state = init_state.clone()
        for turn in dialog:
            if 'user' in turn:
                new_state = make_new_state(
                    init_state,
                    turn['domain'],
                    turn['intent'],
                    turn['slots'],
                    reset_slots=turn['reset_slots']
                )
                slot_vec = state.slot_vec
                new_slot_vec = new_state.slot_vec
                y = np.array([
                    1 if a != b else 0
                    for a, b in zip(slot_vec.tolist(), new_slot_vec.tolist())
                ])
                x0 = state.vec
                x1 = new_state.vec
                x = np.concatenate([x0, x1])
                x_dst.append(x)
                y_dst.append(y)
                # if turn['reset_slots']:
                #     import pdb; pdb.set_trace()
                state = new_state
            if 'sys' in turn:
                x = state.vec
                state.sys_intent = turn['intent']
                y = state.sys_vec
                x_dpl.append(x)
                y_dpl.append(y)

    x_dst = np.array(x_dst)
    y_dst = np.array(y_dst)
    x_dpl = np.array(x_dpl)
    y_dpl = np.array(y_dpl)
    print(x_dst.shape, y_dst.shape, x_dpl.shape, y_dpl.shape)
    return x_dst, y_dst, x_dpl, y_dpl
