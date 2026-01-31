# Implementation Plan - Clawdbot Beads & Memory V2 Skill

This plan outlines the creation of a reusable "Skill" for Clawdbot that implements the "Beads" Task Management system and "Memory V2" Knowledge Distillation protocol.

## Goal Description
Create a standardized "Skill" package that can be "installed" or "loaded" into a Clawdbot agent. This skill will enable the agent to:
1.  Manage tasks using the **Beads Protocol** (`#plan`, `#do`, `#status`, `#add`).
2.  Manage knowledge using the **Memory V2 Protocol** (`#memory` with `[W]`, `[B]`, `[O]` tags).
3.  Perform self-maintenance via `#backup` and `#fix`.

## User Review Required
> [!IMPORTANT]
> This skill relies on the user configuring their Clawdbot setup to recognize the `SKILL.md` instructions. The plan assumes a standard "Skills" folder structure `i:/Skills/<skill-name>`.

## Proposed Changes

### New Skill Directory: `i:/Skills/clawdbot-beads-memory`

#### [NEW] [SKILL.md](file:///i:/Skills/clawdbot-beads-memory/SKILL.md)
The core instruction file containing the "Commander Protocol". This file will be read by the Agent to understand how to behave.
- Defines **Persona**: Chopper (Doctor/Assistant).
- Defines **Beads Protocol**: `#plan`, `#do`, `#status`.
- Defines **Memory V2 Protocol**: `#memory` (Retain/Recall/Reflect).
- Defines **System Commands**: `#switch`, `#fix`, `#backup`.

#### [NEW] [README.md](file:///i:/Skills/clawdbot-beads-memory/README.md)
Documentation on how to "install" and use this skill.
- Instructions to copy `systemPrompt` into `clawdbot.json`.
- Instructions to setup `.gitignore` and `~/clawd/bank`.

#### [NEW] [templates/.gitignore](file:///i:/Skills/clawdbot-beads-memory/templates/.gitignore)
A template `.gitignore` file optimized for this protocol.
- Ignores `sessions/`, `node_modules`.
- Whitelists `BEADS.md`, `bank/`, `SOUL.md`.

#### [NEW] [templates/SOUL.md](file:///i:/Skills/clawdbot-beads-memory/templates/SOUL.md)
A structured `SOUL.md` file that can be placed in the agent's workspace to reinforce the protocols.

## Verification Plan

### Manual Verification
1.  **Install Check**: User reviews the generated `SKILL.md` and `README.md`.
2.  **Protocol Simulation**: (Optional) We can simulate a chat session where I act as the "Clawdbot" with this skill loaded to demonstrate `#plan` and `#memory` working as intended.
