# NetCoreX ModelSwitch

**Telegram-first hybrid multi-bot orchestration and model routing with token-cost observability.**

NetCoreX ModelSwitch is a decision and orchestration layer for AI operations. It receives conversational requests through Telegram, analyzes intent and complexity, coordinates specialist bots, routes execution across local and cloud LLMs, and records token/cost usage per request.

## Why NetCoreX ModelSwitch?
Modern AI operations break down when teams have to choose between:
- low cost and low quality
- high quality and uncontrolled spending
- one generic bot and many disconnected specialist workflows
- local privacy and cloud capability

NetCoreX ModelSwitch is designed to solve that trade-off by combining:
- **Telegram-first operation** for simple command and response flows
- **specialist bot orchestration** for domain-specific work
- **hybrid local/cloud routing** for cost-aware execution
- **fallback chains** for resilience
- **per-request telemetry** for governance and spend visibility

## Initial pilot focus
The initial pilot focuses on **Telegram** as the primary operational channel.

### Pilot goals
- Route simple tasks to low-cost local models
- Escalate high-value or risky tasks to premium cloud models
- Coordinate specialist bots for domain-specific subtasks
- Track token usage, provider choice, latency, and fallback decisions
- Deliver a unified conversational experience through Telegram

## Product thesis
NetCoreX ModelSwitch is not just a model router.
It is a **coordination layer** for:
- channel intake
- specialist bot orchestration
- local vs cloud model routing
- multimodal escalation paths
- fallback control
- token and cost observability
- governance and budget-aware execution

## Core architecture pillars
1. **Telegram-first channel layer**
2. **Intent and complexity analysis**
3. **Multi-bot specialist orchestration**
4. **Hybrid model routing**
5. **Execution and fallback chains**
6. **Telemetry and token ledger**
7. **Governance and policy enforcement**

## Telegram-first pilot scope
### In scope
- Telegram inbound/outbound message contract
- Coordinator bot flow
- Specialist bot registry
- Routing engine contracts
- Policy engine skeleton
- Telemetry event model
- Token/cost ledger design
- Basic CLI/dev bootstrap
- Local-first routing strategy with premium escalation

### Out of scope for v1 pilot
- Slack runtime integration
- WhatsApp/Discord/Web channels
- production dashboard
- enterprise tenant admin UI
- advanced tenant-level policy management

## Planned bot roles
- **Coordinator Bot** — receives Telegram requests, builds execution plan, consolidates final output
- **Routing Analyst Bot** — evaluates best execution path by cost/risk/latency
- **Solutions Architect Bot** — architecture and systems design
- **Coding Bot** — implementation and debugging
- **Research Bot** — web/document/market analysis
- **Business Strategy Bot** — positioning, pricing, and decision support
- **Content & Communication Bot** — response shaping, refinement, and formatting

## Planned routing strategy
- low-risk / simple / short tasks → local model
- complex / strategic / high-risk tasks → premium cloud model
- multimodal / long-document tasks → specialized provider path
- local failure or low confidence → fallback escalation

## Token and cost visibility
NetCoreX ModelSwitch is designed to treat token accounting as a first-class capability.

### Target telemetry by request
- provider used
- model used
- selected bot(s)
- route reason
- input tokens
- output tokens
- estimated or real cost
- latency
- fallback triggered or not
- local-vs-paid execution attribution

### Planned operator experience
- Telegram usage summaries
- daily provider reports
- per-model cost visibility
- local savings estimation
- premium escalation traceability

## MVP v0.1 target
The first meaningful pilot milestone should deliver:
- Telegram intake
- coordinator bot
- one local adapter
- one premium cloud adapter
- route policy v1
- per-request token ledger
- Telegram consumption summary command

## Slack-ready, Telegram-first
Although the pilot is Telegram-first, the architecture should remain channel-extensible.
Slack is considered a priority next-step channel after the Telegram pilot stabilizes.

## Repository structure
```text
src/netcorex_modelswitch/
  channels/
    telegram/
  intake/
  intent/
  orchestrator/
  agents/
  router/
  policies/
  providers/
  execution/
  telemetry/
  governance/
  contracts/
  cli/
```

## Development
```bash
make test
make lint
make format
```

## Roadmap
See:
- `docs/architecture/overview.md`
- `docs/roadmap/initial-roadmap.md`
- `docs/adr/0001-repository-bootstrap.md`
