---
name: implement-seo-fixes
description: Plan and apply user-requested SEO fixes in a website codebase with minimal, reviewable changes and verification. Use only when the user asks to change or implement code.
---

# Implement SEO Fixes

Analyze by default. Enter this workflow only when the user requests implementation or clearly authorizes code changes.

## Before editing

1. Read repository instructions and inspect the framework, routing, rendering model, content source, and existing tests.
2. Trace each requested fix to the shared layout, template, component, metadata API, or content record that owns the behavior.
3. Present a concise change plan covering affected behavior and verification. Preserve unrelated user changes.
4. Resolve conflicts between recommendations and product, accessibility, security, legal, or framework constraints in favor of correctness and disclose the tradeoff.

## Editing rules

- Prefer systemic template fixes over repeated page patches when blast radius is understood.
- Keep metadata unique, truthful, and derived from authoritative content.
- Keep canonical, robots, sitemap, redirect, and hreflang behavior mutually consistent.
- Generate structured data from trusted application data; never hard-code invented ratings, prices, dates, or identities.
- Preserve accessibility and human-readable content while improving search semantics.
- Do not add tracking, paid services, new dependencies, or external network calls unless the user authorizes them.
- Never put credentials in source, examples, logs, tests, or client-visible bundles.

## Verify

Run the smallest relevant existing tests, type checks, builds, or static checks. Inspect the rendered or generated output when feasible. For changes affecting several routes, test representative variants and failure states.

Summarize changed behavior, files, verification results, and anything that still requires deployment-time or external validation. Do not claim rankings, indexation, rich results, or Core Web Vitals improved before evidence exists.
