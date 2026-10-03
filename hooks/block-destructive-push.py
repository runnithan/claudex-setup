#!/usr/bin/env python3
"""PreToolUse[Bash] guard: block destructive git push forms.

The permissions.deny prefix patterns in settings.json catch the common spellings
(`git push --force`, `git push -f`, and the four added beside them), but a prefix
pattern cannot see a flag written after the remote (`git push origin --force`) and
cannot express a refspec shape at all (`+main`, `:old-branch`). This hook closes
both, so the deny list stays as the cheap first tier and this is the durable one.

It also looks through the wrappers a prefix rule never sees: a path-qualified git
(`/usr/bin/git`, `git.exe`), env assignments, `env`/`command`/`time` and their
options (`env -u NAME`, `nice -n 5`), shell keywords, `bash -c '...'`, and
`$(...)`, `<(...)` or backtick substitutions. A Bash rule matches the command
text as written, so it is not a boundary on its own.

The command is read the way a shell reads it: quotes and `${...}` stay inside their
word, a quoted `;` is an argument, `#` starts a comment only at the start of a word,
and a redirect (`2>/dev/null`) does not end the command. So text that merely
mentions a push (a commit message, an echo) is not blocked, and a quoted argument
cannot hide a flag that follows it. Option values (`-o draft`) are not read as
flags, and `--` ends options but not refspecs. Nesting too deep to inspect, and
text the parser cannot read, is blocked rather than passed.

Inline git config is read too: an alias set with `-c alias.x=...` (or through
`GIT_CONFIG_*` assignments anywhere in the same command) is expanded, and
`remote.<name>.mirror` or a forced `remote.<name>.push` counts as destructive.
What it cannot see: aliases and remote settings stored in a git config file or
exported by an earlier, separate command, a value held only in a variable
(`$REF` with no visible default), a script file it is asked to run, refspecs another program feeds
in (xargs reading stdin), and programs that run commands their own way
(`python -c`, `make`).

Deliberately scoped to DESTRUCTIVE forms only. A plain `git push` is untouched: a
hook cannot tell whether the owner approved in the current turn, and blocking
ordinary pushes would make the guard something people switch off. For the same
reason a `--force-with-lease` push to branches it names explicitly, none of them
main or master, is allowed: amending your own feature branch and pushing it is
routine. Without a named branch the lease push stays blocked, since the current
branch may be main.
"""
import json
import re
import shlex
import sys

DESTRUCTIVE = ("--force", "--force-with-lease", "--delete", "--mirror", "--prune")
WRAPPERS = ("env", "command", "time", "nice", "nohup", "sudo", "doas", "exec", "builtin",
            "timeout", "xargs", "stdbuf", "ionice", "setsid", "chrt", "taskset",
            "su", "runuser", "script", "flock")
# A wrapper option whose value is a whole command line (`su -c`, `env -S`),
# alone or ending a short cluster (`su -lc`, `env -vS`). Group 1 or 2 holds an
# attached value; with neither, the value is the next word.
COMMAND_STRING_OPT = re.compile(r"-[A-Za-z]*?[cS](.*)|--(?:command|split-string)(?:=(.*))?", re.S)
KEYWORDS = ("!", "if", "then", "else", "elif", "do", "while", "until", "coproc")
SHELLS = ("bash", "sh", "zsh", "dash")
GIT_OPTS_WITH_VALUE = ("-C", "-c", "--git-dir", "--work-tree", "--namespace", "--config-env")
# git push options whose value is the next word (or, for -o, the rest of a cluster).
# The short option comes first; the rest are long.
PUSH_OPTS_WITH_VALUE = ("-o", "--push-option", "--repo", "--receive-pack", "--exec")
SHELL_LONG_OPTS_WITH_VALUE = ("--rcfile", "--init-file")
# A wrapper followed by one of these only looks a command up or prints help.
LOOKUP_FLAGS = {"command": ("-v", "-V"), "env": ("--help", "--version")}
REDIRECT = re.compile(r"&>>?|<<<|<<-?|<>|>>|>&|<&|>\||[<>]")
SEPARATOR = re.compile(r";;|&&|\|\||\|&|[;&|()]")
MAX_DEPTH = 5


