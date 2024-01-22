from __future__ import annotations


def list_converter_to_set(list_: list) -> set:
    set_ = set()
    for l in list_:
        set_.add(l)
    return set_
