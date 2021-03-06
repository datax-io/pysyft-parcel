"""Beaver Triples Protocol.

D. Beaver. *Efficient multiparty protocols using circuit randomization*.
In J. Feigenbaum, editor, CRYPTO, volume **576** of Lecture Notes in
Computer Science, pages 420–432. Springer, 1991.
"""


# stdlib
import operator
import secrets
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple

# third party
import numpy as np

# relative
from ....tensor.smpc.mpc_tensor import MPCTensor
from ....tensor.smpc.share_tensor import ShareTensor
from ...store import register_primitive_generator
from ...store import register_primitive_store_add
from ...store import register_primitive_store_get
from ...store.exceptions import EmptyPrimitiveStore

ttp_generator = np.random.default_rng()


def _get_triples(
    op_str: str,
    nr_parties: int,
    a_shape: Tuple[int],
    b_shape: Tuple[int],
    ring_size: int = 2 ** 32,
    **kwargs: Dict[Any, Any],
) -> Tuple[Tuple[Tuple[ShareTensor, ShareTensor, ShareTensor]]]:
    """Get triples.

    The Trusted Third Party (TTP) or Crypto Provider should provide this triples Currently,
    the one that orchestrates the communication provides those triples.".

    Args:
        op_str (str): Operator string.
        nr_parties (int): Number of parties
        a_shape (Tuple[int]): Shape of a from beaver triples protocol.
        b_shape (Tuple[int]): Shape of b part from beaver triples protocol.
        ring_size (int) : Ring Size of the triples to generate.
        kwargs: Arbitrary keyword arguments for commands.

    Returns:
        List[List[3 x List[ShareTensor, ShareTensor, ShareTensor]]]:
        The generated triples a,b,c for each party.

    Raises:
        ValueError: If the triples are not consistent.
        ValueError: If the share class is invalid.
    """
    # relative
    from ..... import Tensor

    cmd = getattr(operator, op_str)
    min_value, max_value = ShareTensor.compute_min_max_from_ring(ring_size)
    seed_shares = secrets.randbits(32)

    a_rand = Tensor(
        ttp_generator.integers(
            low=min_value, high=max_value, size=a_shape, endpoint=True, dtype=np.int32
        )
    )
    a_shares = MPCTensor._get_shares_from_local_secret(
        secret=a_rand,
        nr_parties=nr_parties,
        shape=a_shape,
        seed_shares=seed_shares,
    )

    b_rand = Tensor(
        ttp_generator.integers(
            low=min_value, high=max_value, size=b_shape, endpoint=True, dtype=np.int32
        )
    )

    b_shares = MPCTensor._get_shares_from_local_secret(
        secret=b_rand,
        nr_parties=nr_parties,
        shape=b_shape,
        seed_shares=seed_shares,
    )

    c_val = cmd(a_rand, b_rand, **kwargs)

    c_shares = MPCTensor._get_shares_from_local_secret(
        secret=c_val, nr_parties=nr_parties, shape=c_val.shape, seed_shares=seed_shares
    )

    # We are always creating an instance
    triple_sequential = [(a_shares, b_shares, c_shares)]

    """
    Example -- for n_instances=2 and n_parties=2:
    For Beaver Triples the "res" would look like:
    res = [
        ([a0_sh_p0, a0_sh_p1], [b0_sh_p0, b0_sh_p1], [c0_sh_p0, c0_sh_p1]),
        ([a1_sh_p0, a1_sh_p1], [b1_sh_p0, b1_sh_p1], [c1_sh_p0, c1_sh_p1])
    ]

    We want to send to each party the values they should hold:
    primitives = [
        [[a0_sh_p0, b0_sh_p0, c0_sh_p0], [a1_sh_p0, b1_sh_p0, c1_sh_p0]], # (Row 0)
        [[a0_sh_p1, b0_sh_p1, c0_sh_p1], [a1_sh_p1, b1_sh_p1, c1_sh_p1]]  # (Row 1)
    ]

    The first party (party 0) receives Row 0 and the second party (party 1) receives Row 1
    """

    triple = list(
        map(list, zip(*map(lambda x: map(list, zip(*x)), triple_sequential)))  # type: ignore
    )

    return triple  # type: ignore


# Beaver Operations defined for Multiplication


@register_primitive_generator("beaver_mul")
def get_triples_mul(
    *args: List[Any], **kwargs: Dict[Any, Any]
) -> Tuple[Tuple[Tuple[ShareTensor, ShareTensor, ShareTensor]]]:
    """Get the beaver triples for the multiplication operation.

    Args:
        *args (List[ShareTensor]): Named arguments of :func:`beaver.__get_triples`.
        **kwargs (List[ShareTensor]): Keyword arguments of :func:`beaver.__get_triples`.

    Returns:
        Tuple[Tuple[ShareTensor, ShareTensor, ShareTensor]]: The generated triples a,b,c
        for the mul operation.
    """
    return _get_triples("mul", *args, **kwargs)  # type: ignore


