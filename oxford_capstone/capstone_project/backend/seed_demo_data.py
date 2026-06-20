"""
Seed SQLite with demo tickets and chat messages for DB RAG and agent demos.

Usage (from capstone_project/):
  python -m backend.seed_demo_data --reset
"""

from __future__ import annotations

import argparse
from typing import Any, Dict, List

import backend.env_bootstrap  # noqa: F401 — load backend/.env

from sqlalchemy.orm import Session

from backend.database import SessionLocal, create_message, create_ticket, init_db
from backend.database.models import Message, Ticket

DEMO_TICKETS: List[Dict[str, str]] = [
    {
        "title": "VPN error 422 on Mac",
        "description": (
            "Cisco AnyConnect shows error 422 when connecting from home. "
            "User restarted the app and cleared MFA cache; issue persists after macOS update."
        ),
        "priority": "HIGH",
        "category": "NETWORK",
        "user_email": "alice.smith@oxforduniversity.com",
        "session_id": "demo-session-vpn",
    },
    {
        "title": "WiFi drops in Bodleian Library",
        "description": (
            "Laptop disconnects from eduroam every 10–15 minutes on Level 2. "
            "Other devices on the same network work fine."
        ),
        "priority": "MEDIUM",
        "category": "NETWORK",
        "user_email": "bob.jones@oxforduniversity.com",
        "session_id": "demo-session-wifi",
    },
    {
        "title": "Password reset — account locked",
        "description": (
            "User exceeded password attempts and is locked out of SSO. "
            "Needs self-service reset at password.oxforduniversity.com."
        ),
        "priority": "HIGH",
        "category": "PASSWORD",
        "user_email": "carol.lee@oxforduniversity.com",
        "session_id": "demo-session-password",
    },
    {
        "title": "New laptop setup for research fellow",
        "description": (
            "Day-one checklist: BitLocker, eduroam profile, VPN client, "
            "Microsoft 365, and approved research software."
        ),
        "priority": "LOW",
        "category": "HARDWARE",
        "user_email": "dan.patel@oxforduniversity.com",
        "session_id": "demo-session-laptop",
    },
    {
        "title": "Request: install MATLAB",
        "description": (
            "User needs MATLAB for a course. Software install policy requires "
            "manager approval and ticket before deployment via SCCM."
        ),
        "priority": "MEDIUM",
        "category": "SOFTWARE",
        "user_email": "emma.wright@oxforduniversity.com",
        "session_id": "demo-session-software",
    },
    {
        "title": "Shared drive access for project folder",
        "description": (
            "User cannot open \\\\files.oxford\\research-shared. "
            "Needs read/write access for the climate-modelling group."
        ),
        "priority": "MEDIUM",
        "category": "ACCESS",
        "user_email": "frank.nguyen@oxforduniversity.com",
        "session_id": "demo-session-access",
    },
]

DEMO_MESSAGES: List[Dict[str, str]] = [
    {
        "session_id": "demo-session-vpn",
        "role": "user",
        "content": "I'm getting VPN error 422 when I try to connect from my Mac.",
    },
    {
        "session_id": "demo-session-vpn",
        "role": "assistant",
        "content": (
            "Error 422 usually means the MFA prompt timed out. Close AnyConnect, "
            "wait 30 seconds, reopen, and respond to Duo within 60 seconds."
        ),
    },
    {
        "session_id": "demo-session-wifi",
        "role": "user",
        "content": "My WiFi keeps dropping in the library on eduroam.",
    },
    {
        "session_id": "demo-session-wifi",
        "role": "assistant",
        "content": (
            "Try forgetting eduroam and re-joining with your Oxford credentials. "
            "If it persists, note your MAC address for a network ticket."
        ),
    },
    {
        "session_id": "demo-session-password",
        "role": "user",
        "content": "I'm locked out after too many password attempts.",
    },
    {
        "session_id": "demo-session-password",
        "role": "assistant",
        "content": (
            "Use the self-service portal at password.oxforduniversity.com. "
            "If still locked, IT can unlock after identity verification."
        ),
    },
    {
        "session_id": "demo-session-software",
        "role": "user",
        "content": "How do I get MATLAB installed on my work laptop?",
    },
    {
        "session_id": "demo-session-software",
        "role": "assistant",
        "content": (
            "MATLAB is on the approved list but needs a ticket and manager approval "
            "before SCCM deployment."
        ),
    },
]


def clear_demo_data(db: Session) -> Dict[str, int]:
    """Remove all tickets and messages (demo reset)."""
    ticket_count = db.query(Ticket).count()
    message_count = db.query(Message).count()
    db.query(Message).delete()
    db.query(Ticket).delete()
    db.commit()
    return {"tickets": ticket_count, "messages": message_count}


def seed_demo_data(db: Session, *, reset: bool = False) -> Dict[str, int]:
    """
    Insert demo tickets and messages. Skips insert when rows already exist unless reset=True.
    """
    if reset:
        clear_demo_data(db)
    elif db.query(Ticket).count() > 0:
        return {"tickets": 0, "messages": 0, "skipped": True}

    for row in DEMO_TICKETS:
        create_ticket(
            db,
            title=row["title"],
            description=row["description"],
            priority=row["priority"],
            category=row["category"],
            user_email=row["user_email"],
            session_id=row.get("session_id"),
        )

    for row in DEMO_MESSAGES:
        create_message(
            db,
            session_id=row["session_id"],
            role=row["role"],
            content=row["content"],
        )

    return {"tickets": len(DEMO_TICKETS), "messages": len(DEMO_MESSAGES)}


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed demo tickets and messages for DB RAG")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Clear existing tickets/messages before seeding",
    )
    args = parser.parse_args()

    init_db()
    db = SessionLocal()
    try:
        result = seed_demo_data(db, reset=args.reset)
    finally:
        db.close()

    if result.get("skipped"):
        print("Demo data already present — use --reset to replace.")
        return

    print(f"Seeded {result['tickets']} tickets and {result['messages']} messages.")


if __name__ == "__main__":
    main()
