#!/usr/bin/env python3
"""Read-only, dependency-free security triage scanner.

Reports candidate locations without printing matched values. Results require review.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


DEFAULT_EXCLUDES = {
    ".git", ".hg", ".svn", ".idea", ".vscode", "node_modules", "vendor",
    "dist", "build", "coverage", "target", "__pycache__", ".venv", "venv",
    ".tox", ".mypy_cache", ".pytest_cache", ".next", ".cache",
}
TEXT_SUFFIXES = {
    ".py", ".pyi", ".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx", ".java",
    ".go", ".rs", ".rb", ".php", ".cs", ".sh", ".bash", ".zsh", ".ps1",
    ".sql", ".html", ".htm", ".vue", ".svelte", ".yaml", ".yml", ".json",
    ".toml", ".ini", ".cfg", ".conf", ".properties", ".xml", ".env",
}
TEXT_NAMES = {
    "dockerfile", "containerfile", "makefile", "procfile", "jenkinsfile",
    "gemfile", "rakefile", "requirements.txt", "pipfile", "poetry.lock",
    "package-lock.json", "pnpm-lock.yaml", "yarn.lock", "cargo.lock", "go.sum",
}
MAX_FILE_BYTES = 2 * 1024 * 1024


@dataclass(frozen=True)
class Rule:
    rule_id: str
    severity: str
    title: str
    pattern: re.Pattern[str]
    suffixes: frozenset[str] | None = None


@dataclass(frozen=True)
class Finding:
    rule_id: str
    severity: str
    title: str
    file: str
    line: int
    status: str = "needs-verification"


RULES = (
    Rule("SEC001", "critical", "Private key material", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----")),
    Rule("SEC002", "critical", "AWS access key identifier", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    Rule("SEC003", "high", "GitHub token-like value", re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{30,255}\b")),
    Rule("SEC004", "high", "OpenAI key-like value", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b")),
    Rule("SEC005", "high", "Bearer token literal", re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._~+/=-]{20,}")),
    Rule("SEC101", "high", "Python dynamic code execution", re.compile(r"\b(?:eval|exec)\s*\("), frozenset({".py", ".pyi"})),
    Rule("SEC102", "high", "Python subprocess shell mode", re.compile(r"\bshell\s*=\s*True\b"), frozenset({".py", ".pyi"})),
    Rule("SEC103", "medium", "Python unsafe pickle load", re.compile(r"\bpickle\.(?:load|loads)\s*\("), frozenset({".py", ".pyi"})),
    Rule("SEC104", "medium", "Python weak security hash candidate", re.compile(r"\bhashlib\.(?:md5|sha1)\s*\("), frozenset({".py", ".pyi"})),
    Rule("SEC105", "high", "TLS certificate verification disabled", re.compile(r"\bverify\s*=\s*False\b"), frozenset({".py", ".pyi"})),
    Rule("SEC201", "high", "JavaScript dynamic code execution", re.compile(r"\b(?:eval|Function)\s*\("), frozenset({".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx"})),
    Rule("SEC202", "high", "Node string-based command execution", re.compile(r"\b(?:exec|execSync)\s*\("), frozenset({".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx"})),
    Rule("SEC301", "medium", "Potential SQL string assembly", re.compile(r"(?i)(?:select|insert|update|delete).*(?:\+|\$\{|%s|\.format\()"), frozenset({".py", ".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx", ".java", ".rb", ".php", ".cs"})),
)


def is_text_candidate(path: Path) -> bool:
    return path.suffix.lower() in TEXT_SUFFIXES or path.name.lower() in TEXT_NAMES


def iter_files(root: Path, excludes: set[str]) -> Iterable[Path]:
    if root.is_file():
        if not root.is_symlink() and is_text_candidate(root):
            yield root
        return
    for current, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in excludes and not Path(current, d).is_symlink())
        for name in sorted(files):
            path = Path(current, name)
            if path.is_symlink() or not is_text_candidate(path):
                continue
            try:
                if path.stat().st_size <= MAX_FILE_BYTES:
                    yield path
            except OSError:
                continue


def scan(root: Path, excludes: set[str]) -> tuple[list[Finding], list[str]]:
    findings: list[Finding] = []
    errors: list[str] = []
    script_path = Path(__file__).resolve()
    for path in iter_files(root, excludes):
        try:
            if path.resolve() == script_path:
                continue
            text = path.read_text(encoding="utf-8", errors="strict")
        except (OSError, UnicodeError) as exc:
            errors.append(f"{path}: {type(exc).__name__}")
            continue
        suffix = path.suffix.lower()
        try:
            display = str(path.resolve().relative_to(root if root.is_dir() else root.parent))
        except ValueError:
            display = path.name
        for line_no, line in enumerate(text.splitlines(), start=1):
            for rule in RULES:
                if rule.suffixes is not None and suffix not in rule.suffixes:
                    continue
                if rule.pattern.search(line):
                    findings.append(Finding(rule.rule_id, rule.severity, rule.title, display, line_no))
    findings.sort(key=lambda f: (f.file.lower(), f.line, f.rule_id))
    return findings, errors


def render_markdown(root: Path, findings: list[Finding], errors: list[str]) -> str:
    lines = [
        "# Security triage results",
        "",
        f"Scope: `{root}`",
        "",
        "> Candidate patterns only. Manually confirm source-to-sink flow, guards, reachability, and impact.",
        "",
    ]
    if findings:
        lines.extend(["| Rule | Candidate severity | Location | Pattern | Status |", "|---|---|---|---|---|"])
        lines.extend(
            f"| {f.rule_id} | {f.severity} | `{f.file}:{f.line}` | {f.title} | {f.status} |"
            for f in findings
        )
    else:
        lines.append("No candidate patterns detected in the scanned files. This is not proof of security.")
    if errors:
        lines.extend(["", "## Files not scanned", ""])
        lines.extend(f"- `{error}`" for error in errors)
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Read-only security triage; matched values are never printed.")
    parser.add_argument("path", type=Path, help="File or directory to scan")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--exclude", action="append", default=[], help="Additional directory name to exclude")
    parser.add_argument("--fail-on-candidates", action="store_true", help="Exit 1 when candidates are found")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.path.expanduser().resolve()
    if not root.exists():
        print(f"error: path does not exist: {root}", file=sys.stderr)
        return 2
    findings, errors = scan(root, DEFAULT_EXCLUDES | set(args.exclude))
    if args.format == "json":
        print(json.dumps({"scope": str(root), "findings": [asdict(f) for f in findings], "errors": errors}, indent=2))
    else:
        print(render_markdown(root, findings, errors))
    return 1 if args.fail_on_candidates and findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
