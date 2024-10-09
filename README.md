# Prompt Protection in Python

An example CLI tool in Python that demonstrates how to use Pangea's [Secure Audit
Log][] and [Redact][] services to capture and filter what users are sending to
LLMs:

- [Secure Audit Log][] — Create an event when a human prompt is received.
- [Redact][] — Remove sensitive information from prompts.
- [IP Intel][] — Stop prompts with malicious IP addresses from going to the LLM.
- [URL Intel][] — Stop prompts with malicious URLs from going to the LLM.

## Prerequisites

- Python v3.12 or greater.
- pip v24.2 or [uv][] v0.4.5.
- A [Pangea account][Pangea signup] with Secure Audit Log and Redact enabled.
- An [OpenAI API key][OpenAI API keys].

## Setup

```shell
git clone https://github.com/pangeacyber/python-prompt-protection.git
cd python-prompt-protection
```

If using pip:

```shell
python -m venv .venv
source .venv/bin/activate
pip install .
```

Or, if using uv:

```shell
uv sync
source .venv/bin/activate
```

Then the app can be executed with:

```shell
python prompt_protection.py "Give me information on John Smith."
```

## Usage

```
Usage: prompt_protection.py [OPTIONS] PROMPT

Options:
  --model TEXT             OpenAI model.  [default: gpt-4o-mini; required]
  --audit-token TEXT       Pangea Secure Audit Log API token. May also be set
                           via the `PANGEA_AUDIT_TOKEN` environment variable.
                           [required]
  --audit-config-id TEXT   Pangea Secure Audit Log configuration ID.
  --redact-token TEXT      Pangea Redact API token. May also be set via the
                           `PANGEA_REDACT_TOKEN` environment variable.
                           [required]
  --redact-config-id TEXT  Pangea Redact configuration ID.
  --pangea-domain TEXT     Pangea API domain. May also be set via the
                           `PANGEA_DOMAIN` environment variable.  [default:
                           aws.us.pangea.cloud; required]
  --openai-api-key TEXT    OpenAI API key. May also be set via the
                           `OPENAI_API_KEY` environment variable.  [required]
  --help                   Show this message and exit.
```

## Example

With the "Person" Redact rule enabled, names will be redacted. So a prompt like
the following:

```shell
python prompt_protection.py "Give me information on John Smith."
```

Will result in "Give me information on \<PERSON\>." being sent to the LLM
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

[Redact]: https://pangea.cloud/docs/redact/
[Secure Audit Log]: https://pangea.cloud/docs/audit/
[Pangea signup]: https://pangea.cloud/signup
[OpenAI API keys]: https://platform.openai.com/api-keys
[uv]: https://docs.astral.sh/uv/
