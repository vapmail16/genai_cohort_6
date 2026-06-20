"""Tests for demo SQLite seed data used by DB RAG and agent flows."""

from backend.database.models import Message, Ticket
from backend.seed_demo_data import (
    DEMO_MESSAGES,
    DEMO_TICKETS,
    clear_demo_data,
    seed_demo_data,
)


def test_seed_demo_data_creates_tickets_and_messages(db_session):
    result = seed_demo_data(db_session)

    assert result["tickets"] == len(DEMO_TICKETS)
    assert result["messages"] == len(DEMO_MESSAGES)
    assert db_session.query(Ticket).count() == len(DEMO_TICKETS)
    assert db_session.query(Message).count() == len(DEMO_MESSAGES)


def test_seed_demo_data_is_idempotent_without_reset(db_session):
    first = seed_demo_data(db_session)
    second = seed_demo_data(db_session)

    assert first["tickets"] == len(DEMO_TICKETS)
    assert second["tickets"] == 0
    assert second["messages"] == 0
    assert db_session.query(Ticket).count() == len(DEMO_TICKETS)


def test_clear_demo_data_removes_all_rows(db_session):
    seed_demo_data(db_session)
    removed = clear_demo_data(db_session)

    assert removed["tickets"] == len(DEMO_TICKETS)
    assert removed["messages"] == len(DEMO_MESSAGES)
    assert db_session.query(Ticket).count() == 0
    assert db_session.query(Message).count() == 0


def test_seed_demo_data_reset_replaces_existing(db_session):
    seed_demo_data(db_session)
    result = seed_demo_data(db_session, reset=True)

    assert result["tickets"] == len(DEMO_TICKETS)
    assert db_session.query(Ticket).count() == len(DEMO_TICKETS)


def test_demo_tickets_cover_rag_themes():
    titles = " ".join(t["title"] for t in DEMO_TICKETS).lower()
    assert "vpn" in titles
    assert "password" in titles or "wifi" in titles