def program(word):
    """The program a command word names: its basename after either slash,
    lowercased and without `.exe`, so `/usr/bin/git`, `git.exe` (Git Bash on
    Windows) and `GIT` (a case-insensitive macOS disk) all name git."""
    name = re.split(r"[/\\]", word)[-1].lower()
    return name[:-4] if name.endswith(".exe") else name


def block(segment):
    sys.stderr.write(
        "Destructive git push blocked: " + segment + "\n"
        "Force, delete, mirror, prune and rewritten-refspec pushes rewrite or destroy "
        "remote history, which no local undo recovers. Report what you wanted to run "
        "and why, and let the owner run it. To update your own feature branch after "
        "an amend, name it with a lease: git push --force-with-lease origin <branch>.\n")
    sys.exit(2)


ODD_BACKSLASH_END = re.compile(r"(?<!\\)(?:\\\\)*\\$")
# Quoted `{`, `}` and `,` travel through the lexer as private-use stand-ins, so
# brace expansion leaves them literal, and are restored before inspection.
QUOTED_BRACES = str.maketrans({"{": "\ue000", "}": "\ue001", ",": "\ue002"})
PLAIN_BRACES = str.maketrans({"\ue000": "{", "\ue001": "}", "\ue002": ","})
# The escapes a backtick body or an unquoted heredoc body loses before it runs.
ONE_ESCAPE_LEVEL = re.compile(r"\\([\\$`])")


def heredoc_bodies(text, i, heredocs):
    """Read the bodies of the heredocs opened on the line that ended just
    before i, in order: (list of (body, delimiter quoted, token index where
    the heredoc's command starts), index after them).
    A body ends at a line that is exactly its delimiter (after leading tabs
    for `<<-`), or at the end of the text. In an unquoted body a line ending
    in an odd run of backslashes continues on the next, so `EO\\` + `F` is
    the delimiter `EOF`."""
    bodies = []
    for strip_tabs, delim, quoted, *start in heredocs:
        if delim is None:
            continue
        lines = []
        while i < len(text):
            j = text.find("\n", i)
            j = len(text) if j < 0 else j
            line, i = text[i:j], j + 1
            while not quoted and i < len(text) and ODD_BACKSLASH_END.search(line):
                j = text.find("\n", i)
                j = len(text) if j < 0 else j
                line, i = line[:-1] + text[i:j], j + 1
            if (line.lstrip("\t") if strip_tabs else line) == delim:
                break
            lines.append(line)
        bodies.append(("\n".join(lines), quoted, start[0] if start else 0))
    return bodies, min(i, len(text))


def backtick_end(text, i):
    while i < len(text):
        if text[i] == "\\":
            i += 2
            continue
        if text[i] == "`":
            return i
        i += 1
    raise ValueError("unterminated backtick")


HEREDOC_WORD = re.compile(r"""<<(-?)[ \t]*((?:'[^']*'|"[^"]*"|\\.|[^\s;&|()<>'"\\])+)""")
QUOTE_PART = re.compile(r"""'([^']*)'|"([^"]*)"|\\(.)""")
COMMAND_KEYWORD = re.compile(r"(?:if|then|else|elif|do|while|until|time|coproc|!|\{)(?=[\s;&|()]|$)")


def paren_end(text, i):
    """Index of the `)` closing a substitution whose body starts at i. A `)`
    that ends a `case` pattern, or sits in a comment or a heredoc body, does
    not close it. `case` and `esac` count only where a command starts, so
    `echo case` is an argument."""
    depth, cases, word_start, cmd_start, heredocs = 1, 0, True, True, []
    while i < len(text):
        c = text[i]
        if word_start and c == "#":
            j = text.find("\n", i)
            i = len(text) if j < 0 else j
            continue
        if text.startswith("<<<", i):
            i += 3
            continue
        m = HEREDOC_WORD.match(text, i)
        if m:
            delim = QUOTE_PART.sub(lambda q: q.group(1) or q.group(2) or q.group(3) or "", m.group(2))
            heredocs.append([m.group(1) == "-", delim, True])
            i = m.end()
            word_start = False
            continue
        if c == "\n" and heredocs:
            i = heredoc_bodies(text, i + 1, heredocs)[1]
            heredocs, word_start = [], True
            continue
        if word_start and c not in " \t\n;&|()<>":
            if cmd_start and re.match(r"(case|esac)(?![\w-])", text[i:]):
                cases += 1 if text.startswith("case", i) else -1 if cases else 0
                i += 4
                word_start = cmd_start = False
                continue
            # A keyword leaves the next word in command position; any other
            # word starts a command's arguments.
            cmd_start = bool(COMMAND_KEYWORD.match(text, i))
        if c in ";&|()\n":
            cmd_start = True
        word_start = c in " \t\n;&|()"
        if c == "\\":
            i += 2
            continue
        if text.startswith("$'", i):
            # An ANSI-C string may hold an escaped quote (`$'it\'s'`).
            i = ansi_c_end(text, i + 2)[0]
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
        # Inside backticks `\\`, `\$` and `` \` `` lose their backslash before
        # the body runs, so `\\--force` reaches git as `--force`.
        subs.append(ONE_ESCAPE_LEVEL.sub(r"\1", text[i + 1:j]))
        return j + 1
    return None


