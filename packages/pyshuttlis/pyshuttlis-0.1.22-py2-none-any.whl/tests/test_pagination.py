from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from shuttlis.pagination import After, Cursor, Paginator
from shuttlis.time import time_now, dataclass


@pytest.mark.parametrize("id,date", [(uuid4(), time_now())])
def test_from_string_and_str_are_dual(id, date):
    after = After(id, date)
    assert after == After.from_string(str(after))


def test_construction_of_cursor():
    after = After(uuid4(), time_now())
    json_req = {"after": str(after)}
    assert Cursor(after, 10) == Cursor.from_dict(json_req)


def test_construction_of_paginator():
    obj = MagicMock(id=uuid4(), created_at=time_now())
    paginator = Paginator.from_data([obj])

    assert str(After(obj.id, obj.created_at)) == paginator.as_dict()["last"]


def test_as_json_for_custom_paginator_and_paginator_are_same_for_similar_objs():
    id, date = uuid4(), time_now()

    p_obj = MagicMock(id=id, created_at=date)
    cp_obj = MagicMock(id=id, destroyed_at=date)

    @dataclass
    class CustomAfter(After):
        @classmethod
        def from_data(cls, data) -> "CustomAfter":
            return cls(data.id, data.destroyed_at)

    cp = Paginator.from_data([cp_obj], custom_cls=CustomAfter)
    p = Paginator.from_data([p_obj])

    assert p.as_dict() == cp.as_dict()
