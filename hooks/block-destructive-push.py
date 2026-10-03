#!/usr/bin/env python3
"""PreToolUse[Bash] guard: block destructive git push forms.

The permissions.deny prefix patterns in settings.json catch the common spellings
(`git push --force`, `git push -f`, and the four added beside them), but a prefix
pattern cannot see a flag written after the remote (`git push origin --force`) and
cannot express a refspec shape at all (`+main`, `:old-branch`). This hook closes
both, so the deny list stays as the cheap first tier and this is the durable one.

It also looks through the wrappers a prefix rule never sees: a path-qualified git
(`/usr/bin/git`), env assignments, `env`/`command`/`time`, shell keywords,
`bash -c '...'`, and `$(...)`, `<(...)` or backtick substitutions. A Bash rule
matches the command text as written, so it is not a boundary on its own.

The command is read the way a shell reads it: quotes and `${...}` stay inside their
word, a quoted `;` is an argument, `#` starts a comment only at the start of a word,
and a redirect (`2>/dev/null`) does not end the command. So text that merely
mentions a push (a commit message, an echo) is not blocked, and a quoted argument
cannot hide a flag that follows it. Option values (`-o draft`) are not read as
flags, and `--` ends options but not refspecs. Nesting too deep to inspect is
blocked rather than passed.

Deliberately scoped to DESTRUCTIVE forms only. A plain `git push` is untouched: a
hook cannot tell whether the owner approved in the current turn, and blocking
ordinary pushes would make the guard something people switch off.
"""
import json
import os
import re
import shlex
import sys

DESTRUCTIVE = ("--force", "--force-with-lease", "--delete", "--mirror", "--prune")
WRAPPERS = ("env", "command", "time", "nice", "nohup", "sudo", "exec", "builtin")
KEYWORDS = ("!", "if", "then", "else", "elif", "do", "while", "until")
SHELLS = ("bash", "sh", "zsh", "dash")
GIT_OPTS_WITH_VALUE = ("-C", "-c", "--git-dir", "--work-tree", "--namespace", "--config-env")
# git push options whose value is the next word (or, for -o, the rest of a cluster).
PUSH_OPTS_WITH_VALUE = ("-o", "--push-option", "--repo", "--receive-pack", "--exec")
SHELL_OPTS_WITH_VALUE = ("-o", "-O", "+o", "+O")
# A wrapper followed by one of these only looks a command up or prints help.
LOOKUP_FLAGS = {"command": ("-v", "-V"), "env": ("--help", "--version")}
REDIRECT = re.compile(r"&>>?|<<<|<<-?|<>|>>|>&|<&|>\||[<>]")
SEPARATOR = re.compile(r";;|&&|\|\||\|&|[;&|()]")
MAX_DEPTH = 5


def block(segment):
    sys.stderr.write(
        "Destructive git push blocked: " + segment + "\n"
        "Force, delete, mirror, prune and rewritten-refspec pushes rewrite or destroy "
        "remote history, which no local undo recovers. Report what you wanted to run "
        "and why, and let the owner run it.\n")
    sys.exit(2)


HEREDOC = re.compile(r"(?<!<)<<(?!<)-?\s*(['\"]?)([A-Za-z_][\w.-]*)\1")
RUNS_SHELL = re.compile(r"(^|[|;&(\s])(bash|sh|zsh|dash)(\s|$)")


def strip_heredocs(command):
    """Drop heredoc bodies, which are data (a commit message, a file being
    written), so a line in them that merely mentions a push is not blocked.
    A body fed to a shell (`bash <<EOF`, `cat <<EOF | sh`) runs, so it is kept."""
    out, pending = [], []
    for line in command.split("\n"):
        if pending:
            delim, keep = pending[0]
            if line.strip() == delim:
                pending.pop(0)
            elif keep:
                out.append(line)
            continue
        out.append(line)
        keep = bool(RUNS_SHELL.search(line))
        pending += [(m.group(2), keep) for m in HEREDOC.finditer(line)]
    return "\n".join(out)


def backtick_end(text, i):
    while i < len(text):
        if text[i] == "\\":
            i += 2
            continue
        if text[i] == "`":
            return i
        i += 1
    raise ValueError("unterminated backtick")