def body_expansions(body, subs):
    """Record the substitutions in an unquoted heredoc body, which bash runs
    while expanding it. Quotes are literal there; only `\\` escapes."""
    i = 0
    while i < len(body):
        if body[i] == "\\":
            i += 2
            continue
        if body[i] in "$`":
            j = substitution(body, i, subs)
            if j is not None:
                i = j
                continue
        i += 1


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


ANSI_C_ESCAPE = re.compile(
    r"x([0-9A-Fa-f]{1,2})|u([0-9A-Fa-f]{1,4})|U([0-9A-Fa-f]{1,8})|([0-7]{1,3})|c(.)|(.)", re.S)
ANSI_C_CHAR = {"a": "\a", "b": "\b", "e": "\x1b", "E": "\x1b", "f": "\f", "n": "\n",
               "r": "\r", "t": "\t", "v": "\v", "\\": "\\", "'": "'", '"': '"', "?": "?"}


def ansi_c_end(text, i):
    """Decode a `$'...'` string whose body starts at i, as bash does, so an
    escape such as `\\x6f` cannot disguise a flag. Returns (index after, value).
    Bash cuts the decoded string at its first NUL (`\\0`, `\\c@`)."""
    out = []
    while i < len(text):
        c = text[i]
        if c == "'":
            return i + 1, "".join(out).split("\0", 1)[0]
        if c != "\\":
            out.append(c)
            i += 1
            continue
        m = ANSI_C_ESCAPE.match(text, i + 1)
        if m is None:
            break
        hex_digits = m.group(1) or m.group(2) or m.group(3)
        if hex_digits:
            out.append(chr(int(hex_digits, 16)))
        elif m.group(4):
            out.append(chr(int(m.group(4), 8) & 0xFF))
        elif m.group(5):
            out.append(chr(ord(m.group(5)) & 0x1F))
        else:
            out.append(ANSI_C_CHAR.get(m.group(6), "\\" + m.group(6)))
        i = m.end()
    raise ValueError("unterminated quote")