@register_primitive_store_add("beaver_mul")
def mul_store_add(
    store: Dict[str, List[Any]],
    primitives: List[Any],
    a_shape: Tuple[int],
    b_shape: Tuple[int],
) -> None:
    """Add the primitives required for the "mul" operation to the CryptoStore.

    Arguments:
        store (Dict[str, List[Any]]): the CryptoStore
        primitives (List[Any]): the list of primitives
        a_shape (Tuple[int]): the shape of the first operand
        b_shape (Tuple[int]): the shape of the second operand
    """
    config_key = f"beaver_mul_{a_shape}_{b_shape}"
    if config_key in store:
        store[config_key].extend(primitives)
    else:
        store[config_key] = primitives


@register_primitive_store_get("beaver_mul")
def mul_store_get(
    store: Dict[str, List[Any]],
    a_shape: Tuple[int, ...],
    b_shape: Tuple[int, ...],
    remove: bool = True,
) -> Any:
    """Retrieve the primitives from the CryptoStore.

    Those are needed for executing the "mul" operation.

    Args:
        store (Dict[str, List[Any]]): The CryptoStore.
        a_shape (Tuple[int]): The shape of the first operand.
        b_shape (Tuple[int]): The shape of the second operand.
        remove (bool): True if the primitives should be removed from the store.

    Returns:
        Any: The primitives required for the "mul" operation.

    Raises:
        EmptyPrimitiveStore: If no primitive in the store for config_key.
    """
    config_key = f"beaver_mul_{tuple(a_shape)}_{tuple(b_shape)}"

    try:
        primitives = store[config_key]
    except KeyError:
        raise EmptyPrimitiveStore(f"{config_key} does not exists in the store")

    try:
        primitive = primitives[0]
    except Exception:
        raise EmptyPrimitiveStore(f"No primitive in the store for {config_key}")

    if remove:
        del primitives[0]

    return primitive


# Beaver Operations defined for Matrix Multiplication


@register_primitive_generator("beaver_matmul")
def get_triples_matmul(
    *args: List[Any], **kwargs: Dict[Any, Any]
) -> Tuple[List[ShareTensor], List[ShareTensor], List[ShareTensor]]:
    """Get the beaver triples for the matmul  operation.

    Args:
        *args (List[ShareTensor]): Named arguments of :func:`beaver.__get_triples`.
        **kwargs (List[ShareTensor]): Keyword arguments of :func:`beaver.__get_triples`.

    Returns:
        Tuple[Tuple[ShareTensor, ShareTensor, ShareTensor]]: The generated triples a,b,c
        for the matmul operation.
    """
    return _get_triples("matmul", *args, **kwargs)  # type: ignore


@register_primitive_store_add("beaver_matmul")
def matmul_store_add(
    store: Dict[str, List[Any]],
    primitives: List[Any],
    a_shape: Tuple[int],
    b_shape: Tuple[int],
) -> None:
    """Add the primitives required for the "matmul" operation to the CryptoStore.

    Args:
        store (Dict[str, List[Any]]): The CryptoStore.
        primitives (List[Any]): The list of primitives
        a_shape (Tuple[int]): The shape of the first operand.
        b_shape (Tuple[int]): The shape of the second operand.

    """
    config_key = f"beaver_matmul_{a_shape}_{b_shape}"
    if config_key in store:
        store[config_key].extend(primitives)
    else:
        store[config_key] = primitives


@register_primitive_store_get("beaver_matmul")
def matmul_store_get(
    store: Dict[str, List[Any]],
    a_shape: Tuple[int, ...],
    b_shape: Tuple[int, ...],
    remove: bool = True,
) -> Any:
    """Retrieve the primitives from the CryptoStore.

    Those are needed for executing the "matmul" operation.

    Args:
        store (Dict[str, List[Any]]): The CryptoStore.
        a_shape (Tuple[int]): The shape of the first operand.
        b_shape (Tuple[int]): The shape of the second operand.
        remove (bool): True if the primitives should be removed from the store.

    Returns:
        Any: The primitives required for the "matmul" operation.

    Raises:
        EmptyPrimitiveStore: If no primitive in the store for config_key.
    """
    config_key = f"beaver_matmul_{tuple(a_shape)}_{tuple(b_shape)}"

    try:
        primitives = store[config_key]
    except KeyError:
        raise EmptyPrimitiveStore(f"{config_key} does not exists in the store")

    try:
        primitive = primitives[0]
    except Exception:
        raise EmptyPrimitiveStore(f"No primitive in the store for {config_key}")

    if remove:
        del primitives[0]

    return primitive
