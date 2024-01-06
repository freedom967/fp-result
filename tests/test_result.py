import asyncio
import pytest
from fp_result.result import Ok, Err, Result
from fp_result.utils import map_exception
from fp_result.utils.exception_mapper import map_async_exception


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


def test_map_exception():
    @map_exception
    def some_maybe_exception(left: int, right: int) -> float:
        return left / right

    res = some_maybe_exception(1, 0)
    assert res.is_error()


def test_map_async_exception():
    @map_async_exception
    async def async_maybe_exception(data: int) -> bool:
        if data == 0:
            raise ValueError("some error")
        else:
            await asyncio.sleep(0.5)
            return True

    res = asyncio.run(async_maybe_exception(0))
    assert res.is_error()
