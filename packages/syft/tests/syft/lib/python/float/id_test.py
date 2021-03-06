# third party
import pytest

# syft absolute
from syft.lib.python.float import Float

test_float = Float(42.5)
python_float = 42.5
other = Float(42.5)


def test_id_abs() -> None:
    res = test_float.__abs__()
    py_res = python_float.__abs__()

    assert res == py_res
    assert res.id
    assert res.id != test_float.id


def test_id_add() -> None:
    res = test_float.__add__(other)
    py_res = python_float.__add__(other)

    assert res == py_res
    assert res.id
    assert res.id != test_float.id


def test_id_bool() -> None:
    res = test_float.__bool__()
    py_res = python_float.__bool__()

    assert res == py_res
    assert res.id
    assert res.id != test_float.id


def test_id_divmod() -> None:
    r1, q1 = test_float.__divmod__(other)
    r2, q2 = python_float.__divmod__(other)

    assert r1 == r2
    assert q1 == q2
    assert r1.id
    assert q1.id
    assert r1.id != test_float.id
    assert q1.id != test_float.id
    assert r1.id != q1.id


def test_id_eq() -> None:
    res = test_float.__eq__(other)
    py_res = python_float.__eq__(other)

    assert res == py_res
    assert res.id
    assert res.id != test_float.id


def test_id_floordiv() -> None:
    res = test_float.__floordiv__(other)
    py_res = python_float.__floordiv__(other)

    assert res == py_res
    assert res.id
    assert res.id != test_float.id


def test_id_ge() -> None:
    res = test_float.__ge__(other)
    py_res = python_float.__ge__(other)

    assert res == py_res
    assert res.id
    assert res.id != test_float.id


def test_id_gt() -> None:
    res = test_float.__gt__(other)
    py_res = python_float.__gt__(other)

    assert res == py_res
    assert res.id
    assert res.id != test_float.id


def test_id_iadd() -> None:
    res = test_float.__iadd__(other)
    assert res.id == test_float.id


def test_id_ifloordiv() -> None:
    res = test_float.__ifloordiv__(other)
    assert res.id == test_float.id


def test_id_imod() -> None:
    res = test_float.__imod__(other)
    assert res.id == test_float.id


def test_id_imul() -> None:
    res = test_float.__imul__(other)
    assert res.id == test_float.id


def test_id_ipow() -> None:
    res = test_float.__ipow__(other)
    assert res.id == test_float.id


def test_id_isub() -> None:
    res = test_float.__isub__(other)
    assert res.id == test_float.id


def test_id_itruediv() -> None:
    res = test_float.__itruediv__(other)
    assert res.id == test_float.id


def test_id_le() -> None:
    res = test_float.__le__(other)
    py_res = python_float.__le__(other)

    assert res == py_res
    assert res.id
    assert res.id != test_float.id


def test_id_lt() -> None:
    res = test_float.__lt__(other)
    py_res = python_float.__lt__(other)

    assert res == py_res
    assert res.id
    assert res.id != test_float.id


def test_id_mod() -> None:
    res = test_float.__mod__(other)
    py_res = python_float.__mod__(other)

    assert res == py_res
    assert res.id
    assert res.id != test_float.id


def test_id_mul() -> None:
    res = test_float.__mul__(other)
    py_res = python_float.__mul__(other)

    assert res == py_res
    assert res.id
    assert res.id != test_float.id


def test_id_ne() -> None:
    res = test_float.__ne__(other)
    py_res = python_float.__ne__(other)

    assert res == py_res
    assert res.id
    assert res.id != test_float.id


def test_id_neg() -> None:
    res = test_float.__neg__()
    py_res = python_float.__neg__()

    assert res == py_res
    assert res.id
    assert res.id != test_float.id


def test_id_pow() -> None:
    res = test_float.__pow__(other)
    py_res = python_float.__pow__(other)

    assert res == py_res
    assert res.id
    assert res.id != test_float.id


