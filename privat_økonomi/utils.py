import pprint


def pexit(s):
    pprint.pprint(s)
    print(type(s))
    if hasattr(s, '__len__'):
        print(f'Length: {len(s)}')
    exit()
