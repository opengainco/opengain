---
name: geo-aeo
description: Improve generative-engine and answer-engine visibility through crawler access, citation-ready content, entity clarity, source quality, and direct-answer structure, and measure whether AI assistants mention or cite a brand.
---

# GEO and AEO

Optimize for accurate discovery and citation without promising inclusion in an AI answer.

## Process

1. Check whether important public pages are accessible to ordinary browsers and relevant search or AI crawlers without authentication, broken rendering, or contradictory robots controls.
2. Inspect whether the page states who produced the content, what entity it describes, when material facts were updated, and what primary sources support consequential claims.
3. Evaluate direct-answer structure: clear definitions, concise summaries, descriptive headings, tables or lists where appropriate, and passages that remain meaningful when quoted out of context.
4. Review entity consistency across titles, organization/person markup, about/contact pages, author profiles, and cited external sources.
5. Identify unsupported superlatives, vague assertions, circular citations, and claims whose sources are stale or secondary.
6. Treat `llms.txt` as an optional discovery aid, not an indexing or citation guarantee. Do not downgrade an otherwise strong site solely because it is absent.
7. Separate crawler accessibility from content quality and from measured AI visibility. Only claim measured visibility when a suitable tool produced evidence.

## Measure AI visibility

The review above never establishes whether an assistant names or cites the brand. When the user wants measured visibility rather than a readiness review, produce that evidence with the `opengain` MCP server. Do not replace missing tool results with guesses.

### Required inputs

- Subject public domain or URL.
- The topic people ask assistants about, in the words they would use.
- Competitor domain or URL when the question is about a competitor being recommended instead.
- Search context when known: country, language, and desktop or mobile.

Default search context to United States, English, desktop only when the user has not supplied market context and that default is reasonable. State the default in the result.

### Start the analysis

Call `start_analysis` with a free-form `question` phrased so the service classifies it as an AI-visibility question. Use one of these shapes:

- `Why don't AI assistants mention <domain> when people ask about <topic>?`
- `Why do AI assistants recommend <competitor> instead of <domain> for <topic>?`

The first measures mentions and citations for one brand; the second adds the competitor comparison. Name the assistants, the domain, and the topic explicitly. An incomplete question returns a clarification draft and spends no credits, so answer the draft rather than starting a second run.

Also send:

- `max_credits: 15` for the default of one run per engine, or `18` when `include_gsc` is true.
- `include_gsc: true` when the subject is the user's site or the user asks to use owned-site data. The service safely reports unavailable GSC as a limitation. Otherwise use `false`.
- `search_context` from the request when the user supplied market context.
- A unique idempotency key of at least eight characters. Keep the same key when retrying the same logical request; create a new key for changed inputs.

Send `runs: 3` with `max_credits: 30` only when the user wants mention rates, and `runs: 5` with `max_credits: 45` for the highest precision. Mention-rate claims require at least three runs per engine: with one run the report states presence or absence only.

Start immediately once required inputs are known. The credit cap is a maximum reservation, not a claim that all credits will be consumed; a cap too small to cover an engine drops that engine from the plan.

### Poll

Use the returned analysis ID with `get_analysis`. Poll with bounded backoff until status is `completed`, `failed`, or `cancelled`. Avoid rapid repeated calls. Report meaningful stage/progress changes if the user is waiting.

If the run fails, report its error and retryability. Do not automatically create a different paid run unless the user's inputs changed or they request a retry.

### Interpret

For a completed report:

1. Keep the two channels separate. A mention is the brand named in the answer text; a citation is a brand domain in the answer's sources; a retrieved but uncited source is neither.
2. Report per engine, and preserve the sampling disclosure. With one run per engine, state presence or absence only; mention-rate language requires at least three runs per engine.
3. Treat an unsupported premise as the answer. An assistant that already mentions or cites the brand answers the question; do not restate the premise as a finding.
4. Tie recommendations to evidence IDs, preserve impact and confidence labels, and distinguish observations from inference.
5. Include coverage gaps, limitations, search context, observation time, and used credits.
6. Do not promise inclusion in a future AI answer, claim causation, or report engines the run did not sample.

Use `ask_followup` with `max_credits: 2` for a concrete unresolved question about the existing analysis. Reuse the returned analysis session and use a stable new idempotency key for that follow-up.

### Tool failures

- Missing authentication: instruct the user to complete OpenGain OAuth for the `opengain` connection.
- Insufficient credits: report the required and available amounts returned by the server.
- Engine unavailable or skipped: present the engines that answered and name the ones that did not.
- Missing Gemini citations: report them as unavailable evidence, never as evidence that the brand is uncited.

## Output

Prioritize access blockers, factual/source weaknesses, structural improvements, and experiments. For each item include evidence, affected pages, expected benefit, confidence, and a verification approach. Preserve human readability and conversion goals; do not rewrite content into repetitive answer fragments.
