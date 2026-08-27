---
name: technical-seo
description: Diagnose technical SEO across crawlability, indexability, canonicalization, redirects, sitemaps, performance, mobile rendering, and security-adjacent search signals.
---

# Technical SEO

Inspect the smallest representative set of pages and code needed to support each conclusion.

## Checks

1. Crawl access: status codes, redirect chains, robots directives, robots.txt, authentication walls, and accidental staging restrictions.
2. Indexability: meta robots, `X-Robots-Tag`, canonical targets, duplicate variants, pagination, soft 404s, and conflicting signals.
3. Discovery: XML sitemap validity, index files, URL consistency, orphan risk, navigation depth, and internal-link reachability.
4. Rendering: server-rendered content, hydration failures, JavaScript-only critical content, mobile parity, and bot-visible navigation.
5. URL behavior: normalized schemes/hosts, trailing-slash rules, parameters, casing, international variants, and redirect loops.
6. Performance: available Core Web Vitals evidence, response latency, render-blocking work, oversized media, caching, and third-party impact.
7. Protocol and security-adjacent signals: HTTPS consistency, mixed content, broken resources, and headers that prevent legitimate rendering. Do not turn this into penetration testing.

Use source files and framework configuration when available to locate the root cause. For live pages, fetch only public HTTP(S) URLs authorized by the user; do not probe private networks or bypass access controls.

## Evidence rules

- Distinguish field data, lab measurements, source inspection, HTTP observations, and inference.
- Do not quote a Core Web Vitals value unless a tool actually measured or retrieved it.
- A robots.txt allowance does not prove indexation; a sitemap entry does not prove quality or indexing.
- Report conflicting signals explicitly instead of choosing one silently.

## Output

For each finding provide affected URLs or templates, observed evidence, likely impact, confidence, recommended change, and a verification method. Lead with blockers and systemic template issues. Record inaccessible areas and tools that were unavailable.
