# rag-python

An example CLI tool in Python that demonstrates how to use Pangea's [Secure Audit
Log][] and [Redact][] services to capture and filter what users are sending to
LLMs.

## Prerequisites

- Python v3.12 or greater.
- pip v24.2 or [uv][] v0.4.5.
- A [Pangea account][Pangea signup] with Secure Audit Log and Redact enabled.
- An [OpenAI API key][OpenAI API keys].

## Setup

```shell
$ git clone https://github.com/pangeacyber/rag-python.git
$ cd rag-python

# If using pip:
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install .

# Or, if using uv:
$ uv sync
$ source .venv/bin/activate
```

## Usage

```shell
$ python rag_python.py --help
Usage: rag_python.py [OPTIONS] PROMPT

Options:
  --model TEXT           OpenAI model.  [default: gpt-4o-mini; required]
  --audit-token TEXT     Pangea Secure Audit Log API token. May also be set
                         via the `PANGEA_AUDIT_TOKEN` environment variable.
                         [required]
  --redact-token TEXT    Pangea Redact API token. May also be set via the
                         `PANGEA_REDACT_TOKEN` environment variable.
                         [required]
  --pangea-domain TEXT   Pangea API domain. May also be set via the
                         `PANGEA_DOMAIN` environment variable.  [default:
                         aws.us.pangea.cloud; required]
  --openai-api-key TEXT  OpenAI API key. May also be set via the
                         `OPENAI_API_KEY` environment variable.  [required]
  --help                 Show this message and exit.
```

## Example

With the "Person" Redact rule enabled, names will be redacted. So a prompt like
the following:

```shell
$ python rag_python.py "This is a test message about John Smith."
```

Will result in "This is a test message about \<PERSON\>." being sent to the LLM
instead. This redaction will also be logged in Secure Audit Log like so:

```json
{
  "envelope": {
    "event": {
      "message": "Received and redacted prompt to LLM.",
      "old": "This is a test message about John Smith.",
      "new": "This is a test message about <PERSON>."
    }
  }
}
```

[Redact]: https://pangea.cloud/docs/redact
[Secure Audit Log]: https://pangea.cloud/docs/audit/
[Pangea signup]: https://pangea.cloud/signup
[OpenAI API keys]: https://platform.openai.com/api-keys
[uv]: https://docs.astral.sh/uv/
