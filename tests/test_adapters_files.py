"""Model files: listing, copying templates, saving (M2 AK 4)."""

import hashlib
from pathlib import Path

import pytest

from app.adapters import files, settings
from app.errors import InputError

ROOT = Path(__file__).resolve().parent.parent
T2 = ROOT / "examples" / "t2_terminplan.yaml"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_dirs_follow_environment(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("RISK_PILOT_DATA_DIR", str(tmp_path))
    assert settings.models_dir() == tmp_path / "models"
    assert settings.runs_dir() == tmp_path / "runs"
    assert (settings.examples_dir() / "t1_faltung.yaml").is_file()


def test_copy_keeps_source_bytes_and_sets_new_id(tmp_path: Path) -> None:
    before = sha(T2)
    target = files.copy_model(T2, tmp_path, "mein_plan")
    assert sha(T2) == before
    assert target == tmp_path / "mein_plan.yaml"
    model = files.load_model(target)
    assert model.model == "mein_plan"
    assert "# Tutorial T2" in target.read_text(encoding="utf-8")  # comments survive


def test_copy_never_overwrites(tmp_path: Path) -> None:
    files.copy_model(T2, tmp_path, "plan")
    with pytest.raises(InputError) as exc:
        files.copy_model(T2, tmp_path, "plan")
    assert exc.value.issue.code == "files.exists"
    assert exc.value.issue.params["suggestion"] == "plan_2"


def test_copy_rejects_invalid_id(tmp_path: Path) -> None:
    with pytest.raises(InputError) as exc:
        files.copy_model(T2, tmp_path, "Mein Plan")
    assert exc.value.issue.code == "node.id_invalid"


def test_suggest_id() -> None:
    assert files.suggest_id("plan", set()) == "plan"
    assert files.suggest_id("plan", {"plan", "plan_2"}) == "plan_3"


def test_list_models_sorted(tmp_path: Path) -> None:
    files.copy_model(T2, tmp_path, "b_plan")
    files.copy_model(T2, tmp_path, "a_plan")
    assert [p.stem for p in files.list_models(tmp_path)] == ["a_plan", "b_plan"]
    assert files.list_models(tmp_path / "missing") == []


def test_save_is_atomic_and_detects_external_change(tmp_path: Path) -> None:
    path = files.copy_model(T2, tmp_path, "plan")
    opened = files.text_hash(files.read_text(path))
    files.save_model_text(path, "neu\n", expected_hash=opened)
    assert path.read_text(encoding="utf-8") == "neu\n"
    assert not list(tmp_path.glob("*.tmp"))
    with pytest.raises(InputError) as exc:
        files.save_model_text(path, "anders\n", expected_hash=opened)
    assert exc.value.issue.code == "files.changed"


def test_create_model_text_exclusive(tmp_path: Path) -> None:
    text = "schema_version: 1\nmodel: alt\nnodes:\n  y: {type: output, expr: '1'}\n"
    path = files.create_model_text(tmp_path, "neu", text)
    assert files.load_model(path).model == "neu"
    with pytest.raises(InputError):
        files.create_model_text(tmp_path, "neu", text)


def test_copy_records_its_template() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        copy = files.copy_model(T2, Path(tmp), "plan")
        again = files.copy_model(copy, Path(tmp), "plan_b")
        assert files.template_of(files.read_text(copy)) == "t2_terminplan"
        assert files.template_of(files.read_text(again)) == "t2_terminplan"
    assert files.template_of(files.read_text(T2)) is None


def test_csv_column_reads_numbers_skips_blanks() -> None:
    data = b"datum;dauer;notiz\n2026-01-01;3,5;a\n2026-01-02;;b\n2026-01-03;4;c\n"
    assert files.csv_columns(data) == ["datum", "dauer", "notiz"]
    assert files.csv_column(data, "dauer") == ([3.5, 4.0], 1)
    comma = b"x,y\n1.5,2\n2.5,3\n"
    assert files.csv_column(comma, "x") == ([1.5, 2.5], 0)


def test_csv_column_reports_line_of_bad_number() -> None:
    with pytest.raises(InputError) as exc:
        files.csv_column(b"x\n1\nzwei\n", "x")
    assert exc.value.issue.code == "csv.number"
    assert exc.value.issue.line == 3
    with pytest.raises(InputError) as exc:
        files.csv_column(b"x\n1\n", "y")
    assert exc.value.issue.code == "csv.column"


@pytest.mark.parametrize("cell", ["nan", "inf", "-Infinity"])
def test_csv_column_rejects_non_finite(cell: str) -> None:
    with pytest.raises(InputError) as exc:
        files.csv_column(f"x\n1\n{cell}\n".encode(), "x")
    assert exc.value.issue.code == "csv.number"
    assert exc.value.issue.line == 3


def test_csv_in_another_encoding_is_reported() -> None:
    data = "größe\n1\n".encode("latin-1")
    with pytest.raises(InputError) as exc:
        files.csv_columns(data)
    assert exc.value.issue.code == "csv.encoding"
