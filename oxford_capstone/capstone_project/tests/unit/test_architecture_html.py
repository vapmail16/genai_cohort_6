"""Regression tests for interactive MCP architecture HTML diagrams."""

from pathlib import Path

MCP_DIR = Path(__file__).resolve().parents[3] / "mcp"
ARCHITECTURE_FILES = [
    MCP_DIR / "MCPArchitecture.html",
    MCP_DIR / "ITSupportArchitecture.html",
]

PINNED_BABEL = "@babel/standalone@7."


def test_architecture_html_files_exist():
    for path in ARCHITECTURE_FILES:
        assert path.is_file(), f"Missing architecture diagram: {path}"


def test_architecture_html_pins_babel_standalone_v7():
    """Babel 8 on unpkg breaks automatic text/babel compilation (blank page)."""
    for path in ARCHITECTURE_FILES:
        html = path.read_text(encoding="utf-8")
        assert PINNED_BABEL in html, (
            f"{path.name} must pin @babel/standalone to v7; "
            "unpkg latest (v8) no longer auto-compiles text/babel scripts."
        )
        assert "unpkg.com/@babel/standalone/babel.min.js" not in html
