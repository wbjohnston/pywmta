import json
from pywmta import WMTA


if __name__ == '__main__':
    with open('key', 'r') as f:
        key = f.read()

    w = WMTA(key)
    try:
        print(json.dumps(w.get_rail_prediction(['B03']), indent=4))
    except Exception:
        print('failed')

    try:
        print(json.dumps(w.get_bus_prediction(['1001195']), indent=4))
    except:
        print('failed')


