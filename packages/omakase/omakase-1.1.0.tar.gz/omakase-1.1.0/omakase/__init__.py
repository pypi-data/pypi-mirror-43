from forbiddenfruit import curse as patch
from omakase.functions import *


# My list functions

patch(list, 'len', lambda self: len(self))

patch(list, 'map', lambda self, function: map(function, self))
patch(list, 'max', lambda self: max(self) if self else None)
patch(list, 'min', lambda self: min(self) if self else None)
patch(list, 'sum', lambda self: sum(self))
patch(list, 'zip', lambda self, other: zip(self, other))
patch(list, 'first', first)
patch(list, 'last', last)
patch(list, 'freq', freq)
patch(list, 'groupby', groupby)
patch(list, 'indexby', indexby)
patch(list, 'join', join)
patch(list, 'sortby', sortby)
patch(list, 'sorted', lambda self: sorted(self))
patch(list, 'reduce', reduce_sequence)
patch(list, 'percentile', percentile)
patch(list, 'percentiles', percentiles)

patch(list, 'filter', lambda self, function: filter(function, self))
patch(list, 'compact', compact_sequence)
patch(list, 'uniq', uniq)
patch(list, 'take', take)
patch(list, 'drop', drop)
patch(list, 'flatten', flatten)
patch(list, 'each_cons', each_cons)
patch(list, 'each_slice', each_slice)


# My tuple functions

patch(tuple, 'len', lambda self: len(self))
patch(tuple, 'list', lambda self: list(self))

patch(tuple, 'map', lambda self, function: map(function, self))
patch(tuple, 'max', lambda self: max(self) if self else None)
patch(tuple, 'min', lambda self: min(self) if self else None)
patch(tuple, 'sum', lambda self: sum(self))
patch(tuple, 'zip', lambda self, other: zip(self, other))
patch(tuple, 'first', first)
patch(tuple, 'last', last)
patch(tuple, 'freq', freq)
patch(tuple, 'groupby', groupby)
patch(tuple, 'indexby', indexby)
patch(tuple, 'join', join)
patch(tuple, 'sortby', sortby)
patch(tuple, 'sorted', lambda self: sorted(self))
patch(tuple, 'reduce', reduce_sequence)
patch(tuple, 'percentile', percentile)
patch(tuple, 'percentiles', percentiles)


# My dict functions

patch(dict, 'len', lambda self: len(self))
patch(dict, 'compact', compact_mapping)

