
import os
# import sys
import pickle


def main(model_path, outside_function={}):
    # if len(sys.argv) != 2:
    #     print('python3 -m serve model_path')
    #     exit(1)
    # model_path = sys.argv[1]
    nlu_output = os.path.join(model_path, 'nlu.model')
    nlg_output = os.path.join(model_path, 'nlg.model')
    dst_output = os.path.join(model_path, 'dst.model')
    dpl_output = os.path.join(model_path, 'dpl.model')
    state_path = os.path.join(model_path, 'init_state.model')
    nlu = pickle.load(open(nlu_output, 'rb'))
    nlg = pickle.load(open(nlg_output, 'rb'))
    nlg.outside_function = outside_function
    dst = pickle.load(open(dst_output, 'rb'))
    dpl = pickle.load(open(dpl_output, 'rb'))
    state = pickle.load(open(state_path, 'rb'))
    test_model(state, nlu, dst, dpl, nlg)


def test_model(init_state, nlu, dst, dpl, nlg):
    state = init_state.clone()
    while True:
        utterance = input('user:')
        if utterance.lower() in ('quit', 'exit'):
            exit(0)
        # import pdb; pdb.set_trace()
        user_action = nlu.forward(utterance)
        new_state = dst.forward(init_state, state, user_action)
        sys_action = dpl.forward(new_state)
        sys_response = nlg.forward(new_state, sys_action)
        state = new_state
        state.sys_intent = sys_action.intent
        print('sys:', sys_response)


if __name__ == '__main__':
    main()
