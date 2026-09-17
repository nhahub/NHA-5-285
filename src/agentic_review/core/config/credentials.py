"""The provider credential: environment first, then a user-level file outside the repository (FR-1.3a, research R-9).

The value is held in a wrapper that never prints it. Nothing in the repository configuration can supply it.
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import yaml

ENV_VAR = "AGENTIC_REVIEW_API_KEY"
_FOOTER = "Nothing was reviewed."


class Credential:
    __slots__ = ("_value", "source", "location")

    def __init__(self, value: str, *, source: Literal["environment", "user-config"], location: str) -> None:
        self._value = value
        self.source = source
        self.location = location  # the variable name or the file path, never the value

    def reveal(self) -> str:
        return self._value

    def __repr__(self) -> str:
        return f"Credential(source={self.source!r}, location={self.location!r}, value='***')"

    def __str__(self) -> str:
        return "***"


@dataclass(frozen=True)
class CredentialProblem:
    message: str


def user_credential_path(env: Mapping[str, str], *, platform: str = sys.platform) -> Path:
    if platform == "win32":
        appdata = env.get("APPDATA")
        base = Path(appdata) if appdata else _home(env) / "AppData" / "Roaming"
    else:
        xdg = env.get("XDG_CONFIG_HOME")
        base = Path(xdg) if xdg else _home(env) / ".config"
    return base / "agentic-review" / "credentials.yml"


def _home(env: Mapping[str, str]) -> Path:
    home = env.get("HOME") or env.get("USERPROFILE")
    return Path(home) if home else Path.home()


def find_credential(env: Mapping[str, str], repo_root: Path) -> Credential | CredentialProblem:
    value = env.get(ENV_VAR)
    if value:
        return Credential(value, source="environment", location=ENV_VAR)

    path = user_credential_path(env)
    if path.is_file():
        if _is_within(path, repo_root):
            return CredentialProblem(
                f"The user-level credential file {path} is inside the repository at {repo_root}.\n"
                "A credential is never read from a file in the repository. Move it, or set "
                f"{ENV_VAR}.\n{_FOOTER}"
            )
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, yaml.YAMLError):
            data = None
        key = data.get("apiKey") if isinstance(data, dict) else None
        if isinstance(key, str) and key:
            return Credential(key, source="user-config", location=str(path))
        return CredentialProblem(
            f"The credential file {path} exists but holds no 'apiKey: <key>' entry.\n{_FOOTER}"
        )

    return CredentialProblem(
        "No provider credential was found. Looked in:\n"
        f"  the environment variable {ENV_VAR}\n"
        f"  the user-level file {path} (containing 'apiKey: <key>')\n"
        f"{_FOOTER} Supply the credential in one of these places and re-run."
    )


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True
