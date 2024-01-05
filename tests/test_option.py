from fp_result.option import NoneValue, Option, Some


def test_some():
    some_a = Some(1)
    res = some_a.map(lambda x: x + 1)
    assert res == Some(2)


def test_none():
    def div(left: int, right: int) -> Option[float]:
        if right == 0:
            return NoneValue()
        else:
            return Some(left / right)

    assert div(2, 0).is_none()
