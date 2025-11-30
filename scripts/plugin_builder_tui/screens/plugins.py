"""Plugins screen for browsing and editing plugins."""

from __future__ import annotations

from typing import Optional

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Input, Label, ListItem, ListView, Static, Tree
from textual.widgets.tree import TreeNode

from plugin_builder_tui.builder import AssetType, Plugin, PluginBuilder


class PluginListItem(ListItem):
    """A list item representing a plugin."""

    def __init__(self, plugin: Plugin, **kwargs) -> None:
        super().__init__(**kwargs)
        self.plugin = plugin

    def compose(self) -> ComposeResult:
        with Horizontal(classes="plugin-item"):
            yield Label(self.plugin.name, classes="plugin-name")
            yield Label(
                f"({self.plugin.total_assets})",
                classes="plugin-count",
            )


class PluginsScreen(Screen):
    """Screen for browsing and editing plugins."""

    BINDINGS = [
        ("n", "new_plugin", "New Plugin"),
        ("a", "add_asset", "Add Asset"),
        ("r", "remove_asset", "Remove Asset"),
        ("enter", "select", "Select"),
    ]

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.selected_plugin: Optional[Plugin] = None

    def compose(self) -> ComposeResult:
        builder: PluginBuilder = self.app.builder  # type: ignore
        plugins = builder.get_plugins()

        with Container(id="content"):
            yield Label("[bold]Plugins[/]", id="screen-title")

            with Horizontal():
                # Left pane: plugin list
                with Vertical(id="left-pane"):
                    yield Label("[bold]Select Plugin[/]")
                    yield ListView(
                        *[PluginListItem(p, id=f"plugin-{p.name}") for p in plugins],
                        id="plugin-list",
                    )
                    yield Button("New Plugin", id="btn-new", variant="primary")

                # Right pane: plugin details
                with Vertical(id="right-pane"):
                    yield Label("[bold]Plugin Contents[/]", id="plugin-title")
                    yield Static(
                        "[dim]Select a plugin to view its contents[/]",
                        id="plugin-details",
                    )
                    tree: Tree[str] = Tree("Assets", id="asset-tree")
                    tree.show_root = False
                    yield tree
                    with Horizontal(id="plugin-actions"):
                        yield Button(
                            "Add Asset", id="btn-add", variant="success", disabled=True
                        )
                        yield Button(
                            "Remove Asset", id="btn-remove", variant="error", disabled=True
                        )

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle plugin selection."""
        if not isinstance(event.item, PluginListItem):
            return

        self.selected_plugin = event.item.plugin
        self._update_plugin_details()

    def _update_plugin_details(self) -> None:
        """Update the right pane with selected plugin details."""
        if not self.selected_plugin:
            return

        plugin = self.selected_plugin

        # Update title
        title = self.query_one("#plugin-title", Label)
        title.update(f"[bold]{plugin.name}[/]")

        # Update details
        details = self.query_one("#plugin-details", Static)
        details.update(
            f"{plugin.description}\n"
            f"[dim]Version: {plugin.version} | Category: {plugin.category}[/]"
        )

        # Update tree
        tree = self.query_one("#asset-tree", Tree)
        tree.clear()

        # Add commands
        if plugin.commands:
            commands_node = tree.root.add("Commands", expand=True)
            for cmd in plugin.commands:
                commands_node.add_leaf(f"/{cmd}")

        # Add agents
        if plugin.agents:
            agents_node = tree.root.add("Agents", expand=True)
            for agent in plugin.agents:
                agents_node.add_leaf(agent)

        # Add skills
        if plugin.skills:
            skills_node = tree.root.add("Skills", expand=True)
            for skill in plugin.skills:
                skills_node.add_leaf(skill)

        if not (plugin.commands or plugin.agents or plugin.skills):
            tree.root.add_leaf("[dim]No assets[/]")

        # Enable action buttons
        self.query_one("#btn-add", Button).disabled = False
        self.query_one("#btn-remove", Button).disabled = False

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "btn-new":
            self.action_new_plugin()
        elif event.button.id == "btn-add":
            self.action_add_asset()
        elif event.button.id == "btn-remove":
            self.action_remove_asset()

    def action_new_plugin(self) -> None:
        """Create a new plugin."""
        # For now, just show a notification
        # In a full implementation, this would open a dialog
        self.app.notify(
            "Use CLI: python plugin-builder.py create <name>",
            severity="information",
        )

    def action_add_asset(self) -> None:
        """Add an asset to the selected plugin."""
        if not self.selected_plugin:
            self.app.notify("Select a plugin first", severity="warning")
            return

        self.app.notify(
            f"Use CLI: python plugin-builder.py edit add {self.selected_plugin.name} <asset> -t <type>",
            severity="information",
        )

    def action_remove_asset(self) -> None:
        """Remove an asset from the selected plugin."""
        if not self.selected_plugin:
            self.app.notify("Select a plugin first", severity="warning")
            return

        tree = self.query_one("#asset-tree", Tree)
        cursor_node = tree.cursor_node
        if not cursor_node or cursor_node.is_root:
            self.app.notify("Select an asset to remove", severity="warning")
            return

        # Get asset info from tree
        asset_label = str(cursor_node.label)
        if asset_label.startswith("/"):
            asset_label = asset_label[1:]  # Remove leading slash for commands

        self.app.notify(
            f"Use CLI: python plugin-builder.py edit remove {self.selected_plugin.name} {asset_label} -t <type>",
            severity="information",
        )
