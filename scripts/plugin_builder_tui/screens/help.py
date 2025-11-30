"""Help overlay showing keyboard shortcuts."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import ModalScreen
from textual.widgets import Label, Static


SHORTCUTS = [
    ("Navigation", [
        ("d", "Go to Dashboard"),
        ("p", "Go to Plugins"),
        ("a", "Go to Assets"),
        ("Esc", "Back / Close modal"),
    ]),
    ("Plugin Management", [
        ("a", "Add asset to plugin (in Plugins)"),
        ("r", "Remove asset from plugin (in Plugins)"),
        ("n", "New plugin (CLI only)"),
        ("v", "Validate all symlinks"),
    ]),
    ("Search & Filter", [
        ("/", "Open search overlay"),
        ("Ctrl+F", "Search (alternative)"),
        ("f", "Focus filter input (in Assets)"),
        ("Esc", "Clear filter (in Assets)"),
    ]),
    ("General", [
        ("?", "Show this help"),
        ("q", "Quit application"),
        ("Tab", "Navigate between panes"),
        ("Enter", "Select / Confirm"),
        ("Delete", "Delete asset (in Assets)"),
    ]),
]


class HelpScreen(ModalScreen):
    """Modal help overlay."""

    BINDINGS = [
        ("escape", "close", "Close"),
        ("question_mark", "close", "Close"),
    ]

    def compose(self) -> ComposeResult:
        with Container(id="help-overlay"):
            yield Label("[bold]Plugin Builder - Keyboard Shortcuts[/]\n")

            for section, shortcuts in SHORTCUTS:
                yield Label(f"[bold cyan]{section}[/]", classes="help-title")
                for key, desc in shortcuts:
                    yield Label(f"  [bold cyan]{key:15}[/] {desc}")
                yield Label("")

            yield Label("\n[dim italic]Press Esc or any key to close[/]")

    def action_close(self) -> None:
        """Close the help overlay."""
        self.dismiss()

    def on_key(self, event) -> None:
        """Close on any key."""
        self.dismiss()
