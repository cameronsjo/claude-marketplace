# Homebridge Plugin Design

**Date:** 2026-02-01
**Status:** Approved

## Overview

Claude Code plugin for Homebridge plugin development - from scaffolding through debugging. Provides expert-level assistance with official Homebridge/HAP APIs, HomeKit capability mappings, and common patterns.

## Structure

```
src/homebridge/
├── .claude-plugin/
│   └── plugin.json
├── README.md
├── skills/
│   └── homebridge-dev/
│       ├── SKILL.md
│       └── resources/
│           ├── hap-services.md
│           ├── hap-characteristics.md
│           ├── config-schema.md
│           ├── accessory-patterns.md
│           ├── verified-publisher.md
│           ├── child-bridge.md
│           ├── log-patterns.md
│           └── hap-inspector.md
└── agents/
    └── homebridge-explorer.md
```

## Components

### Skill: homebridge-dev

**Invoke:** `/homebridge`

**Behavior:**
1. Reads project context (package.json, existing accessories, config.schema.json)
2. Detects JS vs TS from project configuration
3. Loads relevant resources into context
4. Provides guided assistance based on current task

**Key capabilities:**
- New plugin scaffolding (JS or TS)
- Accessory implementation with correct HAP service/characteristic mappings
- Config schema authoring with validation and UI hints
- Log analysis and debugging workflows
- Verified publisher setup guidance
- Child bridge configuration
- HAP Inspector usage

**Tone:** Direct expert. Assumes familiarity with Homebridge, provides specific guidance without over-explaining basics.

### Agent: homebridge-explorer

**Purpose:** Research agent for longer exploration tasks. The skill dispatches to it when needed.

**Use cases:**
- HAP service/characteristic lookups
- Config schema deep dives
- Log analysis and correlation
- Pattern discovery

**Configuration:**
- Model: haiku (fast, cheap for research)
- Tools: Read, Grep, Glob, WebFetch, WebSearch

### Resources

#### hap-services.md
Complete HAP service reference:
- All services (Switch, Outlet, Thermostat, SecuritySystem, CameraRTPStreamManagement, etc.)
- Required and optional characteristics per service
- Typical use cases and examples

#### hap-characteristics.md
All HAP characteristics:
- UUIDs, value formats, valid ranges, permissions
- Grouped by category (temperature, humidity, security, battery, etc.)
- Value constraints and units

#### config-schema.md
Config schema patterns:
- JSON structure and homebridge-config-ui-x hints
- Conditional fields ("show X only when Y is enabled")
- Array handling for multiple devices
- Credential and sensitive data patterns
- Common validation (IP addresses, ports, enums)

#### accessory-patterns.md
Templates for common accessory types:
- Sensors: motion, contact, temperature, humidity, leak, smoke, CO
- Switches and outlets
- Locks
- Thermostats
- Cameras (with streaming setup)
- Security systems

Both JS and TS versions. Includes:
- Service setup
- Characteristic handlers
- Event patterns
- Error handling
- Logging conventions

#### verified-publisher.md
Verified publisher workflow:
- NPM organization setup
- Plugin naming conventions (`homebridge-*` or `@org/homebridge-*`)
- Verification request process
- Badge integration
- Maintaining verified status

#### child-bridge.md
Child bridge patterns:
- When to use child bridges (isolation, crash recovery, performance)
- Configuration in config.schema.json
- Platform vs accessory isolation
- Common patterns and gotchas

#### log-patterns.md
Debugging with logs:
- Common error signatures and what they mean
- HAP event correlation
- Startup sequence issues
- Accessory registration problems
- Characteristic update failures
- Debugging flowcharts

#### hap-inspector.md
HAP Inspector integration:
- Installation and setup
- Capturing HAP traffic
- Interpreting requests/responses
- Common issues it reveals
- Correlation with plugin behavior

## Language Support

The skill detects JavaScript or TypeScript from:
- `package.json` devDependencies (typescript, ts-node)
- Presence of `tsconfig.json`
- Source file extensions in `src/`

Adapts all patterns and examples to match project language.

## Out of Scope

- MCP server / live Homebridge instance connection
- Automated test scaffolding
- Custom UI (`homebridge-ui`) development
- Vendor-specific API knowledge (SimpliSafe, Ring, etc.)
