# Plugin acceptance tests

`fixtures/seo-site` is a small, intentionally flawed static website used to test the OpenGain skills in Claude Code and Codex without crawling a live site.

Run the repository checks first:

```bash
python3 scripts/validate_repository.py
claude plugin validate .
claude plugin validate ./plugins/opengain
```

Then open the fixture as the host workspace and ask the prompts in `evals.json`. A successful response should cite repository evidence, identify the expected issues, avoid claiming that a live crawl or Search Console check occurred, and avoid editing files unless the prompt explicitly asks for implementation.

Host output and production MCP responses may contain account or analysis data. Keep those artifacts in a temporary directory and never commit them here.

`oauth/client-metadata.json` is a secret-free Client ID Metadata Document for the release acceptance test. Its only redirect target is a fixed loopback callback, and it cannot authenticate a user without OpenGain sign-in and consent.