def paren_end(text, i):
    """Index of the `)` closing a substitution whose body starts at i. A `)`
    that ends a `case` pattern, or sits in a comment, does not close it."""
    depth, cases, word_start = 1, 0, True
    while i < len(text):
        c = text[i]
        if word_start and c == "#":
            j = text.find("\n", i)
            i = len(text) if j < 0 else j
            continue
        if word_start and re.match(r"(case|esac)(?![\w-])", text[i:]):
            cases += 1 if text.startswith("case", i) else -1 if cases else 0
            i += 4
            word_start = False
            continue
        word_start = c in " \t\n;&|()"
        if c == "\\":
            i += 2
            continue
        if c == "'":
            j = text.find("'", i + 1)
            if j < 0:
                raise ValueError("unterminated quote")
            i = j + 1
            continue
        if c == '"':
            i = double_end(text, i + 1, [])
            continue
        if c == "`":
            i = backtick_end(text, i + 1) + 1
            continue
        if c == "(":
            depth += 1
        elif c == ")" and not (cases and depth == 1):
            depth -= 1
            if depth == 0:
                return i
        i += 1
    raise ValueError("unterminated substitution")


def brace_end(text, i):
    depth = 1
    while i < len(text):
        c = text[i]
        if c == "\\":
            i += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    raise ValueError("unterminated expansion")


def substitution(text, i, subs):
    """If a substitution or expansion starts at i, record any command it runs and
    return the index after it; else return None."""
    if text.startswith(("$(", "<(", ">("), i):
        j = paren_end(text, i + 2)
        subs.append(text[i + 2:j])
        return j + 1
    if text.startswith("${", i):
        j = brace_end(text, i + 2)
        # Whether quotes inside an expansion protect a substitution depends on
        # the surrounding quotes and the operator, so fail closed: every
        # substitution in the body counts, quoted or not.
        body, k = text[i + 2:j], 0
        while k < len(body):
            if body.startswith(("$(", "${", "<(", ">("), k) or body[k] == "`":
                k = substitution(body, k, subs)
            else:
                k += 1
        return j + 1
    if text[i] == "`":
        j = backtick_end(text, i + 1)
        subs.append(text[i + 1:j])
        return j + 1
    return None


def double_end(text, i, subs):
    """Index after the `"` closing a double-quoted string whose body starts at i."""
    while i < len(text):
        c = text[i]
        if c == "\\":
            i += 2
            continue
        if c == '"':
            return i + 1
        if c in "$`":
            j = substitution(text, i, subs)
            if j is not None:
                i = j
                continue
        i += 1
    raise ValueError("unterminated quote")


def lex(text):
    """Split shell text into (kind, value, quoted) tokens, kind being "word",
    "sep" (ends a simple command) or "redir" (its next word is a redirect
    target), plus the commands found inside substitutions."""
    tokens, subs, word = [], [], []
    state = {"in_word": False, "quoted": False}

    def end_word():
        if state["in_word"]:
            tokens.append(("word", "".join(word), state["quoted"]))
        word.clear()
        state.update(in_word=False, quoted=False)

    i = 0
    while i < len(text):
        c = text[i]
        if c == "\\":
            if text.startswith("\\\n", i):
                i += 2
                continue
            word.append(text[i + 1:i + 2])
            state["in_word"] = True
            i += 2
            continue
        if c == "'":
            j = text.find("'", i + 1)
            if j < 0:
                raise ValueError("unterminated quote")
            word.append(text[i + 1:j])
            state.update(in_word=True, quoted=True)
            i = j + 1
            continue
        if c == '"':
            j = double_end(text, i + 1, subs)
            # Inside double quotes a backslash escapes only $ ` " \ and newline.
            word.append(re.sub(r'\\([$`"\\\n])', lambda m: "" if m.group(1) == "\n" else m.group(1),
                               text[i + 1:j - 1]))
            state.update(in_word=True, quoted=True)
            i = j
            continue
        if c in "$`" or (c in "<>" and text.startswith("(", i + 1)):
            j = substitution(text, i, subs)
            if j is not None:
                word.append(text[i:j])
                state["in_word"] = True
                i = j
                continue
        if c == "#" and not state["in_word"]:
            j = text.find("\n", i)
            i = len(text) if j < 0 else j
            continue
        if c in " \t\r":
            end_word()
            i += 1
            continue
        if c == "\n":
            end_word()
            tokens.append(("sep", "\n", False))
            i += 1
            continue
        if c in "<>" or text.startswith("&>", i):
            if state["in_word"] and not state["quoted"] and "".join(word).isdigit():
                word.clear()
                state["in_word"] = False
            end_word()
            m = REDIRECT.match(text, i)
            tokens.append(("redir", m.group(), False))
            i = m.end()
            continue
        if c in ";&|()":
            end_word()
            m = SEPARATOR.match(text, i)
            tokens.append(("sep", m.group(), False))
            i = m.end()
            continue
        word.append(c)
        state["in_word"] = True
        i += 1
    end_word()
    return tokens, subs


