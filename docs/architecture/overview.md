# Architecture Overview

## Telegram-first pilot architecture

### Layers
1. Channel Layer (Telegram-first)
2. Intake Layer
3. Intent & Complexity Analysis
4. Specialist Bot Orchestrator
5. Model Routing Engine
6. Execution Layer
7. Telemetry, Ledger & Governance

## High-level request flow
1. A Telegram message enters the system through the channel adapter.
2. The intake layer normalizes the inbound request into internal contracts.
3. The intent layer classifies task type, complexity, and potential risk.
4. The orchestrator decides whether the coordinator bot can answer directly or whether specialist bots should be engaged.
5. The routing engine chooses the execution path:
   - local model
   - premium cloud model
   - multimodal path
   - fallback chain
6. The execution layer runs the chosen bot/model path.
7. The synthesizer consolidates specialist outputs when needed.
8. The telemetry and governance layer records cost, tokens, latency, fallback decisions, and route reasons.
9. A final response is delivered back through Telegram.

## Design goals
- minimize paid-token spend
- preserve precision for important work
- support specialist bot delegation
- keep every routing decision explainable
- keep Telegram as the initial operational surface
- make token-cost reporting a native feature, not an afterthought

## Key responsibilities
### Coordinator Bot
- receives the normalized request
- creates an execution plan
- decides when specialist bots are needed
- consolidates final response output

### Specialist Bot Orchestrator
- selects one or more specialists
- manages delegated subtasks
- tracks subtask outcomes and synthesis order

### Model Routing Engine
- chooses local vs premium execution
- enforces route policies
- applies fallback chains when necessary
- balances cost, latency, and quality targets

### Telemetry & Governance Layer
- records request-level token/cost data
- tracks provider/model usage
- supports budget-aware operations
- enables operator reporting in Telegram and future dashboards
