from fp_result.option import NoneValue, Option, Some


def test_some():
    some_a = Some(1)
    res = some_a.map(lambda x: x + 1)
    assert res == Some(2)


def div(left: int, right: int) -> Option[float]:
    if right == 0:
        return NoneValue()
    else:
        return Some(left / right)


def test_none():
    assert div(2, 0).is_none()


def test_and_then():
    some_a = Some(1)
    res = some_a.and_then(lambda x: div(x, 0))
    assert res.is_none()


def test_unwrap_or():
    v = Option.NoneValue()
    out = v.unwrap_or(4)
    assert out == 4