def segments(tokens):
    """Word lists for each simple command. Redirect targets are dropped, and
    unquoted `{`/`}` group words end a command like an operator does."""
    out, current, skip_next = [], [], False
    for kind, value, quoted in tokens:
        if kind == "redir":
            skip_next = True
        elif kind == "sep" or (value in ("{", "}") and not quoted):
            if current:
                out.append(current)
            current, skip_next = [], False
        elif skip_next:
            skip_next = False
        else:
            current.append(value)
    if current:
        out.append(current)
    return out


def shell_script(tokens, k):
    """The `-c` string of a shell invocation whose options start at k, and the
    positional arguments after it, or (None, [])."""
    while k < len(tokens) and tokens[k][:1] in "-+":
        if re.fullmatch(r"-[A-Za-z]*c[A-Za-z]*", tokens[k]):
            if k + 1 < len(tokens):
                return tokens[k + 1], tokens[k + 2:]
            return None, []
        k += 2 if tokens[k] in SHELL_OPTS_WITH_VALUE else 1
    return None, []


def push_args(tokens, depth):
    """Arguments after `push` when the segment is a git push, else None."""
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if i and t in LOOKUP_FLAGS.get(os.path.basename(tokens[i - 1]), ()):
            return None
        if (re.match(r"^[A-Za-z_]\w*=", t) or os.path.basename(t) in WRAPPERS
                or t in KEYWORDS or (t.startswith("-") and i)):
            i += 1
            continue
        break
    if i >= len(tokens):
        return None
    prog = os.path.basename(tokens[i])
    if prog in SHELLS:
        script, positional = shell_script(tokens, i + 1)
        if script:
            check(script, depth + 1)
            # Arguments after the script reach it as $0, $1.., $@ and $*. Where
            # they land is shell semantics, so fail closed: a pushing script
            # that reads them, handed destructive-looking ones, is blocked.
            if (positional and re.search(r"\$\{?[@*0-9]", script)
                    and re.search(r"\bpush\b", script) and destructive(positional)):
                block(" ".join(tokens))
        return None
    if prog != "git":
        return None
    j = i + 1
    while j < len(tokens) and tokens[j].startswith("-"):
        j += 2 if tokens[j] in GIT_OPTS_WITH_VALUE else 1
    if j < len(tokens) and tokens[j] == "push":
        return tokens[j + 1:]
    return None


def destructive(after):
    options, skip = True, False
    for a in after:
        if skip:
            skip = False
            continue
        if options and a == "--":
            options = False
            continue
        if options and a.startswith("-"):
            if a in PUSH_OPTS_WITH_VALUE:
                skip = True
            elif a in DESTRUCTIVE or a.startswith(("--force-with-lease=", "--delete=")):
                return True
            elif re.fullmatch(r"-[A-Za-z0-9]+", a):
                for n, ch in enumerate(a[1:], 1):
                    if ch in "fd":
                        return True
                    if ch == "o":
                        # -o takes a value: the rest of the cluster, or the next word.
                        skip = n == len(a) - 1
                        break
            continue
        if a.startswith(("+", ":")):
            return True
    return False


def fallback_segments(command):
    """For text the lexer cannot read (unbalanced quotes): a cruder split that
    errs toward blocking, since the shell would reject it anyway."""
    out = []
    for part in re.split(r"[;&|(){}]{1,2}|\n", command):
        try:
            out.append(shlex.split(part))
        except ValueError:
            out.append([t.strip("'\"") for t in part.split()])
    return out


def check(command, depth=0):
    if depth > MAX_DEPTH:
        block("(command nested too deeply to inspect)")
    try:
        tokens, subs = lex(command)
        parts = segments(tokens)
    except ValueError:
        subs, parts = [], fallback_segments(command)
    for inner in subs:
        check(inner, depth + 1)
    for words in parts:
        after = push_args(words, depth)
        if after is not None and destructive(after):
            block(" ".join(words))


def main():
    try:
        data = json.loads(sys.stdin.buffer.read().decode("utf-8"))
    except (json.JSONDecodeError, ValueError, UnicodeDecodeError):
        sys.exit(0)
    if data.get("tool_name", "") != "Bash":
        sys.exit(0)
    command = data.get("tool_input", {}).get("command", "")
    try:
        check(strip_heredocs(command))
    except (RecursionError, ValueError, IndexError):
        # An exit other than 0 or 2 lets the command run, so a parser failure on
        # anything that mentions a push must block rather than crash.
        if re.search(r"\bpush\b", command):
            block("(command too complex to inspect)")
    sys.exit(0)


if __name__ == "__main__":
    main()