def lex(text):
    """Split shell text into (kind, value, quoted) tokens, kind being "word",
    "sep" (ends a simple command) or "redir" (its next word is a redirect
    target), plus the commands found inside substitutions.

    A heredoc body is data (a commit message, a file being written), so it is
    not tokenized. A body a shell could read (`bash <<EOF`, `cat <<EOF | sh`,
    any shell named in the heredoc's command or later on its line) runs, so it is returned as a
    command to check, and so are the substitutions in an unquoted body. A
    here-string (`bash <<< '...'`) is treated the same way."""
    tokens, subs, word = [], [], []
    state = {"in_word": False, "quoted": False}
    # A shell can read a heredoc or here-string only from that redirect's own
    # command or a later one on the line (`cat <<EOF | sh`, `> s.sh && bash
    # s.sh`), never from a command that ran before it, so each remembers the
    # token index where its command starts.
    cmd_start = 0
    heredocs = []  # [strip_tabs, delimiter, quoted, cmd_start]
    herestrings = []  # (word after `<<<`, cmd_start) on the current line

    def end_word():
        if state["in_word"]:
            value = "".join(word)
            tokens.append(("word", value, state["quoted"]))
            if heredocs and heredocs[-1][1] is None:
                heredocs[-1][1:3] = [value.translate(PLAIN_BRACES), state["quoted"]]
            start = state.pop("herestring", None)
            if start is not None:
                herestrings.append((value.translate(PLAIN_BRACES), start))
        word.clear()
        state.update(in_word=False, quoted=False)

    i = 0
    while i < len(text):
        c = text[i]
        if c == "\\":
            if text.startswith("\\\n", i):
                i += 2
                continue
            # An escaped character is quoted: `\{` is an argument, not a group.
            # Quoted braces and commas are kept as stand-ins (QUOTED_BRACES) so
            # brace expansion, which only sees unquoted ones, skips them.
            word.append(text[i + 1:i + 2].translate(QUOTED_BRACES))
            state.update(in_word=True, quoted=True)
            i += 2
            continue
        if c == "'":
            j = text.find("'", i + 1)
            if j < 0:
                raise ValueError("unterminated quote")
            word.append(text[i + 1:j].translate(QUOTED_BRACES))
            state.update(in_word=True, quoted=True)
            i = j + 1
            continue
        if c == '"':
            j = double_end(text, i + 1, subs)
            # Inside double quotes a backslash escapes only $ ` " \ and newline.
            word.append(re.sub(r'\\([$`"\\\n])', lambda m: "" if m.group(1) == "\n" else m.group(1),
                               text[i + 1:j - 1]).translate(QUOTED_BRACES))
            state.update(in_word=True, quoted=True)
            i = j
            continue
        if text.startswith("$'", i):
            i, value = ansi_c_end(text, i + 2)
            word.append(value.translate(QUOTED_BRACES))
            state.update(in_word=True, quoted=True)
            continue
        if text.startswith('$"', i):
            # A locale-translated string: the `"` that follows is an ordinary quote.
            i += 1
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
            bodies, i = heredoc_bodies(text, i + 1, heredocs)
            for body, quoted, start in bodies:
                if names_shell(tokens[start:]):
                    # The shell reads an unquoted body after the outer shell
                    # has stripped one escape level (`\\--force` -> `\--force`).
                    script = body if quoted else ONE_ESCAPE_LEVEL.sub(r"\1", body)
                    subs.append(stdin_script(script, tokens[start:]))
                elif not quoted:
                    body_expansions(body, subs)
            subs += [stdin_script(h, tokens[s:]) for h, s in herestrings if names_shell(tokens[s:])]
            heredocs.clear()
            herestrings.clear()
            cmd_start = len(tokens)
            continue
        if c in "<>" or text.startswith("&>", i):
            if state["in_word"] and not state["quoted"] and "".join(word).isdigit():
                word.clear()
                state["in_word"] = False
            end_word()
            m = REDIRECT.match(text, i)
            tokens.append(("redir", m.group(), False))
            if m.group() in ("<<", "<<-"):
                heredocs.append([m.group() == "<<-", None, False, cmd_start])
            state["herestring"] = cmd_start if m.group() == "<<<" else None
            i = m.end()
            continue
        if c in ";&|()":
            end_word()
            m = SEPARATOR.match(text, i)
            tokens.append(("sep", m.group(), False))
            cmd_start = len(tokens)
            i = m.end()
            continue
        word.append(c)
        state["in_word"] = True
        i += 1
    end_word()
    subs += [stdin_script(h, tokens[s:]) for h, s in herestrings if names_shell(tokens[s:])]
    return tokens, subs


def names_shell(tokens):
    """Whether any word among these tokens names a shell, which could then
    read a heredoc or here-string on the same line as its script."""
    return any(kind == "word" and program(value) in SHELLS for kind, value, _ in tokens)


def stdin_script(script, line):
    """A script a shell on this line reads from stdin, as the equivalent
    `bash -c` command carrying that shell's own arguments, so the
    forwarded-argument check covers `bash -s -- --force <<EOF` too."""
    args, started, skip = [], False, False
    for kind, value, _ in line:
        if not started:
            started = kind == "word" and program(value) in SHELLS
        elif kind == "sep":
            break
        elif kind == "redir":
            skip = True
        elif skip:
            skip = False
        elif value not in ("-s", "-", "--"):
            args.append(value.translate(PLAIN_BRACES))
    return "bash -c " + " ".join(shlex.quote(a) for a in [script, "_"] + args)


