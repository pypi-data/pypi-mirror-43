# Functions that I am missing, mostly inspired from Ruby


def join(sequence, separator):
    return separator.join(sequence)


def sortby(sequence, function):
    return sorted(sequence, key=function)


def compact_sequence(sequence):
    result = []
    for each in sequence:
        if each is None: continue
        result.append(each)

    return result

def compact_mapping(mapping):
    result = {}
    for name in mapping:
        value = mapping[name]
        if value is None: continue
        result[name] = value

    return result

def freq(sequence, function=None):
    mapping = {}
    for each in sequence:
        key = function(each) if function else each
        mapping[key] = mapping.get(key, 0) + 1

    return mapping


def groupby(sequence, function=None):
    mapping = {}
    for each in sequence:
        key = function(each) if function else each
        if not key in mapping: mapping[key] = []
        mapping[key].append(each)

    return mapping


def indexby(sequence, function=None):
    mapping = {}
    for each in sequence:
        key = function(each) if function else each
        if key in mapping: continue
        mapping[key] = each

    return mapping


def uniq(sequence):
    reply = []
    mapping = {}
    for each in sequence:
        if each in mapping: continue
        mapping[each] = True
        reply.append(each)

    return reply


def take(sequence, n):
    return sequence[:n]


def drop(sequence, n):
    return sequence[n:]


def first(sequence):
    return sequence[0] if sequence else None


def last(sequence):
    return sequence[-1] if sequence else None


def reduce_sequence(sequence, first_argument, second_argument=None):
    if second_argument:
        function = second_argument
        initial = first_argument
        return reduce(function, sequence, initial)
    elif not sequence:
        return None
    else:
        function = first_argument
        return reduce(function, sequence)


def flatten(sequence):
    result = []
    for each in sequence:
        result.extend(each) if isinstance(each, list) else result.append(each)

    return result


def each_cons(sequence, n):
    if n < 1: raise ValueError
    result = []
    for i in range(0, sequence.len() - n + 1):
        result.append(sequence[i : i + n])

    return result


def each_slice(sequence, n):
    if n < 1: raise ValueError
    result = []
    for i in range(0, sequence.len(), n):
        result.append(sequence[i : i + n])

    return result


def percentile(sequence, float):
    if not sequence: return None
    length = len(sequence) - 1
    return sorted(sequence)[int(float * length)]


def percentiles(sequence, *floats):
    if not sequence: return None
    length = len(sequence) - 1
    sorted_sequence = sorted(sequence)
    return map(lambda float: sorted_sequence[int(float * length)], floats)
