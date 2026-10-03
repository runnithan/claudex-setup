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
    "git push origin +:",
    # Git accepts any unique prefix of a long option.
    "git push origin --del old",
    "git push --mirr origin",
    "git push origin --m",
    "git push --pru origin",
    "git push origin --force-w",
    "git push origin --force-wi=main main",
    # Brace expansion runs before git sees its arguments.
    "git push origin --{force,force} main",
    "git push origin -{d..f} old",
    "{git,} push origin --force",
    "git push origin {+main,dev}",
    "git push origin --{mirror,x}",
    "git push origin \"--\"{force,x}",
    "git push origin --{force,force}{,,,,,,,,,}{,,,,,,,,,}{,,,,,,,,,} main",
    "git push -o {--force,--force} origin main",
    # Quoted braces stay literal, so they cannot fabricate a word.
    "git push -o '{x,-o}' --force origin main",
    # A short cluster is read flag by flag, whatever its -o value holds.
    "git push origin -foci.skip main",
    "git push origin -df/x",
    # Wrappers, path-qualified git and git global options.
    "/usr/bin/git push --force origin main",
    "env git push -f",
    "command git push -f",
    "time git push -f",
    "FOO=1 git push -f",
    # Wrapper options that take a value must not hide the program.
    "env -u FOO git push origin --force",
    "env -C /repo git push -f",
    "nice -n 5 git push origin --force",
    "sudo -u me git push origin --force",
    "time -o /tmp/t git push -f",
    "sudo -u me bash -c 'git push -f'",
    "env -u command -v git push origin --force main",
    "timeout 60 git push origin --force",
    "echo x | xargs git push origin --force",
    "xargs -n1 git push origin --delete < branches.txt",
    "stdbuf -oL git push -f",
    "ionice -c3 git push -f",
    "setsid git push -f",
    "doas git push -f",
    "chrt -o 0 git push -f",
    "taskset 1 git push -f",
    # Command strings handed to eval or to a wrapper's -c / -S option.
    "eval 'git push origin --force'",
    "eval \"git push\" --force",
    "command eval 'git push -f'",
    "env -S 'git push origin --force'",
    "env -S'git push origin --force'",
    "env --split-string='git push -f'",
    "su -c 'git push origin --force' me",
    "su me --command='git push -f'",
    "env -vS 'git push origin --force main'",
    "env -S 'git push origin' --force main",
    "env -S'git push origin' -f",
    "env -S 'git push origin \\_--force main'",
    "env -iS'git push -f'",
    "su -lc 'git push -f' me",
    "su --command 'git push -f' me",
    "runuser -u me -- git push -f",
    "script -q -c 'git push -f' /dev/null",
    "flock /tmp/lock -c 'git push -f'",
    "git -C /p push -f",
    "git -c a=b push -f",
    "git -C \"${PWD}\" push -f",
    "git --config-env http.extraHeader=AUTH_HEADER push origin --force",
    # Inline aliases are expanded, and inline config can make a push destructive.
    "git -c alias.p=push p origin --force",
    "git -c alias.P=push p origin --force",
    "git -c 'alias.pf=push --force' pf origin main",
    "git -c 'alias.p=!git push --force' p",
    "git -c 'alias.p=!git push origin' p --force",
    "git -c 'alias.p=!f() { git push origin \"$@\"; }; f' p --force main",
    "git -c alias.a=b -c alias.b=push a origin --force",
    "git --config-env=alias.p=ALIAS p origin",
    "git -c alias.push=status push origin --force main",
    "git -c alias.p=status -c 'alias.p=push --force' p origin main",
    "git -c remote.origin.mirror=true push origin",
    "git -c remote.origin.mirror push origin",
    "git -c remote.origin.mirror=false -c remote.origin.mirror=true push origin main",
    "git -c 'remote.origin.push=+refs/heads/*:refs/heads/*' push origin",
    "git -c remote.origin.push=:old push origin",
    # Config set through the environment counts like -c.
    "GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=remote.origin.mirror GIT_CONFIG_VALUE_0=true git push origin",
    "env GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=alias.p GIT_CONFIG_VALUE_0='push --force' git p origin main",
    "GIT_CONFIG_PARAMETERS=\"'remote.origin.mirror'='true'\" git push origin",
    "GIT_CONFIG_PARAMETERS=\"'alias.a'='b' 'alias.b'='push --force'\" git a origin main",
    "GIT_CONFIG_COUNT=2 GIT_CONFIG_KEY_1=remote.origin.mirror GIT_CONFIG_VALUE_1=true "
    "GIT_CONFIG_KEY_0=remote.origin.mirror GIT_CONFIG_VALUE_0=false git push origin",
    # A child shell inherits the environment, and export keeps it for later.
    "GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=remote.origin.mirror GIT_CONFIG_VALUE_0=true bash -c 'git push origin'",
    "export GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=remote.origin.mirror GIT_CONFIG_VALUE_0=true; git push origin",
    "GIT_CONFIG_PARAMETERS=\"'remote.origin.mirror'='true'\" bash <<'EOF'\ngit push origin\nEOF",
    # Windows and case-insensitive spellings of the same programs.
    "git.exe push origin --force main",
    "GIT.EXE push -f",
    "\"C:\\Program Files\\Git\\cmd\\git.exe\" push -f",
    "bash.exe -c 'git push -f'",
    "env.exe git push -f",
    "bash.exe <<'EOF'\ngit push origin --force\nEOF",
    # An expansion's visible default can supply a destructive argument.
    "git push origin \"${FLAG:---force}\" main",
    "git push origin ${REF-+main}",
    "git push origin ${X:+--delete} old",
    # A program or subcommand built from an expansion could be git or push.
    "p=push; git $p origin --force",
    "git \"$SUB\" origin --force",
    "git $(echo push) origin --force",
    "\"$(command -v git)\" push origin --force",
    "$GIT push -f",
    "${GIT:-git} push origin --force",
    "${RUNNER:-bash} -c 'git push origin --force main'",
    "$RUNNER -c 'git push origin --force main'",
    "${W:-sudo} -u me git push -f",
    "$X git push --force",
    # git-push is git itself, run as the push builtin.
    "/usr/lib/git-core/git-push origin --force main",
    "\"$(git --exec-path)/git-push\" origin -f",
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
    "git -C { push origin --force main",
    "git -C } push -f",
    "echo $(git push -f)",
    "echo `git push -f`",
    # Backticks strip one level of \\, \$ and \` before the body runs.
    "echo `git push origin \\\\--force main`",
    "echo `git push origin \\$'--force'`",
    "echo `echo \\`git push origin --force\\``",
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
    # `case` is a keyword only where a command starts, not as an argument.
    "echo \"$(echo case; git push origin $'--force' main)\"",
    "echo \"$(if true; then case x in x) echo ok;; esac; fi; git push origin $'-f')\"",
    "echo \"$(true # )\ngit push origin --force)\"",
    "bash -c 'git push origin \"$@\"' _ --force main",
    "echo ${UNSET:-<(git push origin --force)}",
    "echo ${UNSET:-\"'$(git push origin --force)'\"}",
    "bash -c 'git push origin \"$0\"' --force",
    "bash -c 'git push origin \"$@\" # note' _ --force",
    "bash -c 'git push origin \"$2\" main' _ -o --force",
    "bash -c 'git push origin \"$2\"' _ -- :old",
    "bash -c 'git pu\"\"sh origin \"$@\"' _ --force main",
    "bash -c 'git p\\ush origin \"$1\"' _ --force",
    "bash -c 'git \"$1\" origin \"$2\"' _ push --force",
    "bash -c '\"$@\"' _ git push --force",
    "bash -c 'git push origin \"${!#}\" main' _ --force",
    "bash -c '\"$@\"' _ /usr/lib/git-core/git-push origin --force main",
    # Shell options may follow -c; the first non-option word is the script.
    "bash -c -e 'git push origin --force'",
    "bash -c -- 'git push origin --force'",
    "bash -c - 'git push origin --force'",
    "bash -c -o pipefail 'git push origin --force'",
    "bash -eo pipefail -c 'git push origin --force'",
    "bash --rcfile /dev/null -c 'git push origin --force'",
    # ANSI-C and locale quoting are decoded like any other quote.
    "git push origin $'--force' main",
    "git push origin $'--f\\x6frce' main",
    "git push origin $'\\053main'",
    "git push origin $\"--force\" main",
    "git push origin $'--force\\0' main",
    "git push origin $'--fo\\0junk'rce main",
    "git push origin $'--force\\c@x' main",
    "echo \"$(git push origin $'--force')\"",
    "echo \"$(: $'it\\'s'; git push origin $'--force' main)\"",
    # Shell keywords before a command.
    "if true; then git push -f; fi",
    "! git push -f",
    "coproc git push origin --force main",
    "coproc pusher { git push -f; }",
    # Heredocs whose body runs, or a push after the heredoc closes.
    "bash <<EOF\ngit push -f\nEOF",
    "cat <<'EOF' | sh\ngit push --force\nEOF",
    "cat <<EOF\nhello\nEOF\ngit push -f",
    "git commit -F - <<'EOF'\nmsg\nEOF\ngit push origin +main",
    # Only a real redirect opens a heredoc, a shell is found by its basename,
    # and the terminator must match exactly.
    "echo '<<EOF'\ngit push origin --force",
    "echo ready # <<EOF\ngit push origin --force",
    "/bin/bash <<'EOF'\ngit push origin --force\nEOF",
    "cat <<'EOF'\n EOF\ncat <<X\nEOF\ngit push origin --force",
    "echo \"$(bash <<'EOF'\ngit push origin --force\nEOF\n)\"",
    "cat <<EOF\nbody\nEO\\\nF\ngit push origin --force main",
    # A here-string fed to a shell is its script.
    "bash <<< 'git push origin --force main'",
    "sh <<< \"git push -f\"",
    "bash <<<'git push -f'; echo done",
    "echo hi\n/bin/bash <<< 'git push -f'",
    # A shell after the heredoc's command can still run what it wrote.
    "cat <<'EOF' > s.sh && bash s.sh\ngit push --force\nEOF",
    "bash -c ':'; bash -s -- --force <<'EOF'\ngit push origin \"$1\"\nEOF",
    # An unquoted body loses one level of \\, \$ and \` before bash reads it.
    "bash <<EOF\ngit push origin \\\\--force main\nEOF",
    "bash <<EOF\n\\$(git push origin --force)\nEOF",
    # A shell reading its script on stdin still forwards its own arguments.
    "bash -s -- --force main <<'EOF'\ngit push origin \"$1\" \"$2\"\nEOF",
    "bash -s --force <<< 'git push origin \"$1\"'",
    # An unquoted heredoc body is expanded, so its substitutions run.
    "cat <<EOF\n$(git push origin --force)\nEOF",
    "cat <<EOF\nnever run `git push origin --force`\nEOF",
    "cat > notes.md <<EOF\n${X:-$(git push origin --force)}\nEOF",
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
    "git push origin {main,dev}",
    "git log HEAD@{1} && git push origin main",
    "git push origin --{mirror}{,} main",
    "git push origin '--{force,x}' main",
    "git push -o \"{a,b}\" origin main",
    "for i in {1..5000}; do echo $i; done",
    "echo ${X:-{a,--force}} && git push origin main",
    # The bare `:` refspec pushes matching branches; it deletes nothing.
    "git push origin :",
    "git -C /p push origin main",
    "git -c alias.st=status st",
    "git -c alias.p=push p origin main",
    "git -c 'alias.push=push --force' push origin main",
    "git -c 'alias.p=push --force' -c alias.p=status p origin main",
    "git -c remote.origin.mirror=false push origin main",
    "git -c remote.origin.mirror=true -c remote.origin.mirror=false push origin main",
    "git -c remote.origin.push=refs/heads/main:refs/heads/main push origin",
    "git -c core.editor=vim commit",
    "GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=user.name GIT_CONFIG_VALUE_0=me git push origin main",
    "GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=user.name GIT_CONFIG_VALUE_0=me bash -c 'git push origin main'",
    "GIT_CONFIG_COUNT=2 GIT_CONFIG_KEY_1=remote.origin.mirror GIT_CONFIG_VALUE_1=false "
    "GIT_CONFIG_KEY_0=remote.origin.mirror GIT_CONFIG_VALUE_0=true git push origin main",
    "GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=alias.p GIT_CONFIG_VALUE_0='push --force' git -c alias.p=status p",
    "/usr/lib/git-core/git-push origin main",
    "git $SUB origin main",
    "git push origin \"${BRANCH:-main}\"",
    "$EDITOR notes.md",
    "\"$PY\" -c 'print(\"git push --force\")'",
    "${RUNNER:-bash} -c 'git push origin main'",
    "\"$(command -v git)\" push origin main",
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
    "cat <<< 'git push origin --force'",
    "bash -s -- --force <<'EOF'\necho \"$1\"\nEOF",
    "bash <<'EOF'\ngit push origin \\\\--force main\nEOF",
    "bash -s -- main <<'EOF'\ngit push origin \"$1\"\nEOF",
    "git commit -F - <<'EOF'\nfix: tidy\n\ngit push -f was never needed\nEOF",
    "cat > notes.md <<EOF\ngit push --force origin main\nEOF",
    "git commit -q -F - <<-EOF\n\tgit push -d origin x\n\tEOF\necho done",
    "git commit -F - <<\\EOF\ngit push -f\nEOF",
    "cat <<'EOF'\n EOF\ngit push origin --force\nEOF",
    "cat <<'EOF'\nEO\\\nF\ngit push origin --force main\nEOF",
    "cat <<EOF\npath C:\\\\\ngit push origin --force main\nEOF",
    "bash -c 'cat <<EOF\ngit push origin --force\nEOF'",
    "cat <<'EOF'\n$(git push origin --force)\nEOF",
    "cat <<EOF\n\\$(git push origin --force)\nEOF",
    "git commit -F - <<EOF\nfix: it's (done\n\ngit push -f was wrong\nEOF",
    # A shell that ran before the heredoc's command cannot read its body.
    "bash scripts/gate.sh frontend > /tmp/g.log 2>&1; git commit -F - <<'EOF'\n"
    "fix: the \"pill\" said it's saving\n\ngit push --force was never needed\nEOF",
    # A heredoc inside $(...) is data too, whatever quotes or parens it holds.
    "git commit -m \"$(cat <<'EOF'\nfix: don't\n\ngit push -f was wrong\nEOF\n)\"",
    "git commit -m \"$(cat <<'EOF'\nfix: (a\n\ngit push -f was wrong\nEOF\n)\"",
    "git commit -m \"$(cat <<-EOF\n\tfix: it's\n\tgit push -d origin x\n\tEOF\n)\"",
    # Option values are not flags.
    "git push -odraft origin main",
    "git push -o '-draft' origin main",
    "git push -o \"--delete\" origin main",
    "git push --push-o --force origin main",
    "git push -uoci.skip=f.d origin main",
    "git push --dry origin main",
    "git push --follow origin main",
    # Only the -c string runs; later words are the script's positional args.
    "bash -c 'git push origin main' --force",
    # Lookups and help do not execute git.
    "command -v git push --force",
    "env --help git push -f",
    "sudo command -v git push --force",
    "nice -n 5 git push origin main",
    "timeout 60 git push origin main",
    "eval 'git push origin main'",
    "env -S 'git status'",
    "env -S 'git push origin' main",
    "su -c 'git push origin main' me",
    # A -c value that is not shell (grep's count flag) is data, not a script.
    "command grep -c \"gh\\` CLI\" README.md",
    "command grep -c ' -- \\|\\\\\"' notes.md",
    "sudo -u git git status",
    # Quoted operators and braces are arguments, comments are not run.
    "printf '%s\\n' ';' git push --force",
    "printf '%s\\n' '{' git push --force '}'",
    "printf '%s\\n' \\{ git push origin --force \\}",
    "git push origin main # --force",
    "echo '$(git push -f)'",
    "bash -c 'git push origin \"$@\"' _ main",
    "echo $'it\\'s done' && git push origin main",
    "echo \"$(: $'it\\'s')\" && git push origin main",
    "bash -c 'git status \"$@\"' _ --force",
]