def test_id_radd() -> None:
    res = test_float.__radd__(other)
    py_res = python_float.__radd__(other)

    assert res == py_res
    assert res.id
    assert res.id != test_float.id


def test_id_rdivmod() -> None:
    r1, q1 = test_float.__rdivmod__(other)
    r2, q2 = python_float.__rdivmod__(other)

    assert r1 == r2
    assert q1 == q2

    assert r1.id != q1.id
    assert r1.id != test_float.id
    assert q1.id != test_float.id


def test_id_rfloordiv() -> None:
    res = test_float.__rfloordiv__(other)
    py_res = python_float.__rfloordiv__(other)

    assert res == py_res
    assert res.id
    assert res.id != test_float.id


def test_id_rmod() -> None:
    res = test_float.__rmod__(other)
    py_res = python_float.__rmod__(other)

    assert res == py_res
    assert res.id
    assert res.id != test_float.id


def test_id_rmul() -> None:
    res = test_float.__rmul__(other)
    py_res = python_float.__rmul__(other)

    assert res == py_res
    assert res.id
    assert res.id != test_float.id


def test_id_round() -> None:
    res = test_float.__round__()
    py_res = python_float.__round__()

    assert res == py_res
    assert res.id
    assert res.id != test_float.id


def test_id_rpow() -> None:
    res = test_float.__rpow__(other)
    py_res = python_float.__rpow__(other)

    assert res == py_res
    assert res.id
    assert res.id != test_float.id


def test_id_rsub() -> None:
    res = test_float.__rsub__(other)
    py_res = python_float.__rsub__(other)

    assert res == py_res
    assert res.id
    assert res.id != test_float.id


def test_id_rtruediv() -> None:
    res = test_float.__rtruediv__(other)
    py_res = python_float.__rtruediv__(other)

    assert res == py_res
    assert res.id
    assert res.id != test_float.id


def test_id_sub() -> None:
    res = test_float.__sub__(other)
    py_res = python_float.__sub__(other)

    assert res == py_res
    assert res.id
    assert res.id != test_float.id


def test_id_truediv() -> None:
    res = test_float.__truediv__(other)
    py_res = python_float.__truediv__(other)

    assert res == py_res
    assert res.id
    assert res.id != test_float.id


def test_id_trunc() -> None:
    res = test_float.__trunc__()
    py_res = python_float.__trunc__()

    assert res == py_res
    assert res.id
    assert res.id != test_float.id


def test_id_as_integer_ratio() -> None:
    u1, l1 = test_float.as_integer_ratio()
    u2, l2 = python_float.as_integer_ratio()

    assert u1 == u2
    assert l1 == l2
    assert u1.id != l1.id
    assert l1.id != test_float.id
    assert test_float.id != u1.id


@pytest.mark.xfail
def test_id_binary() -> None:
    # TODO finish this when we have bytes support
    assert True is False


def test_id_conjugate() -> None:
    res = test_float.conjugate()
    py_res = python_float.conjugate()

    assert res == py_res
    assert res.id
    assert res.id != test_float.id


def test_id_hex() -> None:
    res = test_float.hex()
    py_res = python_float.hex()

    assert res == py_res
    assert res.id
    assert res.id != test_float.id


def test_id_imag() -> None:
    res = test_float.imag
    py_res = python_float.imag

    assert res == py_res
    assert res.id
    assert res.id != test_float.id


def test_id_is_integer() -> None:
    res = test_float.is_integer()
    py_res = python_float.is_integer()

    assert res == py_res
    assert res.id
    assert res.id != test_float.id


def test_id_real() -> None:
    res = test_float.real
    py_res = python_float.real

    assert res == py_res
    assert res.id
    assert res.id != test_float.id


def test_upcast() -> None:
    assert Float(42.5).upcast() == 42.5
    assert type(Float(42.5).upcast()) is float
