# ADR 0001 — Repository Bootstrap

## Status
Accepted

## Context
NetCoreX ModelSwitch starts as a Telegram-first pilot for multi-bot orchestration and hybrid model routing.

## Decision
Adopt a Python-first monorepo-style scaffold with clear domain modules under `src/`.

## Consequences
- Fast iteration for orchestration and policy engine design
- Easy path to service/CLI evolution
- Future adapters can be added incrementally
