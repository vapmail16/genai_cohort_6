"""Compose supplies credentials; connections default to local Postgres :5432."""

from __future__ import annotations

from pathlib import Path

import pytest

from de_demo import config

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_repo_compose_still_maps_host_5433(monkeypatch):
    """Published port in compose (Docker) is parseable; URL default is local 5432."""
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("WAREHOUSE_HOST_PORT", raising=False)
    user, password, db, published = config.warehouse_connection_from_compose(
        compose_package_root=REPO_ROOT
    )
    assert (user, password, db, published) == ("dedemo", "dedemo", "dedemo_wh", 5433)


def test_warehouse_url_defaults_to_local_listening_port(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("WAREHOUSE_HOST_PORT", raising=False)
    url = config.warehouse_url(compose_package_root=REPO_ROOT)
    assert "127.0.0.1:5432/dedemo_wh" in url


def test_warehouse_host_port_env_targets_docker_publish(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.setenv("WAREHOUSE_HOST_PORT", "5433")
    url = config.warehouse_url(compose_package_root=REPO_ROOT)
    assert "127.0.0.1:5433/dedemo_wh" in url


def test_custom_compose_publish_does_not_change_url_without_env(monkeypatch, tmp_path):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("WAREHOUSE_HOST_PORT", raising=False)
    (tmp_path / "docker-compose.yml").write_text(
        """services:
  warehouse:
    environment:
      POSTGRES_USER: x
      POSTGRES_PASSWORD: y
      POSTGRES_DB: z
    ports:
      - "6000:5432"
""",
        encoding="utf-8",
    )
    url = config.warehouse_url(compose_package_root=tmp_path)
    assert "127.0.0.1:5432/z" in url.replace("+", "+")


def test_custom_warehouse_host_port_env_overrides_default(monkeypatch, tmp_path):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.setenv("WAREHOUSE_HOST_PORT", "6000")
    (tmp_path / "docker-compose.yml").write_text(
        """services:
  warehouse:
    environment:
      POSTGRES_USER: x
      POSTGRES_PASSWORD: y
      POSTGRES_DB: z
    ports:
      - "6000:5432"
""",
        encoding="utf-8",
    )
    url = config.warehouse_url(compose_package_root=tmp_path)
    assert "127.0.0.1:6000/z" in url.replace("+", "+")


def test_raises_when_no_mapping_to_container_5432(monkeypatch, tmp_path):
    monkeypatch.setattr(config, "PACKAGE_ROOT", tmp_path)
    (tmp_path / "docker-compose.yml").write_text(
        """services:
  warehouse:
    environment:
      POSTGRES_USER: a
      POSTGRES_PASSWORD: b
      POSTGRES_DB: c
    ports:
      - "5433:5434"
""",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="5432"):
        config.warehouse_connection_from_compose()


def test_explicit_database_url_override(monkeypatch):
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql+psycopg2://u:p@localhost:9999/other",
    )
    assert config.warehouse_url() == "postgresql+psycopg2://u:p@localhost:9999/other"
