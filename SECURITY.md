# Security Policy

## Reporting a vulnerability

Please report security issues privately through GitHub's security-advisory feature for this repository. Do not open a public issue containing credentials, OAuth artifacts, private reports, or exploit details.

Include the affected component, reproduction conditions, potential impact, and any suggested mitigation. OpenGain will acknowledge a complete report and coordinate disclosure after a fix is available.

## Repository boundary

This repository contains declarative plugin manifests and Markdown workflow instructions. It must not contain API keys, OAuth tokens, cookies, private customer data, cloud environment files, or source copied from the private OpenGain service.

The hosted MCP server enforces authentication, workspace isolation, scopes, rate limits, and credit caps. Plugin instructions are not a substitute for those server-side controls.
