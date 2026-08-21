# Contextual Prompt

You are an expert Python developer specializing in secure, production-ready API integrations. Below is the current version of a tool called `sentiment_analyzer.py`, which analyzes the sentiment of a sentence using a public Text Processing API.

```python
#!/usr/bin/python3
"""
Sentiment Analysis Tool
Analyzes the sentiment of a given sentence using a public API.
"""
import requests
import sys


def analyze_sentiment(text):
    """
    Analyzes the sentiment of the given text using the Text Processing API.

    Args:
        text (str): The sentence to analyze

    Returns:
        str: The sentiment label (positive, negative, or neutral)
    """
    url = "https://api.text-processing.com/api/sentiment/"
    payload = {"text": text}

    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()  # Raises exception for 4xx/5xx status codes
        data = response.json()
        label = data.get('label', 'neutral')

        # Map API response format to our desired output
        if label == 'pos':
            return 'positive'
        elif label == 'neg':
            return 'negative'
        else:
            return 'neutral'

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}", file=sys.stderr)
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}", file=sys.stderr)
        return None
    except (KeyError, ValueError) as e:
        print(f"Invalid response format: {e}", file=sys.stderr)
        return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./sentiment_analyzer.py <sentence>")
        sys.exit(1)

    sentence = " ".join(sys.argv[1:])
    result = analyze_sentiment(sentence)

    if result:
        print(result)
    else:
        sys.exit(1)
```

I need you to refactor the `analyze_sentiment` function with the following two non-functional requirements:

1. **Secure API key handling**: The hypothetical Text Processing API now requires an API key for authentication. Modify the function to securely read an API key from the environment variable `TEXT_PROCESSING_API_KEY` (using the `os` module — add the necessary import), and include it in the outgoing request headers using the standard `Authorization: Bearer <key>` format. If the environment variable is not set, the function should fail gracefully with a clear error message rather than sending a request with a missing/empty key.

2. **Enhanced error handling**: Expand the existing try/except block to explicitly catch `requests.exceptions.Timeout` and `requests.exceptions.ConnectionError` as their own distinct except clauses (placed before the more general `requests.exceptions.RequestException` catch, since Python matches except clauses in order). Each new exception type must print its own distinct, informative message to `sys.stderr` (e.g., a Timeout should say the request timed out, and a ConnectionError should say the service could not be reached), so that a person debugging failures in production can immediately tell which kind of network failure occurred rather than seeing one generic "request failed" message for every case.

Please return the complete, updated `sentiment_analyzer.py` file (not just the diff), preserving the existing docstrings, CLI usage behavior, and overall structure, and only changing what's needed to meet the two requirements above.
