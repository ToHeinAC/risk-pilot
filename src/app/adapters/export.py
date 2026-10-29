"""Raw samples of a run as Parquet bytes (M6 AK 4); pyarrow writes into a memory buffer."""

# pyarrow ships without type stubs; its members are untyped for pyright.
# pyright: reportMissingTypeStubs=false, reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false, reportUnknownArgumentType=false
import io

import pyarrow as pa
import pyarrow.parquet as pq

from app.engine.simulate import SimulationResult

META_KEYS = ("model_id", "model_hash", "n", "seed", "generator", "risk_pilot", "timestamp")


def samples_parquet(result: SimulationResult, scenario: str) -> bytes:
    """One column per kept node; model hash, N, seed and scenario in the schema metadata."""
    table = pa.table({name: values for name, values in result.samples.items()})
    meta = {k: str(result.meta[k]) for k in META_KEYS if k in result.meta}
    table = table.replace_schema_metadata({**meta, "scenario": scenario})
    out = io.BytesIO()
    pq.write_table(table, out)
    return out.getvalue()
