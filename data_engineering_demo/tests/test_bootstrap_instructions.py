from __future__ import annotations

import sys

from de_demo.main import bootstrap_instructions_text, run_cli


def test_bootstrap_instructions_mentions_sql_file():
    txt = bootstrap_instructions_text()
    assert "bootstrap_local_roles.sql" in txt
    assert "pg_isready" in txt


def test_cli_prints_bootstrap_instructions(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["de_demo", "--bootstrap-instructions"])
    run_cli()
    assert "bootstrap_local_roles.sql" in capsys.readouterr().out
