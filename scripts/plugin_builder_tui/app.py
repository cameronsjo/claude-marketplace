"""
Main Textual App for Plugin Builder TUI.
"""

from pathlib import Path
from typing import Optional

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer, Header

from .builder import PluginBuilder
from .screens.assets import AssetsScreen
from .screens.dashboard import DashboardScreen
from .screens.help import HelpScreen
from .screens.plugins import PluginsScreen
from .screens.search import SearchScreen


class PluginBuilderApp(App):
    """A TUI for managing Claude Code marketplace plugins."""

    TITLE = "Plugin Builder"
    SUB_TITLE = "Claude Code Marketplace"
    CSS_PATH = "styles.tcss"

    BINDINGS = [
        Binding("q", "quit", "Quit", show=True),
        Binding("?", "help", "Help", show=True),
        Binding("f1", "help", "Help", show=False),
        Binding("slash", "search", "Search", show=True),
        Binding("ctrl+f", "search", "Search", show=False),
        Binding("d", "dashboard", "Dashboard", show=True),
        Binding("a", "assets", "Assets", show=True),
        Binding("p", "plugins", "Plugins", show=True),
        Binding("v", "validate", "Validate", show=True),
        Binding("escape", "back", "Back", show=False),
    ]

    SCREENS = {
        "dashboard": DashboardScreen,
        "assets": AssetsScreen,
        "plugins": PluginsScreen,
    }

    def __init__(
        self,
        marketplace_root: Optional[Path] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.builder = PluginBuilder(marketplace_root)
        self._current_main_screen = "dashboard"

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Header()
        yield Footer()

    def on_mount(self) -> None:
        """Called when app is mounted."""
        self.push_screen("dashboard")

    def action_quit(self) -> None:
        """Quit the application."""
        self.exit()

    def action_help(self) -> None:
        """Show help overlay."""
        self.push_screen(HelpScreen())

    def action_search(self) -> None:
        """Show search overlay."""
        self.push_screen(SearchScreen())

    def _switch_main_screen(self, screen_name: str) -> None:
        """Switch to a main screen, closing any overlays first."""
        # Close any modal overlays first
        while len(self.screen_stack) > 1:
            self.pop_screen()
        # Replace the current main screen with the new one
        if self._current_main_screen != screen_name:
            self.pop_screen()
            self.push_screen(screen_name)
            self._current_main_screen = screen_name

    def action_dashboard(self) -> None:
        """Go to dashboard."""
        self._switch_main_screen("dashboard")

    def action_assets(self) -> None:
        """Go to assets screen."""
        self._switch_main_screen("assets")

    def action_plugins(self) -> None:
        """Go to plugins screen."""
        self._switch_main_screen("plugins")

    def action_validate(self) -> None:
        """Run validation and show results."""
        is_valid, issues = self.builder.validate()
        if is_valid and not issues:
            self.notify("All plugins validated successfully!", severity="information")
        elif is_valid:
            self.notify(
                f"Validation passed with {len(issues)} warning(s)", severity="warning"
            )
        else:
            broken = sum(1 for i in issues if i.issue_type == "broken")
            self.notify(f"Validation failed: {broken} broken symlink(s)", severity="error")

    def action_back(self) -> None:
        """Go back or close overlay."""
        if len(self.screen_stack) > 1:
            self.pop_screen()


def run(marketplace_root: Optional[Path] = None) -> None:
    """Run the TUI application."""
    app = PluginBuilderApp(marketplace_root=marketplace_root)
    app.run()


if __name__ == "__main__":
    run()
