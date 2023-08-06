import json


def json_loads(obj):
    try:
        result = json.loads(obj)
    except:
        result = ''
    return result


def split_string(obj, delimiter):
    return str(obj).strip().split(delimiter)


def trim_string(string):
    return string.strip()


def trans_list(list_obj):
    return list(map(list, zip(*list_obj)))


def append_list(list_obj, obj):
    list_obj.append(obj)
    return list_obj


def trim_comment(obj):
    return str(obj).strip('/*').strip('*/')


def gen_dict(objs=list()):
    d = {}
    for obj in objs:
        d[obj.key] = obj.value.name
    return d


def gen_list(string):
    mts = str(string).maketrans('|', ' ')

    ls = str(string).translate(mts).split(' ')

    return list(filter(lambda x: x, ls))


def gen_table_dict(key, value):
    return dict(zip(value, key))


def trans_dict(k, v):
    return dict(zip(k, zip(*v)))


def format_matrix(list_obj):
    matrix = []
    temp_matrix = []
    for item in list_obj:
        temp_list = []
        for k, v in item.items():

            for v_item in v:
                temp_matrix.append({k: v_item})

            if not len(matrix):
                matrix = temp_matrix
            temp_matrix = []

            for i, val in enumerate(matrix):
                val[k] = v[i]
                # print('v:', v[i])

    return matrix
