"""Search overlay for finding assets."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import ModalScreen
from textual.widgets import Input, Label, ListItem, ListView, Static

from ..builder import Asset, PluginBuilder


class SearchResultItem(ListItem):
    """A search result item."""

    def __init__(self, asset: Asset, **kwargs) -> None:
        super().__init__(**kwargs)
        self.asset = asset

    def compose(self) -> ComposeResult:
        yield Label(
            f"[bold]{self.asset.name}[/] [dim]({self.asset.asset_type.value})[/]"
        )
        if self.asset.description:
            yield Label(f"[dim]{self.asset.description[:60]}...[/]" if len(self.asset.description) > 60 else f"[dim]{self.asset.description}[/]")


class SearchScreen(ModalScreen):
    """Modal search overlay."""

    BINDINGS = [
        ("escape", "close", "Close"),
        ("enter", "select", "Select"),
    ]

    def compose(self) -> ComposeResult:
        with Container(id="search-overlay"):
            yield Label("[bold]Search Assets[/]")
            yield Input(placeholder="Type to search...", id="search-input")
            yield ListView(id="search-results")
            yield Label("[dim]Esc to close, Enter to select[/]")

    def on_mount(self) -> None:
        """Focus the input on mount."""
        self.query_one("#search-input", Input).focus()

    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle search input changes."""
        if event.input.id != "search-input":
            return

        query = event.value.strip()
        results_view = self.query_one("#search-results", ListView)
        results_view.clear()

        if len(query) < 2:
            return

        builder: PluginBuilder = self.app.builder  # type: ignore
        results = builder.search_assets(query)

        for asset in results[:20]:  # Limit to 20 results
            results_view.append(SearchResultItem(asset))

        if not results:
            results_view.append(
                ListItem(Label("[dim]No results found[/]"))
            )

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle result selection."""
        if isinstance(event.item, SearchResultItem):
            asset = event.item.asset
            self.app.notify(
                f"Selected: {asset.name} ({asset.asset_type.value})",
                severity="information",
            )
            self.dismiss()

    def action_close(self) -> None:
        """Close the search overlay."""
        self.dismiss()

    def action_select(self) -> None:
        """Select the highlighted result."""
        results_view = self.query_one("#search-results", ListView)
        if results_view.highlighted_child:
            results_view.highlighted_child.post_message(
                ListView.Selected(results_view, results_view.highlighted_child)
            )
