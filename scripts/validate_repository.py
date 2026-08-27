#!/usr/bin/env python3
"""Dependency-free structural and secret-safety checks for the OpenGain plugin."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "opengain"
EXPECTED_SKILLS = {
    "competitor-ranking",
    "geo-aeo",
    "implement-seo-fixes",
    "local-international",
    "on-page-content",
    "schema-markup",
    "seo-audit",
    "technical-seo",
}

TEXT_SUFFIXES = {
    "",
    ".json",
    ".md",
    ".py",
    ".txt",
    ".yaml",
    ".yml",
}

SECRET_PATTERNS = {
    "private key": re.compile(r"-----BEGIN(?: [A-Z0-9]+)? PRIVATE KEY-----"),
    "AWS access key": re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    "GitHub token": re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{30,}\b"),
    "OpenAI-style key": re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b"),
    "Anthropic key": re.compile(r"\bsk-ant-[A-Za-z0-9_-]{20,}\b"),
    "Stripe live key": re.compile(r"\b(?:sk|rk)_live_[A-Za-z0-9]{16,}\b"),
    "credential-bearing URL": re.compile(r"https?://[^\s/:]+:[^\s/@]+@"),
}


def fail(message: str) -> None:
    raise AssertionError(message)


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(f"{path.relative_to(ROOT)}: invalid JSON: {error}")


def require_mapping(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, dict):
        fail(f"{label} must be a JSON object")
    return value


def validate_manifests() -> None:
    codex_path = PLUGIN / ".codex-plugin" / "plugin.json"
    claude_path = PLUGIN / ".claude-plugin" / "plugin.json"
    codex = require_mapping(load_json(codex_path), "Codex manifest")
    claude = require_mapping(load_json(claude_path), "Claude manifest")

    for key in ("name", "version", "description", "homepage", "repository", "license"):
        if codex.get(key) != claude.get(key):
            fail(f"plugin manifests disagree on {key}")
    if codex.get("name") != PLUGIN.name:
        fail("plugin folder and manifest name must match")
    if not re.fullmatch(r"\d+\.\d+\.\d+", str(codex.get("version", ""))):
        fail("plugin version must be strict semver")
    if codex.get("mcpServers") != "./.mcp.json" or claude.get("mcpServers") != "./.mcp.json":
        fail("both plugin manifests must reference ./.mcp.json")
    if codex.get("skills") != "./skills/" or claude.get("skills") != "./skills/":
        fail("both plugin manifests must reference ./skills/")
    interface = require_mapping(codex.get("interface"), "Codex interface")
    prompts = interface.get("defaultPrompt")
    if not isinstance(prompts, list) or not 1 <= len(prompts) <= 3:
        fail("Codex defaultPrompt must contain one to three prompts")
    if not all(isinstance(prompt, str) and 1 <= len(prompt) <= 128 for prompt in prompts):
        fail("Codex default prompts must be non-empty strings of at most 128 characters")


def validate_mcp() -> None:
    config = require_mapping(load_json(PLUGIN / ".mcp.json"), "MCP config")
    servers = require_mapping(config.get("mcpServers"), "mcpServers")
    if set(servers) != {"opengain"}:
        fail("MCP config must expose exactly one server named opengain")
    server = require_mapping(servers["opengain"], "opengain MCP server")
    expected = {"type": "http", "url": "https://opengain.co/mcp"}
    if server != expected:
        fail("opengain MCP server must contain only the approved type and URL")


def validate_marketplaces() -> None:
    claude = require_mapping(load_json(ROOT / ".claude-plugin" / "marketplace.json"), "Claude marketplace")
    codex = require_mapping(load_json(ROOT / ".agents" / "plugins" / "marketplace.json"), "Codex marketplace")
    for label, manifest in (("Claude", claude), ("Codex", codex)):
        if manifest.get("name") != "opengain":
            fail(f"{label} marketplace name must be opengain")
        plugins = manifest.get("plugins")
        if not isinstance(plugins, list) or len(plugins) != 1:
            fail(f"{label} marketplace must contain exactly one plugin")
        entry = require_mapping(plugins[0], f"{label} marketplace plugin")
        if entry.get("name") != "opengain":
            fail(f"{label} marketplace plugin name must be opengain")
        source = entry.get("source")
        path = source if isinstance(source, str) else require_mapping(source, f"{label} source").get("path")
        if path != "./plugins/opengain":
            fail(f"{label} marketplace must reference ./plugins/opengain")


def frontmatter_name(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(?P<header>.*?)\n---\n", text, flags=re.DOTALL)
    if not match:
        fail(f"{path.relative_to(ROOT)}: missing YAML frontmatter")
    header = match.group("header")
    name = re.search(r"^name:\s*([a-z0-9-]+)\s*$", header, flags=re.MULTILINE)
    description = re.search(r"^description:\s*(\S.*)$", header, flags=re.MULTILINE)
    if not name or not description:
        fail(f"{path.relative_to(ROOT)}: frontmatter requires name and description")
    return name.group(1)


def validate_skills() -> None:
    files = sorted((PLUGIN / "skills").glob("*/SKILL.md"))
    names = {frontmatter_name(path) for path in files}
    folders = {path.parent.name for path in files}
    if names != EXPECTED_SKILLS or folders != EXPECTED_SKILLS:
        fail(f"expected exactly these skills: {', '.join(sorted(EXPECTED_SKILLS))}")
    if len(files) != len(names):
        fail("skill frontmatter names must be unique")

    competitor = (PLUGIN / "skills" / "competitor-ranking" / "SKILL.md").read_text(encoding="utf-8")
    for required_text in (
        "start_analysis",
        "get_analysis",
        "ask_followup",
        "max_credits: 30",
        "max_credits: 32",
        "max_credits: 2",
        "idempotency",
        "completed",
        "failed",
        "cancelled",
    ):
        if required_text not in competitor:
            fail(f"competitor-ranking is missing required contract text: {required_text}")

    implementation = (PLUGIN / "skills" / "implement-seo-fixes" / "SKILL.md").read_text(encoding="utf-8")
    if "only when the user requests implementation" not in implementation:
        fail("implement-seo-fixes must preserve the explicit-request boundary")


def repository_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if ".git" in path.parts or path.is_dir():
            continue
        if path.is_symlink():
            fail(f"symlinks are not allowed: {path.relative_to(ROOT)}")
        files.append(path)
    return files


def validate_secret_safety(files: list[Path]) -> None:
    forbidden_names = {".env", ".env.local", ".env.production", ".npmrc", ".pypirc"}
    for path in files:
        relative = path.relative_to(ROOT)
        if path.name in forbidden_names or path.suffix in {".pem", ".p12", ".pfx", ".key"}:
            fail(f"forbidden credential-bearing file: {relative}")
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8")
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                fail(f"possible {label} in {relative}")
        for line_number, line in enumerate(text.splitlines(), start=1):
            assignment = re.match(
                r"\s*(?:export\s+)?[A-Z0-9_]*(?:TOKEN|SECRET|PASSWORD|API_KEY|PRIVATE_KEY)[A-Z0-9_]*\s*=\s*(.+)",
                line,
            )
            if assignment:
                assigned_value = assignment.group(1).strip().strip("\"'")
                safe_values = {"", "placeholder", "example", "changeme", "{", "[", "("}
                if assigned_value not in safe_values:
                    fail(f"possible assigned secret in {relative}:{line_number}")


def validate_internal_links(files: list[Path]) -> None:
    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for path in files:
        if path.suffix.lower() != ".md":
            continue
        text = path.read_text(encoding="utf-8")
        for target in link_pattern.findall(text):
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            clean_target = target.split("#", 1)[0]
            if clean_target and not (path.parent / clean_target).resolve().exists():
                fail(f"broken relative link in {path.relative_to(ROOT)}: {target}")


def main() -> int:
    validate_manifests()
    validate_mcp()
    validate_marketplaces()
    validate_skills()
    files = repository_files()
    validate_secret_safety(files)
    validate_internal_links(files)
    print(f"Validated {len(files)} files, 8 skills, 2 plugin manifests, and 2 marketplaces.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as error:
        print(f"validation failed: {error}", file=sys.stderr)
        raise SystemExit(1)