# Accepted over-blocks: quote rules inside ${...} depend on the surrounding
# quotes and the operator, so the hook treats any substitution there as live.
# Bash would only print these; blocking them is the safe direction.
FAIL_CLOSED = [
    "echo ${UNSET:-'`git push origin --force`'}",
    "printf '%s\\n' \"${VAR#'`git push --force`'}\"",
    # A lookup after a wrapper option cannot be told from an option value
    # (`env -u command -v git push` does push), so only an unbroken chain of
    # wrappers before `command -v` is trusted as a lookup.
    "sudo -u me command -v git push --force",
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
    # 2000 nested expansions recurse past Python's default limit of 1000, so
    # the parser fails; at 600 the push was simply found, which never tested
    # the failure path. The diagnostic proves which path blocked.
    command = "$(git push origin --force)"
    for _ in range(2000):
        command = "${UNSET:-" + command + "}"
    payload = json.dumps({"tool_name": "Bash", "tool_input": {"command": "echo \"" + command + "\""}})
    result = subprocess.run([sys.executable, "-I", str(HOOK)], input=payload,
                            capture_output=True, text=True)
    assert result.returncode == 2
    assert "too complex to inspect" in result.stderr


def test_parser_overflow_blocks_without_a_literal_push():
    # Bash can spell push without the literal word, so a parser failure must
    # block whether or not the raw text says "push".
    command = "x"
    for _ in range(2000):
        command = "${X:-" + command + "}"
    assert run_hook("X=ok; echo \"" + command + "\"; git pu\"\"sh origin --force main") == 2


def test_oversized_brace_expansion_blocks():
    # Past the expansion limit the words cannot all be inspected, so block.
    command = "git push origin --{force,x}" + "{,}" * 14
    payload = json.dumps({"tool_name": "Bash", "tool_input": {"command": command}})
    result = subprocess.run([sys.executable, "-I", str(HOOK)], input=payload,
                            capture_output=True, text=True)
    assert result.returncode == 2
    assert "too complex to inspect" in result.stderr


def test_unreadable_command_blocks():
    # Text the lexer cannot read is blocked whole; the old fallback split read
    # `$'--force'` as `$--force` and let the push before the bad quote run.
    payload = json.dumps({"tool_name": "Bash", "tool_input": {
        "command": "git push origin $'--force' main\necho \"unterminated"}})
    result = subprocess.run([sys.executable, "-I", str(HOOK)], input=payload,
                            capture_output=True, text=True)
    assert result.returncode == 2
    assert "too complex to inspect" in result.stderr


def test_any_internal_error_blocks():
    # Any exit other than 0 or 2 lets the command run, so an unexpected error
    # inside the parser (here an AttributeError from a non-string command)
    # blocks.
    payload = json.dumps({"tool_name": "Bash", "tool_input": {"command": ["git", "push", "-f"]}})
    result = subprocess.run([sys.executable, "-I", str(HOOK)], input=payload,
                            capture_output=True, text=True)
    assert result.returncode == 2
    assert "too complex to inspect" in result.stderr


def test_ignores_other_tools():
    payload = json.dumps({"tool_name": "Write", "tool_input": {"command": "git push -f"}})
    result = subprocess.run([sys.executable, "-I", str(HOOK)], input=payload,
                            capture_output=True, text=True)
    assert result.returncode == 0
