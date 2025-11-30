"""Dashboard screen showing stats and health overview."""

from __future__ import annotations

from typing import Union

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Label, Static

from plugin_builder_tui.builder import PluginBuilder


class StatCard(Static):
    """A card displaying a single statistic."""

    def __init__(self, label: str, value: Union[str, int], **kwargs) -> None:
        super().__init__(**kwargs)
        self.stat_label = label
        self.stat_value = str(value)

    def compose(self) -> ComposeResult:
        yield Label(self.stat_value, classes="stat-value")
        yield Label(self.stat_label, classes="stat-label")


class HealthPanel(Static):
    """Panel showing health status."""

    def __init__(self, builder: PluginBuilder, **kwargs) -> None:
        super().__init__(**kwargs)
        self.builder = builder

    def compose(self) -> ComposeResult:
        is_valid, issues = self.builder.validate()
        orphans = self.builder.get_orphans()
        shared = self.builder.get_shared_assets()

        # Set panel class based on health
        if not is_valid:
            self.add_class("unhealthy")
        elif orphans:
            pass  # Default styling
        else:
            self.add_class("healthy")

        yield Label("Health Status", classes="help-title")

        if is_valid and not orphans and not issues:
            yield Label("[green]All systems healthy[/]")
        else:
            if not is_valid:
                broken = sum(1 for i in issues if i.issue_type == "broken")
                yield Label(f"[red]Broken symlinks: {broken}[/]")

            if orphans:
                yield Label(f"[yellow]Orphaned assets: {len(orphans)}[/]")
                for orphan in orphans[:3]:
                    yield Label(
                        f"  [dim]{orphan.asset_type.value}/{orphan.name}[/]",
                    )
                if len(orphans) > 3:
                    yield Label(f"  [dim]... and {len(orphans) - 3} more[/]")

            warnings = [i for i in issues if i.issue_type == "warning"]
            if warnings:
                yield Label(f"[yellow]Warnings: {len(warnings)}[/]")

        if shared:
            yield Label(f"[blue]Shared assets: {len(shared)}[/]")


class DashboardScreen(Screen):
    """Main dashboard screen with stats and health."""

    BINDINGS = []

    def compose(self) -> ComposeResult:
        # Get builder from app
        builder: PluginBuilder = self.app.builder  # type: ignore
        stats = builder.get_stats()

        with Container(id="content"):
            yield Label("[bold]Dashboard[/]", id="screen-title")

            # Stats grid
            with Horizontal(id="stats-row"):
                yield StatCard(
                    "Commands",
                    stats["commands"],
                    classes="stat-card",
                )
                yield StatCard(
                    "Agents",
                    stats["agents"],
                    classes="stat-card",
                )
                yield StatCard(
                    "Skills",
                    stats["skills"],
                    classes="stat-card",
                )
                yield StatCard(
                    "Plugins",
                    stats["plugins"],
                    classes="stat-card",
                )

            with Horizontal(id="stats-row-2"):
                yield StatCard(
                    "Total Assets",
                    stats["total_assets"],
                    classes="stat-card",
                )
                yield StatCard(
                    "Total Size",
                    f"{stats['total_size_kb']} KB",
                    classes="stat-card",
                )
                yield StatCard(
                    "Avg per Plugin",
                    f"{stats['avg_assets_per_plugin']:.1f}",
                    classes="stat-card",
                )

            # Health panel
            yield HealthPanel(builder, id="health-panel")

            # Quick actions hint
            yield Label(
                "\n[dim]Press [bold]a[/] for Assets, [bold]p[/] for Plugins, "
                "[bold]/[/] to Search, [bold]?[/] for Help[/]",
                id="quick-hint",
            )
