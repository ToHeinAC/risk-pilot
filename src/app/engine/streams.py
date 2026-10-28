"""One independent random stream per node, derived from the run seed and the node ID."""

import hashlib

import numpy as np
from numpy.typing import NDArray

STREAM_DERIVATION = "sha256-spawn-key-v1"
GENERATOR = "PCG64"
_SMALLEST = 2.0**-53


def stream_key(node_id: str) -> int:
    """First 8 bytes of SHA-256 over the UTF-8 node ID, big-endian."""
    return int.from_bytes(hashlib.sha256(node_id.encode("utf-8")).digest()[:8], "big")


def uniforms(seed: int, node_id: str, n: int) -> NDArray[np.float64]:
    """Exactly ``n`` uniforms in the open interval (0, 1) for one node."""
    sequence = np.random.SeedSequence(entropy=seed, spawn_key=(stream_key(node_id),))
    u = np.random.Generator(np.random.PCG64(sequence)).random(n)
    u[u == 0.0] = _SMALLEST
    return u
