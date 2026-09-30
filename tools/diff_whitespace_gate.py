"""Run git diff --check with exact historical line exceptions."""

from __future__ import annotations

import re
import subprocess
import sys
from collections.abc import Sequence

APPROVED_EXCEPTIONS = frozenset(
    {
        "reports/SERVICE_AUDIT_ALIGNMENT_MATRIX.md:3",
        "reports/SERVICE_AUDIT_ALIGNMENT_MATRIX.md:4",
    }
)
FINDING = re.compile(r"^(?P<path>.+):(?P<line>\d+): .+\.$")


def evaluate_output(output: str, returncode: int) -> tuple[bool, list[str], str]:
    """Return pass status, accepted findings, and a diagnostic message."""
    if returncode == 0 and not output.strip():
        return True, [], "PASS: no whitespace violations."

    findings: list[str] = []
    unparsed: list[str] = []
    for line in output.splitlines():
        match = FINDING.match(line)
        if match:
            findings.append(f"{match.group('path')}:{match.group('line')}")
        elif line.startswith("+"):
            # git diff --check prints the offending added line after its diagnostic.
            continue
        elif line.strip():
            unparsed.append(line)

    if unparsed or returncode not in (0, 2):
        details = "\n".join(unparsed) or f"git diff --check exited with {returncode}"
        return False, [], f"FAIL: could not safely interpret git diff --check output:\n{details}"

    unexpected = sorted(set(findings) - APPROVED_EXCEPTIONS)
    if unexpected:
        return False, [], "FAIL: unapproved whitespace violations:\n" + "\n".join(unexpected)
    if len(findings) != len(set(findings)):
        return False, [], "FAIL: duplicate whitespace findings were reported."

    if findings:
        accepted = sorted(findings)
        return (
            True,
            accepted,
            "PASS_WITH_DOCUMENTED_EXCEPTION: accepted historical whitespace findings:\n"
            + "\n".join(accepted),
        )

    if returncode != 0:
        return False, [], f"FAIL: git diff --check exited with {returncode} without parsed findings."
    return True, [], "PASS: no whitespace violations."


def main(args: Sequence[str]) -> int:
    if len(args) != 1:
        print("Usage: python tools/diff_whitespace_gate.py <base>...<head>", file=sys.stderr)
        return 2
    result = subprocess.run(
        ["git", "diff", "--check", args[0]],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    passed, _, message = evaluate_output(result.stdout + result.stderr, result.returncode)
    print(message)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
