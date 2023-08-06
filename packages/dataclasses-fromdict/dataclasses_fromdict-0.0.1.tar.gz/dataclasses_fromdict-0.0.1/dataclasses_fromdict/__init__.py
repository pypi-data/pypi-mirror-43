# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import typing
from typing import Tuple
from dataclasses import (
    is_dataclass,
    fields
)


def _get_list_info(cls):
    if cls is list:
        return (list, None)
    if isinstance(cls, typing._GenericAlias):
        if cls.__origin__ is list:
            return (list, *cls.__args__)

def _get_tuple_info(cls):
    if cls is tuple:
        return (tuple, None)
    if isinstance(cls, typing._GenericAlias):
        if cls.__origin__ is tuple:
            return (tuple, cls.__args__)


def from_dict(d: dict, cls: type):
    if not is_dataclass(cls):
        raise TypeError(f"{repr(cls)} is not a dataclass")
    kwargs = d.copy()
    for field in fields(cls):
        if is_dataclass(field.type):
            kwargs[field.name] = from_dict(kwargs[field.name])
            continue
        list_info = _get_list_info(field.type)
        if list_info:
            kwargs[field.name] = from_list(kwargs[field.name], *list_info)
            continue
        tuple_info = _get_tuple_info(field.type)
        if tuple_info:
            kwargs[field.name] = from_tuple(kwargs[field.name], *tuple_info)
            continue
    return cls(**kwargs)


def from_list(l: list, cls: type=list, el_type: type=None):
    if el_type is None:
        return cls(l)
    else:
        return cls(from_dict(i, el_type) for i in l)


def from_tuple(t: tuple, cls: type=tuple, el_types: Tuple[type]=None):
    if el_types is None:
        return cls(t)
    elif len(el_types) == 2 and el_types[-1] is Ellipsis:
        vartype = el_types[0]
        return cls(from_dict(i, vartype) for i in t)
    elif len(t) != len(el_types):
        raise ValueError(f'{repr(t)} does not match tuple {repr(el_types)}')
    else:
        return cls(from_dict(l, r) for l, r in zip(t, el_types))
