"""Preflight: everything that can stop a run is checked before any change is resolved or any model is called.

Checks run in the order of contracts/cli.md "Preflight messages" and stop at the first failure (FR-001, AC-9).
Implemented here: 1 (inside a git repository), 2 (configuration valid), 4 (credential available). Checks 3 and 5
(scope arguments, range base) arrive with User Story 3.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from agentic_review.core.changeset.resolve import GitNotFound, locate_repository
from agentic_review.core.config.credentials import ENV_VAR, Credential, CredentialProblem, find_credential
from agentic_review.core.config.loader import ConfigError, LoadedSettings, load_settings
from agentic_review.core.config.redact import redact

CONFIG_FILE_NAME = ".agentic-review.yml"


@dataclass(frozen=True)
class PreflightFailure:
    message: str
    """Already redacted. The CLI prints it to stderr."""


@dataclass(frozen=True)
class PreflightOk:
    repo_root: Path
    loaded: LoadedSettings
    credential: Credential


def preflight(cwd: Path, config_path: Path | None, env: Mapping[str, str]) -> PreflightFailure | PreflightOk:
    secret = env.get(ENV_VAR)

    def fail(message: str) -> PreflightFailure:
        return PreflightFailure(redact(message, secret))

    try:
        repo_root = locate_repository(cwd)
    except GitNotFound:
        return fail("git was not found on PATH, so no repository could be located.\nNothing was reviewed.")
    if repo_root is None:
        return fail(
            f"{cwd} is not inside a git repository.\n"
            "Nothing was reviewed. Run the review from inside the repository you want reviewed."
        )

    explicit = config_path is not None
    path = config_path if config_path is not None else repo_root / CONFIG_FILE_NAME
    try:
        loaded = load_settings(path, explicit=explicit, display_name=str(path) if explicit else CONFIG_FILE_NAME)
    except ConfigError as error:
        return fail(error.message)

    credential = find_credential(env, repo_root)
    if isinstance(credential, CredentialProblem):
        return fail(credential.message)

    return PreflightOk(repo_root=repo_root, loaded=loaded, credential=credential)