def segments(tokens):
    """Word lists for each simple command. Redirect targets are dropped, and
    unquoted `{`/`}` group words end a command like an operator does. Bash
    only reads a brace as a group word at the start of a command, so a
    command holding one is also returned whole, braces kept as words: in
    `git -C { push --force` the brace is the value of -C."""
    out, current, whole, braced, skip_next = [], [], [], False, False
    for kind, value, quoted in tokens:
        if kind == "redir":
            skip_next = True
            continue
        if kind == "sep":
            out += [current] if current else []
            out += [whole] if braced else []
            current, whole, braced, skip_next = [], [], False, False
            continue
        if skip_next:
            skip_next = False
            continue
        whole.append(value)
        if value in ("{", "}") and not quoted:
            out += [current] if current else []
            current, braced = [], True
        else:
            current.append(value)
    out += [current] if current else []
    out += [whole] if braced else []
    return out


def shell_script(tokens, k):
    """The `-c` string of a shell invocation whose options start at k, and the
    positional arguments after it, or (None, []). As in bash, `-c` only says
    the first non-option word is the script, so options may follow it
    (`bash -c -e 'cmd'`), and each `o`/`O` in a cluster takes a value."""
    has_c = False
    while k < len(tokens) and tokens[k][:1] in "-+":
        t = tokens[k]
        if t in ("-", "--"):
            k += 1
            break
        if t.startswith("--"):
            k += 2 if t in SHELL_LONG_OPTS_WITH_VALUE else 1
            continue
        has_c = has_c or (t[0] == "-" and "c" in t)
        k += 1 + t.count("o") + t.count("O")
    if has_c and k < len(tokens):
        return tokens[k], tokens[k + 1:]
    return None, []


def inspect(words, depth):
    """Block if this simple command is a destructive git push, or hands one
    to a shell."""
    i, first = 0, None
    while i < len(words):
        t = words[i]
        if program(t) in WRAPPERS:
            first = i if first is None else first
        elif not (re.match(r"^[A-Za-z_]\w*=", t) or t in KEYWORDS or (t.startswith("-") and i)):
            break
        i += 1
    if first is None:
        if i < len(words):
            inspect_program(words, i, depth)
        return
    # A wrapper option can take a value (`env -u NAME`, `nice -n 5`,
    # `sudo -u user`) that the loop above would take for the program, and
    # each wrapper spells its options differently. So after a wrapper, fail
    # closed: every later word that names git or a shell starts a command,
    # and a command string given to -c or -S (`su -c '...'`, `env -S '...'`)
    # is checked as a script.
    for k in range(first + 1, len(words)):
        w = words[k]
        # `command -v` only looks a program up, but only an unbroken chain of
        # wrappers proves `command` is the program: after `env -u` it is the
        # name of a variable to unset, and the push after it runs.
        if (w in LOOKUP_FLAGS.get(program(words[k - 1]), ())
                and all(program(x) in WRAPPERS for x in words[first:k])):
            return
        inspect_program(words, k, depth)
        m = COMMAND_STRING_OPT.fullmatch(w)
        if m:
            attached = m.group(1) or m.group(2)
            value, rest = (attached, k + 1) if attached else (" ".join(words[k + 1:k + 2]), k + 2)
            # env -S appends the words after its string to the command it
            # builds, so check them together; for other options the extra
            # words are only arguments to check alongside. GNU env also reads
            # `\_` as an argument separator, which a shell would not.
            value = value.replace("\\_", " ")
            try:
                check(" ".join([value] + [shlex.quote(r) for r in words[rest:]]), depth + 1)
            except ValueError:
                # The scan cannot tell whose -c this is: under `command grep
                # -c PATTERN` it is grep's count flag and the value is data.
                # Text that is not valid shell is not a script a wrapper runs.
                pass


def inspect_program(words, k, depth):
    """Block if the command whose program is words[k] is a destructive push."""
    inspect_as(program(words[k]), words, k, depth)
    if not expanded(words[k]):
        return
    # A program built from an expansion (`$GIT`, `${RUNNER:-bash}`) cannot be
    # resolved here, so beyond its literal name (`"$(git --exec-path)/git-push"`
    # is still git-push), fail closed: try its visible default, read it as git,
    # and read it as an unknown launcher whose later words may run a command.
    default = with_default(words[k])
    if default != words[k]:
        inspect([default] + words[k + 1:], depth)
    inspect_as("git", words, k, depth)
    inspect(["nohup"] + words[k + 1:], depth)


