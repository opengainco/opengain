---
name: competitor-ranking
description: Use OpenGain's MCP tools to compare why one public page outranks another for a specific Google query, poll the validated report, and ask evidence-aware follow-ups.
---

# Competitor Ranking

Use the `opengain` MCP server for live ranking comparisons. Do not replace missing tool results with guesses.

## Required inputs

- Search query, 2–500 characters.
- Subject public HTTP(S) URL.
- Competitor public HTTP(S) URL, different from the subject.
- Search context when known: country, language, and desktop or mobile.

Default search context to Google, United States, English, desktop only when the user has not supplied market context and that default is reasonable. State the default in the result.

## Start the analysis

Call `start_analysis` with:

- `query`, `subject`, `competitor`, and `search_context` from the request.
- `include_gsc: true` when the subject is identified as the user's site or the user asks to use owned-site data. The service safely reports unavailable GSC as a limitation. Otherwise use `false`.
- `max_credits: 32` when `include_gsc` is true.
- `max_credits: 30` when `include_gsc` is false.
- A unique idempotency key of at least eight characters. Keep the same key when retrying the same logical request; create a new key for changed inputs.

Start immediately once required inputs are known. The credit cap is a maximum reservation, not a claim that all credits will be consumed.

## Poll

Use the returned analysis ID with `get_analysis`. Poll with bounded backoff until status is `completed`, `failed`, or `cancelled`. Avoid rapid repeated calls. Report meaningful stage/progress changes if the user is waiting.

If the run fails, report its error and retryability. Do not automatically create a different paid run unless the user's inputs changed or they request a retry.

## Interpret

For a completed report:

1. Lead with the strongest supported ranking factors.
2. Preserve impact and confidence labels.
3. Tie recommendations to evidence IDs and distinguish observations from inference.
4. Include coverage gaps, limitations, search context, observation time, and used credits.
5. Do not claim causation, guaranteed ranking gains, or data types absent from coverage.

Use `ask_followup` with `max_credits: 2` for a concrete unresolved question about the existing analysis. Reuse the returned analysis session and use a stable new idempotency key for that follow-up.

## Tool failures

- Missing authentication: instruct the user to complete OpenGain OAuth for the `opengain` connection.
- Insufficient credits: report the required and available amounts returned by the server.
- GSC unavailable: continue with other evidence and state the limitation.
- Partial provider coverage: present supported findings and list unavailable evidence explicitly.
