"""Help overlay showing keyboard shortcuts."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import ModalScreen
from textual.widgets import Label, Static


SHORTCUTS = [
    ("Navigation", [
        ("d", "Dashboard"),
        ("a", "Assets"),
        ("p", "Plugins"),
        ("Esc", "Back / Close"),
    ]),
    ("Actions", [
        ("/", "Search"),
        ("v", "Validate"),
        ("f", "Filter (in Assets)"),
        ("n", "New Plugin (in Plugins)"),
    ]),
    ("General", [
        ("?", "This help"),
        ("q", "Quit"),
        ("Tab", "Next pane"),
        ("Enter", "Select / Confirm"),
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
            yield Label("[bold]Keyboard Shortcuts[/]\n")

            for section, shortcuts in SHORTCUTS:
                yield Label(f"[bold cyan]{section}[/]", classes="help-title")
                for key, desc in shortcuts:
                    yield Label(f"  [bold]{key:12}[/] {desc}")
                yield Label("")

            yield Label("[dim]Press Esc or ? to close[/]")

    def action_close(self) -> None:
        """Close the help overlay."""
        self.dismiss()

    def on_key(self, event) -> None:
        """Close on any key."""
        self.dismiss()
