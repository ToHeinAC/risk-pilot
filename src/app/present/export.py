"""Export of one run (M6 AK 4), pure: metrics as CSV text, a standalone HTML report.

The Parquet file of the raw samples needs pyarrow's writer and lives in ``adapters/export``.
"""

# plotly ships without type stubs; its members are untyped for pyright.
# pyright: reportUnknownMemberType=false, reportUnknownVariableType=false
# pyright: reportUnknownArgumentType=false, reportMissingTypeStubs=false
import csv
import html
import io
from collections.abc import Iterator, Mapping
from dataclasses import dataclass
from typing import Any

from plotly.offline import get_plotlyjs

from app.analysis.stats import Proportion, Summary
from app.engine.simulate import SimulationResult
from app.messages import t
from app.model.compile import CompiledModel
from app.present import figures
from app.present.results import correlation_rows
from app.present.text import (
    beyond_sentence,
    metric_rows,
    number,
    quantile_sentence,
    share_sentence,
    target_sentence,
    validity_line,
)

CSV_COLUMNS = (
    "model",
    "model_hash",
    "scenario",
    "n",
    "seed",
    "output",
    "metric",
    "label",
    "value",
    "lo",
    "hi",
    "se",
    "unit",
)
Row = dict[str, Any]


@dataclass(frozen=True)
class Report:
    compiled: CompiledModel
    result: SimulationResult
    summaries: Mapping[str, Summary]
    scenario: str  # the scenario's name as shown
    model_text: str
    scenario_id: str = "basis"  # machine-readable, as in the Parquet metadata


def quantile_key(q: float) -> str:
    """``p5``, ``p50``, ``p2.5``: English decimal point, never the German comma (E11)."""
    return f"p{q * 100:g}"


def file_name(model_id: str, scenario_id: str, kind: str) -> str:
    return f"{model_id}_{scenario_id}_{kind}"


def _proportion(metric: str, label: str, p: Proportion) -> Row:
    return {"metric": metric, "label": label, "value": p.p, "lo": p.lo, "hi": p.hi}


def _metric_rows(s: Summary) -> Iterator[Row]:
    """One row per metric, machine readable: English key, German label, plain floats."""
    if s.share is not None:
        yield _proportion("share", t("result.share_label"), s.share)
        return
    yield {"metric": "mean", "label": t("result.mean"), "value": s.mean, "se": s.se}
    yield {"metric": "sd", "label": t("result.sd"), "value": s.sd}
    yield {"metric": "median", "label": t("result.median"), "value": s.median}
    for q in s.quantiles:
        pct = number(q.q * 100)
        label = t("result.quantile_label", pct=pct)
        yield {
            "metric": quantile_key(q.q),
            "label": label,
            "value": q.value,
            "lo": q.lo,
            "hi": q.hi,
        }
    yield {"metric": "min", "label": t("result.min"), "value": s.min}
    yield {"metric": "max", "label": t("result.max"), "value": s.max}
    if s.target is not None:
        yield _proportion("p_target", t("result.target_label"), s.target)
    if s.beyond is not None:
        yield _proportion("p_beyond", t("result.beyond_label"), s.beyond)
    if s.loss is not None:
        var = s.loss.var
        yield _proportion("p_loss", t("result.p_loss"), s.loss.p_loss)
        yield {
            "metric": "var95",
            "label": t("result.var", pct="95"),
            "value": var.value,
            "lo": var.lo,
            "hi": var.hi,
        }
        es = s.loss
        yield {"metric": "es95", "label": t("result.es", pct="95"), "value": es.es, "se": es.es_se}