def inspect_as(prog, words, k, depth):
    """Block if words[k], run as the program `prog`, pushes destructively."""
    if prog in SHELLS:
        script, positional = shell_script(words, k + 1)
        if script:
            check(script, depth + 1)
            # Arguments after the script reach it as $0, $1.., $@ and $*. Where
            # they land is shell semantics, so fail closed: a pushing script
            # that reads them, handed destructive-looking ones, is blocked.
            # Each is judged alone, since the script may forward only one, so
            # an unused `-o` or `--` must not hide the next. The script may
            # spell push with quotes (`pu""sh`) or take it as an argument.
            # `${!#}` and `${!N}` reach the arguments indirectly.
            if (positional and re.search(r"\$\{?!?[@*0-9#]", script)
                    and (re.search(r"\bpush\b", re.sub(r"[\"'\\]", "", script))
                         or any(p == "push" or program(p) == "git-push" for p in positional))
                    and any(destructive([p]) for p in positional)):
                block(" ".join(words))
    elif prog == "git-push":
        # git's exec-path holds git-push, a link to git that runs the push
        # builtin when invoked under that name.
        args = words[k + 1:]
        if destructive(args) or destructive([with_default(a) for a in args]):
            block(" ".join(words))
    elif prog == "eval":
        # eval joins its arguments with spaces and runs the result.
        check(" ".join(words[k + 1:]), depth + 1)
    elif prog == "git":
        j, config = k + 1, env_config(SEEN_GIT_ENV + words[:k])
        while j < len(words) and words[j].startswith("-"):
            if words[j] in ("-c", "--config-env") and j + 1 < len(words):
                config.append((words[j] == "--config-env", words[j + 1]))
            elif words[j].startswith("--config-env="):
                config.append((True, words[j].split("=", 1)[1]))
            j += 2 if words[j] in GIT_OPTS_WITH_VALUE else 1
        if j < len(words):
            inspect_git(words, k, j, config, depth)


# Every GIT_CONFIG_* assignment seen anywhere in the command being checked. A
# child shell inherits one and `export` keeps it for the commands after, so
# each git command checked later sees them all: wider than bash's scoping,
# which only errs toward blocking.
SEEN_GIT_ENV = []


def env_config(words):
    """Config set through the environment by assignments in this command
    (`GIT_CONFIG_KEY_n`/`GIT_CONFIG_VALUE_n` pairs, `GIT_CONFIG_PARAMETERS`),
    as -c style (hidden, "key=value") items. They come before the -c items,
    since a -c value overrides them."""
    env = dict(w.split("=", 1) for w in words if re.match(r"[A-Za-z_]\w*=", w))
    items = []
    # Git reads the pairs by index, 0 first, whatever order they were set in.
    indexes = sorted((int(m.group(1)), m.group(1)) for m in
                     (re.fullmatch(r"GIT_CONFIG_KEY_(\d+)", name) for name in env) if m)
    for _, n in indexes:
        items.append((False, env["GIT_CONFIG_KEY_" + n] + "=" + env.get("GIT_CONFIG_VALUE_" + n, "")))
    for m in re.finditer(r"'([^']*)'(?:='([^']*)')?", env.get("GIT_CONFIG_PARAMETERS", "")):
        items.append((False, m.group(1) if m.group(2) is None else m.group(1) + "=" + m.group(2)))
    return items


def expanded(word):
    """Whether a word holds a parameter or command expansion, so its value is
    only known when bash runs it."""
    return "$" in word or "`" in word


# `${name:-word}` and its kin (`-`, `=`, `+`, `?`, with or without `:`).
PARAM_OPERAND = re.compile(r"\$\{[^{}:=+?-]*:?[-=+?]([^{}]*)\}")


def with_default(word):
    """The word with each `${name:-word}`-style expansion replaced by its
    operand: the value bash gives it when the variable is unset (or, for
    `:+`, set). A hook cannot know which happens, so both are checked."""
    return PARAM_OPERAND.sub(lambda m: m.group(1), word)


