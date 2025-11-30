"""
Plugin Builder TUI - Modern terminal interface for Claude Code marketplace management.
"""

from plugin_builder_tui.builder import (
    Asset,
    AssetType,
    Plugin,
    PluginBuilder,
    UsageInfo,
)

__all__ = [
    "PluginBuilder",
    "Asset",
    "AssetType",
    "Plugin",
    "UsageInfo",
]


def get_app():
    """Lazy import of PluginBuilderApp to avoid requiring textual for CLI."""
    from plugin_builder_tui.app import PluginBuilderApp

    return PluginBuilderApp
