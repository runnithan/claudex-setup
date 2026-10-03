"""Regression cases for hooks/block-destructive-push.py.

The hook reads a PreToolUse payload on stdin and exits 2 to block a destructive
git push, 0 otherwise. Each case runs the real script in a subprocess, so the
test exercises the same contract Claude Code does.

Run: uv run --with pytest pytest -q tests/
"""

import json
import shlex
import subprocess
import sys
from pathlib import Path

import pytest

HOOK = Path(__file__).resolve().parent.parent / "hooks" / "block-destructive-push.py"

BLOCK = [
    # Plain and flag-after-remote spellings.
    "git push --force",
    "git push --mirror",
    "git push --no-verify -f",
    "git push -fu origin",
    "git push -d origin foo",
    "git push origin main -d",
    "git push --force-with-lease=main origin",
    "git push --force-with-lease=main origin main",
    "git push origin +main",
    "git push origin :old",
    "git push origin ':old'",
    # Wrappers, path-qualified git and git global options.
    "/usr/bin/git push --force origin main",
    "env git push -f",
    "command git push -f",
    "time git push -f",
    "FOO=1 git push -f",
    "git -C /p push -f",
    "git -c a=b push -f",
    "git -C \"${PWD}\" push -f",
    "git --config-env http.extraHeader=AUTH_HEADER push origin --force",
    # Shells, chains, groups and substitutions.
    "bash -c 'git push -f'",
    "bash -lc 'git push -f'",
    "sh -c \"git push origin --delete foo\"",
    "sh -c 'git -C repo push --force'",
    "bash -c \"cd x && git push -f\"",
    "cd x && git push -f",
    "(git push -f)",
    "(cd x; git push --delete origin y)",
    "{ git push -f; }",
    "echo $(git push -f)",
    "echo `git push -f`",
    "git commit -m \"$(git push -f)\"",
    # Shell expansions must not split the command apart.
    "git push \"${REMOTE}\" main --force",
    "git push origin \"${BRANCH}\" --force",
    # `--` ends option parsing, not refspec parsing.
    "git push -- origin :old-branch",
    "git push -- origin +main",
    "git push origin -- +HEAD:main",
    # Comments end at the newline; redirects do not end the command.
    "echo ready # note\ngit push origin --force",
    "git push origin topic#123 --force",
    "git push origin 2>/dev/null --force",
    "git push origin --force &>/dev/null",
    "git push origin --force 2>&1 | tee log",
    # Quoting inside a substitution is the inner command's own quoting.
    "echo \"$(git push origin '--force')\"",
    "echo \"$(git push origin '+main')\"",
    "echo \"$(printf \")\"; git push origin --force)\"",
    "bash -c \"git push origin \\\"--force\\\"\"",
    "echo \"${UNSET:-'$(git push origin --force)'}\"",
    "echo \"$(case x in x) git push origin --force;; esac)\"",
    "echo \"$(true # )\ngit push origin --force)\"",
    "bash -c 'git push origin \"$@\"' _ --force main",
    "echo ${UNSET:-<(git push origin --force)}",
    "echo ${UNSET:-\"'$(git push origin --force)'\"}",
    "bash -c 'git push origin \"$0\"' --force",
    "bash -c 'git push origin \"$@\" # note' _ --force",
    # Shell keywords before a command.
    "if true; then git push -f; fi",
    "! git push -f",
    # Heredocs whose body runs, or a push after the heredoc closes.
    "bash <<EOF\ngit push -f\nEOF",
    "cat <<'EOF' | sh\ngit push --force\nEOF",
    "cat <<EOF\nhello\nEOF\ngit push -f",
    "git commit -F - <<'EOF'\nmsg\nEOF\ngit push origin +main",
]

ALLOW = [
    "git push",
    "git push origin main",
    "git push -u origin feat",
    "git push --set-upstream origin x",
    "git push --tags",
    "git push --follow-tags",
    "git push --follow-tags origin main",
    "git push --dry-run",
    "git push origin HEAD:main",
    "git push origin HEAD:refs/heads/feat",
    "git -C /p push origin main",
    "npm test && git push origin main",
    "git status",
    "git log -p",
    "ls -d x",
    "bash -c \"git push origin main\"",
    # Mentions in data, not commands.
    "git commit -m \"git push -f\"",
    "git commit -m \"docs: never git push -f\"",
    "echo \"git push --force\"",
    "echo \"(git push --force)\"",
    "grep x <<< 'git push -f'",
    "git commit -F - <<'EOF'\nfix: tidy\n\ngit push -f was never needed\nEOF",
    "cat > notes.md <<EOF\ngit push --force origin main\nEOF",
    "git commit -q -F - <<-EOF\n\tgit push -d origin x\n\tEOF\necho done",
    # Option values are not flags.
    "git push -odraft origin main",
    "git push -o '-draft' origin main",
    "git push -o \"--delete\" origin main",
    # Only the -c string runs; later words are the script's positional args.
    "bash -c 'git push origin main' --force",
    # Lookups and help do not execute git.
    "command -v git push --force",
    "env --help git push -f",
    # Quoted operators and braces are arguments, comments are not run.
    "printf '%s\\n' ';' git push --force",
    "printf '%s\\n' '{' git push --force '}'",
    "git push origin main # --force",
    "echo '$(git push -f)'",
    "bash -c 'git push origin \"$@\"' _ main",
]

# Accepted over-blocks: quote rules inside ${...} depend on the surrounding
# quotes and the operator, so the hook treats any substitution there as live.
# Bash would only print these; blocking them is the safe direction.
FAIL_CLOSED = [
    "echo ${UNSET:-'`git push origin --force`'}",
    "printf '%s\\n' \"${VAR#'`git push --force`'}\"",
]


def nested_shells(command, depth):
    for _ in range(depth):
        command = "bash -c " + shlex.quote(command)
    return command


def run_hook(command):
    payload = json.dumps({"tool_name": "Bash", "tool_input": {"command": command}})
    return subprocess.run([sys.executable, "-I", str(HOOK)], input=payload,
                          capture_output=True, text=True).returncode


@pytest.mark.parametrize("command", BLOCK)
def test_blocks_destructive_push(command):
    assert run_hook(command) == 2


@pytest.mark.parametrize("command", ALLOW)
def test_allows_everything_else(command):
    assert run_hook(command) == 0


@pytest.mark.parametrize("command", FAIL_CLOSED)
def test_ambiguous_expansions_fail_closed(command):
    assert run_hook(command) == 2


@pytest.mark.parametrize("depth", [1, 3, 6, 12])
def test_nested_shells_never_slip_through(depth):
    # Too deep to inspect must fail closed, not pass.
    assert run_hook(nested_shells("git push origin --force", depth)) == 2


def test_parser_overflow_fails_closed():
    command = "$(git push origin --force)"
    for _ in range(600):
        command = "${UNSET:-" + command + "}"
    assert run_hook("echo \"" + command + "\"") == 2


def test_ignores_other_tools():
    payload = json.dumps({"tool_name": "Write", "tool_input": {"command": "git push -f"}})
    result = subprocess.run([sys.executable, "-I", str(HOOK)], input=payload,
                            capture_output=True, text=True)
    assert result.returncode == 0
