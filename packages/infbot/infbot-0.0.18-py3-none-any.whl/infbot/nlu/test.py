
import sys
import pickle
from .lu import LanguageUnderstanding  # noqa


def main(path):
    with open(path, 'rb') as fp:
        lu = pickle.load(fp)
    while True:
        utterance = input('Utterance:')
        if utterance.lower() in ('quit', 'exit'):
            return
        user_action = lu.forward(utterance)
        print(user_action)


if __name__ == '__main__':
    main(sys.argv[1])
