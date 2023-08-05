from typing import (Callable,
                    Iterable)

from lz import left
from lz.hints import (Domain,
                      Range)
from lz.iterating import (first,
                          last)
from lz.replication import duplicate
from tests.utils import are_objects_similar


def test_first(projector: Callable[[Range, Domain], Range],
               projector_initial: Range,
               projector_iterable: Iterable[Domain]) -> None:
    accumulate = left.accumulator(projector, projector_initial)

    result = accumulate(projector_iterable)

    assert first(result) is projector_initial


def test_last(projector: Callable[[Range, Domain], Range],
              projector_initial: Range,
              projector_iterable: Iterable[Domain]) -> None:
    first_target, second_target = duplicate(projector_iterable)
    accumulate = left.accumulator(projector, projector_initial)
    fold = left.folder(projector, projector_initial)

    result = accumulate(first_target)
    fold_result = fold(second_target)

    assert are_objects_similar(last(result), fold_result)
