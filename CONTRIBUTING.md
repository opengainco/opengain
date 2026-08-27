# Contributing

Contributions that make OpenGain's workflows more accurate, portable, testable, or easier to use are welcome.

## Development

1. Fork and clone the repository.
2. Make changes under `plugins/opengain/`.
3. Keep instructions compatible with both Claude Code and Codex.
4. Do not add credentials, private datasets, copied proprietary prompts, or generated customer reports.
5. Run the repository validator:

```bash
python3 scripts/validate_repository.py
```

When Claude Code is installed, also run:

```bash
claude plugin validate .
claude plugin validate ./plugins/opengain
```

Use a fresh conversation for manual routing tests. Do not make paid OpenGain calls in automated tests.

## Pull requests

Explain the user problem, the behavior change, and how you tested it. Changes to tool names, MCP URLs, credit defaults, or skill safety boundaries should include matching documentation and validator updates.