def metrics_csv(report: Report) -> str:
    """Comma separated, decimal point, UTF-8; one row per output and metric (E11)."""
    meta = report.result.meta
    out = io.StringIO()
    writer: csv.DictWriter[str] = csv.DictWriter(
        out, fieldnames=list(CSV_COLUMNS), restval="", lineterminator="\n"
    )
    writer.writeheader()
    for output, summary in report.summaries.items():
        unit = report.compiled.model.nodes[output].unit or ""
        fixed = {
            "model": meta["model_id"],
            "model_hash": meta["model_hash"],
            "scenario": report.scenario_id,
            "n": meta["n"],
            "seed": meta["seed"],
            "output": output,
            "unit": unit,
        }
        for row in _metric_rows(summary):
            writer.writerow({**fixed, **{k: _cell(v) for k, v in row.items()}})
    return out.getvalue()


def _cell(value: Any) -> Any:
    return "" if value is None else repr(value) if isinstance(value, float) else value


def _table(headers: list[str], rows: list[tuple[str, ...]]) -> str:
    head = "".join(f"<th>{html.escape(h)}</th>" for h in headers)
    body = "".join(
        "<tr>" + "".join(f"<td>{html.escape(c)}</td>" for c in row) + "</tr>" for row in rows
    )
    return f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"


def _sentences(report: Report, output: str) -> list[str]:
    """The same sentences in model language as on the result page."""
    summary, unit = report.summaries[output], report.compiled.model.nodes[output].unit
    if summary.share is not None:
        return [share_sentence(summary.share)]
    found: list[str] = []
    target = report.compiled.nodes[output].target
    if target is not None and summary.target is not None:
        found.append(target_sentence(target, summary.target, unit))
    if summary.horizon is not None and summary.beyond is not None:
        found.append(beyond_sentence(summary.horizon, summary.beyond, unit))
    found += [quantile_sentence(q, unit, summary.conf, summary.horizon) for q in summary.quantiles]
    return found


def _output_html(report: Report, output: str) -> str:
    node = report.compiled.model.nodes[output]
    summary = report.summaries[output]
    x = report.result.samples[output]
    parts = [f"<h2>{html.escape(node.name or output)}</h2>"]
    parts += [f"<p>{html.escape(text)}</p>" for text in _sentences(report, output)]
    parts.append(_table([t("ui.metric"), t("ui.value")], metric_rows(summary, node.unit)))
    if summary.share is None:
        for fig in (figures.histogram(x, node.unit, []), figures.cdf(x, node.unit, [])):
            parts.append(fig.to_html(full_html=False, include_plotlyjs=False))
    return "\n".join(parts)


STYLE = (
    "body{font-family:system-ui,sans-serif;max-width:60rem;margin:2rem auto;padding:0 1rem}"
    "table{border-collapse:collapse;margin:1rem 0}td,th{border:1px solid #ccc;padding:.3rem .6rem}"
    "pre{background:#f4f4f4;padding:1rem;overflow:auto}"
)


def report_html(report: Report) -> str:
    """One HTML file: validity, metrics, figures and correlations per output, the model text."""
    model = report.compiled.model
    title = html.escape(model.title or model.model)
    parts = [
        f"<h1>{title}</h1>",
        f"<p>{html.escape(validity_line(report.result.meta, report.scenario))}</p>",
    ]
    if model.illustrative:
        parts.append(f"<p><strong>{html.escape(t('lesson.illustrative'))}</strong></p>")
    corr = correlation_rows(report.compiled, report.result.correlations)
    if corr:
        headers = [t(f"result.corr_{k}") for k in ("group", "pair", "target", "achieved")]
        parts += [f"<h2>{html.escape(t('result.corr_title'))}</h2>", _table(headers, list(corr))]
    parts += [_output_html(report, output) for output in report.summaries]
    parts += [
        f"<h2>{html.escape(t('export.model_text'))}</h2>",
        f"<pre>{html.escape(report.model_text)}</pre>",
    ]
    body = "\n".join(parts)
    return (
        f'<!DOCTYPE html>\n<html lang="de"><head><meta charset="utf-8"><title>{title}</title>'
        f"<style>{STYLE}</style><script>{get_plotlyjs()}</script>"  # inline: works offline (E12)
        f"</head><body>\n{body}\n</body></html>\n"
    )
