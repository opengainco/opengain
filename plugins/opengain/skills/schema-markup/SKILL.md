---
name: schema-markup
description: Inspect, validate, generate, and implement Schema.org JSON-LD without inventing entities, ratings, prices, availability, or other unsupported facts.
---

# Schema Markup

Structured data must describe visible, truthful page content. It is not a place to add claims the page does not support.

## Process

1. Identify the page type, primary entity, publisher, and any existing JSON-LD, microdata, or RDFa.
2. Parse every existing block and report syntax errors, duplicate entities, conflicting identifiers, and references that do not resolve.
3. Choose only types relevant to the page. Prefer a small connected graph with stable `@id` values over unrelated blocks.
4. Preserve existing valid identifiers and connect entities through properties such as `mainEntity`, `about`, `author`, `publisher`, `isPartOf`, or `breadcrumb` when supported.
5. Never fabricate reviews, aggregate ratings, offers, prices, inventory, dates, credentials, locations, or organization relationships.
6. Explain which properties are required by the chosen search feature versus recommended by Schema.org or the site's own data model.
7. Validate syntax locally when possible and provide the exact external validator the user should use for eligibility checks. Do not claim external validation unless it ran.

## Implementation

When the user asks for code changes, follow `implement-seo-fixes`. Generate JSON-LD from server-controlled data, escape serialized content safely, avoid duplicate injection across layouts, and keep page-visible content consistent with the graph.

## Output

Return current-state findings, the proposed entity graph, a complete JSON-LD example or patch, factual inputs still required, and verification steps. State clearly that valid markup does not guarantee a rich result.