def inspect_git(words, k, j, config, depth):
    """Block if git (words[k]) running subcommand words[j] pushes
    destructively. `config` holds the (value hidden in an env var, "key=value")
    pairs set with -c or --config-env, since they can define an alias for the
    subcommand or make a plain push mirror or force."""
    sub, rest = words[j], words[j + 1:]
    # A subcommand built from an expansion (`git $p`) may be push.
    pushing = sub == "push" or expanded(sub)
    # Git ignores an alias named after a built-in command, so `push` is
    # always the real push, whatever alias.push says. A repeated key takes
    # its last value, so search from the end.
    for hidden, item in reversed(config) if not pushing else ():
        key, has_value, value = item.partition("=")
        if key.lower() != "alias." + sub.lower():
            continue
        if hidden or depth > MAX_DEPTH:
            block(" ".join(words))
        if value.startswith("!"):
            # Git runs a shell alias as `sh -c '<alias> "$@"' <alias> <args>`,
            # so check it in that shape: the forwarded-argument check then
            # sees arguments that reach a push through "$@" in a function.
            check("sh -c " + " ".join(shlex.quote(a) for a in [value[1:] + ' "$@"', "_"] + rest),
                  depth + 1)
        else:
            # Keep the words before git too, so config set by assignments
            # there still applies to an alias the expansion chains to.
            inspect_program(words[:j] + shlex.split(value) + rest, k, depth + 1)
        return
    if not pushing:
        return
    mirrors = {}
    for hidden, item in config:
        key, has_value, value = item.partition("=")
        m = re.fullmatch(r"remote\.(.+)\.(mirror|push)", key, re.I)
        if not m:
            continue
        if m.group(2).lower() == "mirror":
            # One value per remote, and the last one set wins.
            mirrors[m.group(1)] = (hidden or not has_value
                                   or value.lower() not in ("false", "no", "off", "0", ""))
        elif hidden or destructive(["--", value]):
            # Push refspecs accumulate, so any forced one counts.
            block(" ".join(words))
    if any(mirrors.values()) or destructive(rest) or destructive([with_default(a) for a in rest]):
        block(" ".join(words))


def destructive(after):
    options, skip, lease, pushes_all, positional = True, False, [], False, []
    for a in after:
        if skip:
            skip = False
            continue
        if options and a == "--":
            options = False
            continue
        if options and a.startswith("--"):
            # Git takes any unique prefix of a long option (`--del`), so match
            # prefixes. One shared with a safe option is ambiguous and git
            # refuses it, so blocking every prefix of a destructive option
            # never blocks a push git would run safely.
            name, _, value = a.partition("=")
            matches = [o for o in DESTRUCTIVE if o.startswith(name)]
            if matches == ["--force-with-lease"]:
                # Judged once every refspec is known (lease_to_feature_branches).
                lease.append(value.split(":", 1)[0])
                continue
            if matches:
                return True
            pushes_all = pushes_all or any(o.startswith(name) for o in ("--all", "--branches"))
            skip = "=" not in a and any(o.startswith(name) for o in PUSH_OPTS_WITH_VALUE[1:])
            continue
        if options and a.startswith("-"):
            if a in PUSH_OPTS_WITH_VALUE:
                skip = True
            else:
                # Read flag by flag: `-foci.skip` is -f, then -o with the value
                # `ci.skip`, so characters after the flags must not hide them.
                for n, ch in enumerate(a[1:], 1):
                    if ch in "fd":
                        return True
                    if ch == "o":
                        # -o takes a value: the rest of the cluster, or the next word.
                        skip = n == len(a) - 1
                        break
            continue
        # `+src:dst` forces and `:dst` deletes; a bare `:` pushes matching branches.
        if a.startswith("+") or (a.startswith(":") and a != ":"):
            return True
        positional.append(a)
    return bool(lease) and not lease_to_feature_branches(positional, lease, pushes_all)


PROTECTED_BRANCHES = ("main", "master")


def lease_to_feature_branches(positional, lease, pushes_all):
    """Whether a --force-with-lease push only rewrites branches it names, none
    of them main or master. Amending your own branch and pushing it with a
    lease is routine, but anything less certain stays blocked: no refspec
    (the current branch, which may be main), `HEAD`/`@`, a pattern, a name
    held in a variable, or --all."""
    if pushes_all or len(positional) < 2:
        return False
    names = [p.rsplit(":", 1)[-1] for p in positional[1:]] + [n for n in lease if n]
    for n in names:
        n = n[len("refs/heads/"):] if n.startswith("refs/heads/") else n
        if not n or n in PROTECTED_BRANCHES or n in ("HEAD", "@") or expanded(n) or any(
                c in n for c in "*?["):
            return False
    return True


