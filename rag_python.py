from __future__ import annotations

import sys

import click
from openai import OpenAI
from pangea import PangeaConfig
from pangea.services import Audit, Redact


@click.command()
@click.option("--model", default="gpt-4o-mini", show_default=True, required=True, help="OpenAI model.")
@click.option(
    "--audit-token",
    envvar="PANGEA_AUDIT_TOKEN",
    required=True,
    help="Pangea Secure Audit Log API token. May also be set via the `PANGEA_AUDIT_TOKEN` environment variable.",
)
@click.option(
    "--redact-token",
    envvar="PANGEA_REDACT_TOKEN",
    required=True,
    help="Pangea Redact API token. May also be set via the `PANGEA_REDACT_TOKEN` environment variable.",
)
@click.option(
    "--pangea-domain",
    envvar="PANGEA_DOMAIN",
    default="aws.us.pangea.cloud",
    show_default=True,
    required=True,
    help="Pangea API domain. May also be set via the `PANGEA_DOMAIN` environment variable.",
)
@click.option(
    "--openai-api-key",
    envvar="OPENAI_API_KEY",
    required=True,
    help="OpenAI API key. May also be set via the `OPENAI_API_KEY` environment variable.",
)
@click.argument("prompt")
def main(
    *, prompt: str, model: str, audit_token: str, redact_token: str, pangea_domain: str, openai_api_key: str
) -> None:
    config = PangeaConfig(domain=pangea_domain)
    audit = Audit(token=audit_token, config=config)
    redact = Redact(token=redact_token, config=config)

    # Redact the prompt before sending it to the LLM.
    redacted = redact.redact(text=prompt)
    assert redacted.result
    cleaned_prompt = redacted.result.redacted_text or prompt

    # Log an event regarding this redaction.
    audit.log_bulk([{"message": "Received and redacted prompt to LLM.", "old": prompt, "new": cleaned_prompt}])

    # Generate chat completions.
    stream = OpenAI(api_key=openai_api_key).chat.completions.create(
        messages=[{"role": "user", "content": cleaned_prompt}], model=model, stream=True
    )
    for chunk in stream:
        for choice in chunk.choices:
            sys.stdout.write(choice.delta.content or "")
            sys.stdout.flush()

        sys.stdout.flush()

    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
