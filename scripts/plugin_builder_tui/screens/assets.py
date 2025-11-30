"""Assets screen for browsing and managing registry assets."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import Screen
from textual.widgets import DataTable, Input, Label, TabbedContent, TabPane

from plugin_builder_tui.builder import AssetType, PluginBuilder


class AssetsScreen(Screen):
    """Screen for browsing assets in the registry."""

    BINDINGS = [
        ("f", "filter", "Filter"),
        ("enter", "select", "Select"),
        ("delete", "delete_asset", "Delete"),
    ]

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.filter_text = ""

    def compose(self) -> ComposeResult:
        builder: PluginBuilder = self.app.builder  # type: ignore

        with Container(id="content"):
            yield Label("[bold]Registry Assets[/]", id="screen-title")
            yield Input(placeholder="Type to filter...", id="asset-filter")

            with TabbedContent():
                with TabPane("Commands", id="tab-commands"):
                    yield self._create_asset_table(builder, AssetType.COMMAND)

                with TabPane("Agents", id="tab-agents"):
                    yield self._create_asset_table(builder, AssetType.AGENT)

                with TabPane("Skills", id="tab-skills"):
                    yield self._create_asset_table(builder, AssetType.SKILL)

    def _create_asset_table(
        self, builder: PluginBuilder, asset_type: AssetType
    ) -> DataTable:
        """Create a data table for an asset type."""
        table = DataTable(id=f"table-{asset_type.value}")
        table.add_columns("Name", "Description", "Used By")
        table.cursor_type = "row"

        assets = builder.get_registry_assets(asset_type)
        usage = builder.get_usage_info()

        for asset in assets:
            key = f"{asset.asset_type.value}:{asset.name}"
            used_by = usage.get(key)
            plugins_str = ", ".join(used_by.plugins) if used_by and used_by.plugins else "-"

            table.add_row(
                asset.name,
                asset.description[:50] + "..." if len(asset.description) > 50 else asset.description or "-",
                plugins_str,
                key=asset.name,
            )

        return table

    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle filter input changes."""
        if event.input.id == "asset-filter":
            self.filter_text = event.value.lower()
            self._apply_filter()

    def _apply_filter(self) -> None:
        """Apply filter to all tables."""
        builder: PluginBuilder = self.app.builder  # type: ignore
        usage = builder.get_usage_info()

        for asset_type in AssetType:
            table = self.query_one(f"#table-{asset_type.value}", DataTable)
            table.clear()

            assets = builder.get_registry_assets(asset_type)

            for asset in assets:
                # Apply filter
                if self.filter_text:
                    if (
                        self.filter_text not in asset.name.lower()
                        and self.filter_text not in asset.description.lower()
                    ):
                        continue

                key = f"{asset.asset_type.value}:{asset.name}"
                used_by = usage.get(key)
                plugins_str = ", ".join(used_by.plugins) if used_by and used_by.plugins else "-"

                table.add_row(
                    asset.name,
                    asset.description[:50] + "..." if len(asset.description) > 50 else asset.description or "-",
                    plugins_str,
                    key=asset.name,
                )

    def action_filter(self) -> None:
        """Focus the filter input."""
        self.query_one("#asset-filter", Input).focus()

    def action_delete_asset(self) -> None:
        """Delete selected asset."""
        # Find the active tab's table
        tabbed = self.query_one(TabbedContent)
        active_tab = tabbed.active
        if not active_tab:
            return

        # Map tab id to asset type
        type_map = {
            "tab-commands": AssetType.COMMAND,
            "tab-agents": AssetType.AGENT,
            "tab-skills": AssetType.SKILL,
        }
        asset_type = type_map.get(active_tab)
        if not asset_type:
            return

        table = self.query_one(f"#table-{asset_type.value}", DataTable)
        if table.cursor_row is None:
            return

        row_key = table.get_row_at(table.cursor_row)
        if not row_key:
            return

        asset_name = str(row_key[0])  # First column is name

        # Show confirmation
        self.app.notify(
            f"Delete '{asset_name}'? Press Delete again to confirm.",
            severity="warning",
        )
