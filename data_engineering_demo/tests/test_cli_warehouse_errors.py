"""CLI exits 1 with a short message when Postgres is unreachable (no long traceback)."""

from __future__ import annotations

import sys
from unittest.mock import patch

import pytest
from sqlalchemy.exc import OperationalError

from de_demo import main


def test_cli_exits_1_on_operational_error(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["de_demo", "--rows", "10"])
    err = OperationalError("statement", {}, None)
    err.__cause__ = None
    with patch("de_demo.main.run_pipeline", side_effect=err):
        with pytest.raises(SystemExit) as exc:
            main.run_cli()
    assert exc.value.code == 1
    err_out = capsys.readouterr().err
    assert "bootstrap-instructions" in err_out
    assert "pg_isready" in err_out


def test_cli_init_warehouse_handles_operational_error(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["de_demo", "--init-warehouse-only"])
    err = OperationalError("statement", {}, None)
    with patch("de_demo.main.ensure_database_objects", side_effect=err):
        with pytest.raises(SystemExit) as exc:
            main.run_cli()
    assert exc.value.code == 1
    err_out = capsys.readouterr().err
    assert "bootstrap_local_roles.sql" in err_out
