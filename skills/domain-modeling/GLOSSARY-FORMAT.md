# glossary.md Format

## Structure

```md
# Ubiquitous Glossary

{One or two sentence description of what this context is and why it exists.}

## Core Domain Terms

**Brew**:
A discrete software feature, refactoring unit, or bug fix being actively developed under the Stage 0-9 protocol.
_Avoid_: Task, issue, ticket, feature branch

**Autonomous Brewing Swarm**:
The collection of specialized, role-focused agentic engines working collaboratively to deliver a Brew.
_Avoid_: Agent pool, script set, AI assistants
```

## Rules

- **Be opinionated.** When multiple words exist for the same concept, pick the best one and list the others under `_Avoid_`.
- **Keep definitions tight.** One or two sentences max. Define what it IS, not what it does.
- **Only include terms specific to this project's context.** General programming concepts (timeouts, error types, utility patterns) don't belong even if the project uses them extensively. Before adding a term, ask: is this a concept unique to this context, or a general programming concept? Only the former belongs.
- **Group terms under subheadings** when natural clusters emerge. If all terms belong to a single cohesive area, a flat list is fine.

## Single vs multi-context repos

**Single context (most repos):** One `docs/glossary.md` in the project `docs/` folder.

**Multiple contexts:** A `docs/glossary-map.md` lists the contexts, where they live, and how they relate to each other:

```md
# Glossary Map

## Contexts

- [Ordering](./src/ordering/glossary.md) — receives and tracks customer orders
- [Billing](./src/billing/glossary.md) — generates invoices and processes payments
- [Fulfillment](./src/fulfillment/glossary.md) — manages warehouse picking and shipping

## Relationships

- **Ordering → Fulfillment**: Ordering emits `OrderPlaced` events; Fulfillment consumes them to start picking
- **Fulfillment → Billing**: Fulfillment emits `ShipmentDispatched` events; Billing consumes them to generate invoices
- **Ordering ↔ Billing**: Shared types for `CustomerId` and `Money`
```

The skill infers which structure applies:

- If `docs/glossary-map.md` exists, read it to find contexts
- If only `docs/glossary.md` exists, single context
- If neither exists, create `docs/glossary.md` lazily when the first term is resolved

When multiple contexts exist, infer which one the current topic relates to. If unclear, ask.