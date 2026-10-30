"""Write form edits back into the YAML text, pure (no file I/O).

The text is read with ruamel.yaml in round-trip mode and its tree is aligned with the wanted
data: changed values are replaced, new keys appended, removed keys deleted, everything else is
left alone. Comments, key order, flow style and quotes of untouched parts stay (M6 E4).
"""

# ruamel.yaml's comment containers are only partly typed for pyright.
# pyright: reportUnknownMemberType=false, reportUnknownVariableType=false
# pyright: reportUnknownArgumentType=false
import difflib
import io
import re
from itertools import pairwise
from typing import Any, cast

import yaml
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap, CommentedSeq
from ruamel.yaml.error import YAMLError
from ruamel.yaml.scalarstring import DoubleQuotedScalarString

from app.errors import InputError, Issue

Data = dict[str, Any]


_ITEM = re.compile(r"^( *)- ")
_KEY = re.compile(r"^( *)[^\s#-][^:]*:\s*$")
_SPACE = re.compile(r"\s+")
_WRAP = 4  # at most this many old lines are joined into one new line


def _offset(text: str) -> int:
    """Indent of block-list dashes below their key: 2 (``  - a``) or 0 (``- a``)."""
    lines = text.splitlines()
    for before, line in pairwise(lines):
        key, item = _KEY.match(before), _ITEM.match(line)
        if key and item:
            return 2 if len(item.group(1)) > len(key.group(1)) else 0
    return 2


def _yaml(text: str = "") -> YAML:
    yaml = YAML()  # round-trip mode
    yaml.preserve_quotes = True
    yaml.width = 4096  # never re-wrap long flow lines
    offset = _offset(text)
    yaml.indent(mapping=2, sequence=offset + 2, offset=offset)
    return yaml


def _flat(lines: list[str]) -> str:
    return _SPACE.sub(" ", " ".join(lines)).strip()


def _span(old: list[str], i: int, line: str) -> int:
    """How many old lines from ``i`` say the same as ``line`` apart from spacing and wrapping."""
    for k in range(1, _WRAP + 1):
        if i + k <= len(old) and _flat(old[i : i + k]) == _flat([line]):
            return k
    return 0


def _restore(old: list[str], new: list[str]) -> list[str]:
    out: list[str] = []
    i = 0
    for line in new:
        k = _span(old, i, line)
        out += old[i : i + k] if k else [line]
        i += k or 1
    return out


def _keep_layout(old: str, new: str) -> str:
    """Changed regions keep the original spacing and line wrapping where the content is equal."""
    a, b = old.splitlines(keepends=True), new.splitlines(keepends=True)
    out: list[str] = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_opcodes():
        out += _restore(a[i1:i2], b[j1:j2]) if tag == "replace" else b[j1:j2]
    return "".join(out)


def _plain(value: Any) -> Any:
    """ruamel's scalar and container types as plain Python values."""
    if isinstance(value, dict):
        return {str(k): _plain(v) for k, v in cast(dict[Any, Any], value).items()}
    if isinstance(value, list):
        return [_plain(v) for v in cast(list[Any], value)]
    if isinstance(value, bool) or value is None:
        return value
    for kind in (int, float, str):
        if isinstance(value, kind):
            return kind(value)
    return value  # pragma: no cover - YAML has no other scalar types here


def _tree(text: str) -> CommentedMap:
    try:
        tree = _yaml().load(text)
    except YAMLError:
        tree = None
    if not isinstance(tree, CommentedMap):
        raise InputError(Issue("form.no_mapping"))
    return tree


def load_data(text: str) -> Data:
    """The YAML mapping as plain data; the form works on it, valid model or not."""
    return cast(Data, _plain(_tree(text)))


def _new(value: Any, flow: bool) -> Any:
    """A fresh container for ``value``; inside a flow-style parent it is flow style too, and so
    is a list of plain values (``[220, 0]``)."""
    if isinstance(value, dict):
        made = CommentedMap((k, _new(v, flow)) for k, v in cast(Data, value).items())
    elif isinstance(value, list):
        items = cast(list[Any], value)
        made = CommentedSeq(_new(v, flow) for v in items)
        flow = flow or not any(isinstance(v, dict | list) for v in items)
    else:
        return _quoted_if_needed(value)
    if flow:
        made.fa.set_flow_style()
    return made


def _quoted_if_needed(value: Any) -> Any:
    """Strings the app (PyYAML, YAML 1.1) would read as something else get quotes: ``on``,
    ``No``, ``1:30``. ruamel writes YAML 1.2 and would leave them bare."""
    if not isinstance(value, str):
        return value
    try:
        same = yaml.safe_load(value) == value
    except yaml.YAMLError:
        same = False
    return value if same else DoubleQuotedScalarString(value)


def _flow(node: CommentedMap | CommentedSeq) -> bool:
    return bool(node.fa.flow_style())


def _siblings_flow(node: CommentedMap) -> bool:
    """New entries copy the style of the existing ones (``nodes: {a: {...}}`` per line)."""
    children = [v for v in node.values() if isinstance(v, CommentedMap | CommentedSeq)]
    return bool(children) and all(_flow(c) for c in children)


def _merge_map(node: CommentedMap, want: Data) -> CommentedMap:
    for key in [k for k in node if k not in want]:
        del node[key]
    if not node and want and _flow(node):
        node.fa.set_block_style()  # ``nodes: {}`` grows into one block entry per line
    flow = _flow(node) or _siblings_flow(node)
    for key, value in want.items():
        if key in node:
            merged = _merge(node[key], value)
            if merged is not node[key]:
                node[key] = merged
        else:
            node[key] = _new(value, flow)
    return node


def _merge_seq(node: CommentedSeq, items: list[Any]) -> CommentedSeq:
    """Items aligned in place, so comments on the kept items and after the list stay."""
    flow = _flow(node) or (bool(node) and all(_is_flow(v) for v in node))
    for i, value in enumerate(items[: len(node)]):
        merged = _merge(node[i], value)
        if merged is not node[i]:
            node[i] = merged
    for value in items[len(node) :]:
        node.append(_new(value, flow))
    while len(node) > len(items):
        del node[len(node) - 1]  # pop() shifts ruamel's comment indices wrongly
    return node


def _is_flow(value: Any) -> bool:
    return isinstance(value, CommentedMap | CommentedSeq) and _flow(value)


def _merge(node: Any, want: Any) -> Any:
    """``node`` aligned with ``want``; the same object when nothing changed."""
    if isinstance(node, CommentedMap) and isinstance(want, dict):
        return _merge_map(node, cast(Data, want))
    if isinstance(node, CommentedSeq) and isinstance(want, list):
        return _merge_seq(node, cast(list[Any], want))
    return node if _same_scalar(_plain(node), want) else _new(want, False)


def _same_scalar(have: Any, want: Any) -> bool:
    """Equal values; 15 and 15.0 are the same number, but True is not 1."""
    numbers = (int, float)
    if isinstance(have, numbers) and isinstance(want, numbers):
        return isinstance(have, bool) == isinstance(want, bool) and have == want
    return type(have) is type(want) and have == want


def patch(text: str, data: Data) -> str:
    """``text`` changed so that it reads back as ``data``; untouched parts stay as they were."""
    if load_data(text) == data:
        return text
    tree = _merge_map(_tree(text), data)
    out = io.StringIO()
    _yaml(text).dump(tree, out)
    dumped = out.getvalue()
    for result in (_keep_layout(text, dumped), dumped):
        if load_data(result) == data:
            return result
    raise InputError(Issue("form.patch_failed"))  # pragma: no cover - guard against silent loss
