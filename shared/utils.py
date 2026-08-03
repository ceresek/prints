import typing as _typing
import itertools as _itertools

def delta_to_absolute [T: int | float] (deltas : _typing.Iterable [tuple [T, ...]]) -> list [tuple [T, ...]]:
    return list (_itertools.accumulate (deltas, lambda a, b: tuple (aa + bb for aa, bb in zip (a, b, strict = True))))
