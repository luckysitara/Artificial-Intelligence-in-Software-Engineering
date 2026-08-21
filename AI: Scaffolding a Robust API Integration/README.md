# AI: Scaffolding a Robust API Integration

## Overview
This task demonstrates using a **Contextual Prompting** technique to have an AI tool refactor an existing Python sentiment-analysis script (`sentiment_analyzer.py`) so that it (1) securely handles API key authentication and (2) has more comprehensive, specific network-error handling.

## AI Tool Used
Claude (Anthropic)

## Files in this folder
- `sentiment_analyzer_original.py` — the starting version of the script, which sends unauthenticated requests and only catches generic `HTTPError` / `RequestException` / `(KeyError, ValueError)`.
- `sentiment_analyzer_refactored.py` — the AI-refactored version generated from the contextual prompt in `contextual_prompt.md`.
- `contextual_prompt.md` — the full contextual prompt submitted to the AI, including the original code as context and the two explicit requirements (secure API key handling, expanded exception handling).

## What changed
1. **Secure API key handling**: Added `import os` and read `TEXT_PROCESSING_API_KEY` from the environment. The key is sent as an `Authorization: Bearer <key>` header rather than being hardcoded or omitted. If the environment variable isn't set, the function fails fast with a clear configuration error instead of sending an unauthenticated request.
2. **Enhanced error handling**: Added explicit `requests.exceptions.Timeout` and `requests.exceptions.ConnectionError` except clauses (ordered before the general `RequestException` catch, since Python evaluates except blocks top-to-bottom), each printing a distinct, actionable message to `sys.stderr`. Also added an explicit `timeout=10` to the request itself so the Timeout branch can actually trigger.

## How to run
```bash
export TEXT_PROCESSING_API_KEY="your-key-here"
python3 sentiment_analyzer_refactored.py "I love this."
```

## Verification
Running the refactored script with a dummy key against the live (public) endpoint correctly triggered the `HTTPError` branch (403 Forbidden, since the key wasn't valid), confirming the header was built and sent correctly. Running it with the environment variable unset correctly triggered the new configuration guard, confirming the secure key-handling requirement is enforced before any network call is made.
