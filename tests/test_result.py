import pytest
from fp_result.result import Ok, Err, Result


def some_result(input: int) -> Result[int]:
    return Ok(input)


def test_match():
    some_error = some_result(2)
    output = 0
    match some_error:
        case Ok(v):
            output = v
        case Err(e):
            print(e)
    assert output == 2


@pytest.mark.xfail
def test_unwrap():
    res = Err("none")
    res.unwrap()

def test_is_ok():
    res = Ok(2333)
    print(res)
    assert res.is_ok()

def test_is_err():
    res = Err("I'm some error")
    print(res)
    assert res.is_error()