BRACE_SEQUENCE = re.compile(
    r"(-?\d+)\.\.(-?\d+)(?:\.\.(-?\d+))?|([A-Za-z])\.\.([A-Za-z])(?:\.\.(-?\d+))?")
MAX_EXPANSIONS = 10000


def brace_sequence(body):
    """The words of a `{a..b}` or `{a..b..step}` sequence, or None."""
    m = BRACE_SEQUENCE.fullmatch(body)
    if not m:
        return None
    numeric = m.group(1) is not None
    a, b = (int(m.group(1)), int(m.group(2))) if numeric else (ord(m.group(4)), ord(m.group(5)))
    step = abs(int((m.group(3) if numeric else m.group(6)) or 1)) or 1
    values = range(a, b + 1, step) if a <= b else range(a, b - 1, -step)
    if len(values) > MAX_EXPANSIONS:
        return None
    return [str(n) if numeric else chr(n) for n in values]


def brace_expand(word):
    """The words bash's brace expansion makes of one word: `--{force,x}` is
    `--force --x` and `-{d..f}` is `-d -e -f`. `${...}` is a parameter
    expansion, not a list, and a single item (`{x}`) stays literal. Empty
    results are dropped, as bash drops them. A sequence longer than the limit
    (`{1..100000}`) stays literal, since numbers alone push nothing, but any
    other expansion past the limit raises, so the command is blocked rather
    than passed half-read."""
    i = 0
    while True:
        i = word.find("{", i)
        if i < 0:
            return [word]
        if i and word[i - 1] == "$":
            try:
                i = brace_end(word, i + 1) + 1
            except ValueError:
                return [word]
            continue
        depth, commas, j = 0, [], i
        while j < len(word):
            if word[j] == "{":
                depth += 1
            elif word[j] == "}":
                depth -= 1
                if depth == 0:
                    break
            elif word[j] == "," and depth == 1:
                commas.append(j)
            j += 1
        else:
            return [word]
        if commas:
            cuts = [i] + commas + [j]
            parts = [word[a + 1:b] for a, b in zip(cuts, cuts[1:])]
        else:
            parts = brace_sequence(word[i + 1:j])
            if parts is None:
                i += 1
                continue
        out = []
        for part in parts:
            out += brace_expand(word[:i] + part + word[j + 1:])
            if len(out) > MAX_EXPANSIONS:
                raise ValueError("brace expansion too large to inspect")
        return [w for w in out if w]


def check(command, depth=0):
    if depth > MAX_DEPTH:
        block("(command nested too deeply to inspect)")
    # Text the lexer cannot read raises here and is blocked whole by main():
    # bash runs every line before a syntax error, and a cruder split misreads
    # quoting (`$'--force'` as `$--force`).
    tokens, subs = lex(command)
    parts = segments(tokens)
    # Collect GIT_CONFIG_* assignments before any nested script is checked:
    # a child shell or heredoc script inherits them.
    SEEN_GIT_ENV.extend(value.translate(PLAIN_BRACES) for kind, value, _ in tokens
                        if kind == "word" and value.startswith("GIT_CONFIG_") and "=" in value)
    for inner in subs:
        check(inner, depth + 1)
    for words in parts:
        inspect([e.translate(PLAIN_BRACES) for w in words for e in brace_expand(w)], depth)


def main():
    try:
        data = json.loads(sys.stdin.buffer.read().decode("utf-8"))
    except (json.JSONDecodeError, ValueError, UnicodeDecodeError):
        sys.exit(0)
    if data.get("tool_name", "") != "Bash":
        sys.exit(0)
    command = data.get("tool_input", {}).get("command", "")
    try:
        check(command)
    except Exception:
        # An exit other than 0 or 2 lets the command run, so any failure here,
        # a parser limit or a bug, must block rather than crash. It cannot
        # first ask whether the text mentions a push: bash can spell one
        # without the word (`pu""sh`).
        block("(command too complex to inspect)")
    sys.exit(0)


if __name__ == "__main__":
    main()
