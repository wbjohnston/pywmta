import json
from pywmta import WMTA


if __name__ == '__main__':
    with open('key', 'r') as f:
        key = f.read()

    w = WMTA(key)
    print(json.dumps(w.getRailPrediction(['B03']), indent=4))


