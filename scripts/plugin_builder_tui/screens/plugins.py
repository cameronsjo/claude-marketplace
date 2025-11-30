"""Plugins screen for browsing and editing plugins."""

from __future__ import annotations

from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.screen import ModalScreen, Screen
from textual.widgets import (
    Button,
    Label,
    ListItem,
    ListView,
    OptionList,
    Static,
    Tree,
)
from textual.widgets.option_list import Option

from ..builder import AssetType, Plugin, PluginBuilder

if TYPE_CHECKING:
    pass


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


class AddAssetModal(ModalScreen[tuple[str, AssetType] | None]):
    """Modal for adding an asset to a plugin."""

    BINDINGS = [
        ("escape", "cancel", "Cancel"),
    ]

    CSS = """
    AddAssetModal {
        align: center middle;
    }

    AddAssetModal > #add-asset-dialog {
        width: 60;
        height: auto;
        max-height: 80%;
        border: round #5fafff;
        background: $background;
        padding: 1 2;
    }

    AddAssetModal #asset-type-tabs {
        height: 3;
        margin-bottom: 1;
    }

    AddAssetModal #available-assets {
        height: 20;
        border: round #808080 30%;
        margin-bottom: 1;
    }

    AddAssetModal .modal-title {
        text-style: bold;
        color: $text;
        margin-bottom: 1;
    }

    AddAssetModal .modal-buttons {
        height: 3;
        align: right middle;
    }

    AddAssetModal Button {
        margin: 0 1;
    }
    """

    def __init__(
        self,
        plugin: Plugin,
        builder: PluginBuilder,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.plugin = plugin
        self.builder = builder
        self.current_type = AssetType.COMMAND
        self.selected_asset: str | None = None

    def compose(self) -> ComposeResult:
        with Container(id="add-asset-dialog"):
            yield Label(f"Add Asset to [bold]{self.plugin.name}[/]", classes="modal-title")

            # Type selector buttons
            with Horizontal(id="asset-type-tabs"):
                yield Button("Commands", id="btn-commands", variant="primary")
                yield Button("Agents", id="btn-agents")
                yield Button("Skills", id="btn-skills")

            # Available assets list
            yield OptionList(id="available-assets")

            # Action buttons
            with Horizontal(classes="modal-buttons"):
                yield Button("Cancel", id="btn-cancel")
                yield Button("Add", id="btn-add", variant="success", disabled=True)

    def on_mount(self) -> None:
        """Load initial assets."""
        self._load_assets(AssetType.COMMAND)
        # Set initial focus to the option list
        self.set_timer(0.1, lambda: self.query_one("#available-assets", OptionList).focus())

    def _load_assets(self, asset_type: AssetType) -> None:
        """Load available assets for the given type."""
        self.current_type = asset_type

        # Update button styles
        for btn_id, btn_type in [
            ("btn-commands", AssetType.COMMAND),
            ("btn-agents", AssetType.AGENT),
            ("btn-skills", AssetType.SKILL),
        ]:
            btn = self.query_one(f"#{btn_id}", Button)
            btn.variant = "primary" if btn_type == asset_type else "default"

        # Get assets not already in the plugin
        all_assets = self.builder.get_registry_assets(asset_type)
        existing = set(getattr(self.plugin, asset_type.value, []))
        available = [a for a in all_assets if a.name not in existing]

        # Update modal title with count
        title = self.query_one(".modal-title", Label)
        title.update(
            f"Add {asset_type.value[:-1].title()} to [bold]{self.plugin.name}[/] "
            f"[dim]({len(available)} available)[/]"
        )

        # Update option list
        option_list = self.query_one("#available-assets", OptionList)
        option_list.clear_options()

        if not available:
            msg = f"All {asset_type.value} are already in this plugin"
            option_list.add_option(Option(f"[dim]{msg}[/]", disabled=True))
        else:
            for asset in available:
                desc = f" - {asset.description[:40]}..." if asset.description else ""
                option_list.add_option(Option(f"{asset.name}{desc}", id=asset.name))

        self.selected_asset = None
        self.query_one("#btn-add", Button).disabled = True

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "btn-commands":
            self._load_assets(AssetType.COMMAND)
        elif event.button.id == "btn-agents":
            self._load_assets(AssetType.AGENT)
        elif event.button.id == "btn-skills":
            self._load_assets(AssetType.SKILL)
        elif event.button.id == "btn-cancel":
            self.dismiss(None)
        elif event.button.id == "btn-add":
            if self.selected_asset:
                self.dismiss((self.selected_asset, self.current_type))

    def on_option_list_option_highlighted(
        self, event: OptionList.OptionHighlighted
    ) -> None:
        """Handle asset selection."""
        if event.option and event.option.id and not event.option.disabled:
            self.selected_asset = str(event.option.id)
            self.query_one("#btn-add", Button).disabled = False
        else:
            self.selected_asset = None
            self.query_one("#btn-add", Button).disabled = True

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        """Handle double-click/enter on asset."""
        if event.option and event.option.id and not event.option.disabled:
            self.dismiss((str(event.option.id), self.current_type))

    def action_cancel(self) -> None:
        """Cancel the modal."""
        self.dismiss(None)


class RemoveAssetModal(ModalScreen[tuple[str, AssetType] | None]):
    """Modal for removing an asset from a plugin."""

    BINDINGS = [
        ("escape", "cancel", "Cancel"),
    ]

    CSS = """
    RemoveAssetModal {
        align: center middle;
    }

    RemoveAssetModal > #remove-asset-dialog {
        width: 60;
        height: auto;
        max-height: 80%;
        border: round #ff5f5f;
        background: $background;
        padding: 1 2;
    }

    RemoveAssetModal #plugin-assets {
        height: 20;
        border: round #808080 30%;
        margin-bottom: 1;
    }

    RemoveAssetModal .modal-title {
        text-style: bold;
        color: $text;
        margin-bottom: 1;
    }

    RemoveAssetModal .modal-buttons {
        height: 3;
        align: right middle;
    }

    RemoveAssetModal Button {
        margin: 0 1;
    }
    """

    def __init__(self, plugin: Plugin, **kwargs) -> None:
        super().__init__(**kwargs)
        self.plugin = plugin
        self.selected_asset: str | None = None
        self.selected_type: AssetType | None = None

    def compose(self) -> ComposeResult:
        with Container(id="remove-asset-dialog"):
            yield Label(
                f"Remove Asset from [bold]{self.plugin.name}[/]", classes="modal-title"
            )

            # Plugin's current assets
            yield OptionList(id="plugin-assets")

            # Action buttons
            with Horizontal(classes="modal-buttons"):
                yield Button("Cancel", id="btn-cancel")
                yield Button("Remove", id="btn-remove", variant="error", disabled=True)

    def on_mount(self) -> None:
        """Load plugin's assets."""
        option_list = self.query_one("#plugin-assets", OptionList)

        has_assets = False

        # Add commands
        if self.plugin.commands:
            option_list.add_option(Option("[bold]Commands[/]", disabled=True))
            for cmd in self.plugin.commands:
                option_list.add_option(Option(f"  /{cmd}", id=f"commands:{cmd}"))
            has_assets = True

        # Add agents
        if self.plugin.agents:
            option_list.add_option(Option("[bold]Agents[/]", disabled=True))
            for agent in self.plugin.agents:
                option_list.add_option(Option(f"  {agent}", id=f"agents:{agent}"))
            has_assets = True

        # Add skills
        if self.plugin.skills:
            option_list.add_option(Option("[bold]Skills[/]", disabled=True))
            for skill in self.plugin.skills:
                option_list.add_option(Option(f"  {skill}", id=f"skills:{skill}"))
            has_assets = True

        if not has_assets:
            option_list.add_option(Option("[dim]No assets in plugin[/]", disabled=True))

        # Set initial focus to the option list
        self.set_timer(0.1, lambda: option_list.focus())

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "btn-cancel":
            self.dismiss(None)
        elif event.button.id == "btn-remove":
            if self.selected_asset and self.selected_type:
                self.dismiss((self.selected_asset, self.selected_type))

    def on_option_list_option_highlighted(
        self, event: OptionList.OptionHighlighted
    ) -> None:
        """Handle asset selection."""
        if event.option and event.option.id and not event.option.disabled:
            option_id = str(event.option.id)
            type_str, asset_name = option_id.split(":", 1)
            self.selected_type = AssetType(type_str)
            self.selected_asset = asset_name
            self.query_one("#btn-remove", Button).disabled = False
        else:
            self.selected_asset = None
            self.selected_type = None
            self.query_one("#btn-remove", Button).disabled = True

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        """Handle double-click/enter on asset."""
        if event.option and event.option.id and not event.option.disabled:
            option_id = str(event.option.id)
            type_str, asset_name = option_id.split(":", 1)
            self.dismiss((asset_name, AssetType(type_str)))

    def action_cancel(self) -> None:
        """Cancel the modal."""
        self.dismiss(None)


class PluginsScreen(Screen):
    """Screen for browsing and editing plugins."""

    BINDINGS = [
        ("n", "new_plugin", "New Plugin"),
        ("a", "add_asset", "Add Asset", True),
        ("r", "remove_asset", "Remove Asset", True),
        ("enter", "select", "Select"),
    ]

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.selected_plugin: Plugin | None = None

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
                        *[PluginListItem(p, id=f"plugin-{i}-init") for i, p in enumerate(plugins)],
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

    def _refresh_plugin_list(self) -> None:
        """Refresh the plugin list after changes."""
        builder: PluginBuilder = self.app.builder  # type: ignore
        plugins = builder.get_plugins()

        plugin_list = self.query_one("#plugin-list", ListView)
        current_plugin_name = self.selected_plugin.name if self.selected_plugin else None

        # Remove all existing items properly
        plugin_list.clear()

        # Use unique IDs with timestamp to avoid conflicts during refresh
        import time
        ts = int(time.time() * 1000) % 100000

        for i, p in enumerate(plugins):
            plugin_list.append(PluginListItem(p, id=f"plugin-{i}-{ts}"))

        # Re-select the current plugin if it still exists
        if current_plugin_name:
            for idx, p in enumerate(plugins):
                if p.name == current_plugin_name:
                    self.selected_plugin = p
                    self._update_plugin_details()
                    # Set the index to highlight the plugin
                    plugin_list.index = idx
                    break
            else:
                # Plugin was deleted, clear selection
                self.selected_plugin = None

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
        self.app.notify(
            "Use CLI: python plugin-builder.py create <name>",
            severity="information",
        )

    def action_add_asset(self) -> None:
        """Add an asset to the selected plugin."""
        if not self.selected_plugin:
            self.app.notify("Select a plugin first", severity="warning")
            return

        builder: PluginBuilder = self.app.builder  # type: ignore

        def handle_add(result: tuple[str, AssetType] | None) -> None:
            if result is None:
                return

            asset_name, asset_type = result
            try:
                success = builder.add_asset_to_plugin(
                    self.selected_plugin.name,  # type: ignore
                    asset_name,
                    asset_type,
                )

                if success:
                    self.app.notify(
                        f"Added {asset_type.value[:-1]} '{asset_name}' to {self.selected_plugin.name}",  # type: ignore
                        severity="information",
                    )
                    self._refresh_plugin_list()
                else:
                    self.app.notify(
                        f"Asset '{asset_name}' already exists in {self.selected_plugin.name}",  # type: ignore
                        severity="warning",
                    )
            except ValueError as e:
                self.app.notify(
                    f"Error: {str(e)}",
                    severity="error",
                )
            except Exception as e:
                self.app.notify(
                    f"Unexpected error: {str(e)}",
                    severity="error",
                )

        self.app.push_screen(
            AddAssetModal(self.selected_plugin, builder),
            handle_add,
        )

    def action_remove_asset(self) -> None:
        """Remove an asset from the selected plugin."""
        if not self.selected_plugin:
            self.app.notify("Select a plugin first", severity="warning")
            return

        # Check if plugin has any assets
        if not (self.selected_plugin.commands or self.selected_plugin.agents or self.selected_plugin.skills):
            self.app.notify(
                f"{self.selected_plugin.name} has no assets to remove",
                severity="information",
            )
            return

        builder: PluginBuilder = self.app.builder  # type: ignore

        def handle_remove(result: tuple[str, AssetType] | None) -> None:
            if result is None:
                return

            asset_name, asset_type = result
            try:
                success = builder.remove_asset_from_plugin(
                    self.selected_plugin.name,  # type: ignore
                    asset_name,
                    asset_type,
                )

                if success:
                    self.app.notify(
                        f"Removed {asset_type.value[:-1]} '{asset_name}' from {self.selected_plugin.name}",  # type: ignore
                        severity="information",
                    )
                    self._refresh_plugin_list()
                else:
                    self.app.notify(
                        f"Asset '{asset_name}' not found in {self.selected_plugin.name}",  # type: ignore
                        severity="warning",
                    )
            except ValueError as e:
                self.app.notify(
                    f"Error: {str(e)}",
                    severity="error",
                )
            except Exception as e:
                self.app.notify(
                    f"Unexpected error: {str(e)}",
                    severity="error",
                )

        self.app.push_screen(
            RemoveAssetModal(self.selected_plugin),
            handle_remove,
        )
