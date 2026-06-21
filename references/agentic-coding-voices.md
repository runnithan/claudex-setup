# Agentic coding voices

People whose recent public posts are worth mining for **agentic-coding lessons** — Claude Code
primarily, but many of these creators also cover **OpenAI Codex**, Cursor, and other agents,
and those lessons often transfer. Read by `/extract-social-lessons`. **Maintain this list** —
handles/affiliations change (verified 2026-06, sourced; re-check before relying on them).

Format: `- Name — role — @handle (X) / blog`. Lines starting with `#` are ignored.
Tiers reflect **recoverability**: open blogs are read first-hand; X-only voices are
best-effort (X login-walls direct fetches, so they only land when reblogged or
mirrored). Beyond people, the **Canonical / non-person sources** tier below tracks the
primary places Claude Code's own behaviour is documented — scout these every run; they
often carry a lesson before any creator covers it.

## Canonical / non-person sources (scout every run; primary, highest signal)
Not people — the first places a new command / flag / hook / gotcha shows up. Same lesson bar
as the voices: a concrete, actionable thing to do or stop doing, grounded in a real quoted
line with its URL. A bare feature announcement is *not* a lesson — extract the **usage
implication** ("now do X instead of Y"), or drop it.
- Claude Code changelog / release notes — new commands, flags, hooks each release — https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
- Claude Code docs (esp. the "best practices" page) — Anthropic's canonical guidance, continuously updated — https://docs.claude.com/en/docs/claude-code
- `anthropics/claude-code` GitHub issues & discussions — confirmed behaviours, gotchas, team-suggested workarounds (the richest "never do X" source) — https://github.com/anthropics/claude-code/issues
- Hacker News — threads on CC releases surface non-obvious community workflows (queryable via Algolia: https://hn.algolia.com/api/v1/search?query=claude%20code) — https://news.ycombinator.com

## Tier 1 — open publishers (scout every run; these reliably deliver)
- Simon Willison — Datasette/`llm` creator; prolific LLM-tooling blogger — @simonw / https://simonwillison.net
- Geoffrey Huntley — author of the "Ralph" autonomous-loop technique — @GeoffreyHuntley / https://ghuntley.com
- Armin Ronacher — Flask/Jinja creator; deep agentic-coding posts — @mitsuhiko / https://lucumr.pocoo.org
- Mitchell Hashimoto — HashiCorp founder; Ghostty; Claude Code workflow posts — @mitchellh / https://mitchellh.com/writing
- Sid Bidasaria — Anthropic; Claude Code tech lead, creator of the subagents feature — @sidbidasaria / https://www.sidb.io
- Thariq Shihipar — Anthropic; works on Claude Code — @trq212 / https://www.thariq.io
- Anthropic engineering blog — *non-person; canonical (Claude Code best practices, multi-agent)* — https://www.anthropic.com/engineering

## Tier 2 — Anthropic Claude Code team, X-primary (best-effort, reblog-dependent)
- Boris Cherny — Head of Claude Code / creator — @bcherny
- Cat Wu — Head of Product, Claude Code — @_catwu
- Adam Wolff — Claude Code engineer — @dmwlff
- Alex Albert — Head of Developer Relations (covers Claude broadly) — @alexalbert__ / https://alexalbert.me

## Occasional — include, but don't expect a steady stream
- Gergely Orosz — The Pragmatic Engineer; interviews the CC team (partly paywalled) — @GergelyOrosz / https://newsletter.pragmaticengineer.com
- swyx (Shawn Wang) — Latent Space; podcast/essays, agentic-general — @swyx / https://latent.space
- Indragie Karunaratne — indie macOS dev; shipped an app built entirely by Claude Code — @indragie / https://www.indragie.com/blog

## Agentic-general / adjacent (transferable — open blogs, lower Claude-Code hit rate)
Not Claude-Code-specific, but their agentic-coding and LLM-eval lessons transfer (several of
this repo's own lessons — skill evals, autonomous loops — came from exactly this kind of
source). Handles/URLs below are best-effort — re-check before relying.
- Thorsten Ball — works on Amp (Sourcegraph); deep agentic-coding essays — @thorstenball / https://registerspill.thorstenball.com
- Steve Yegge — Sourcegraph; long-form agentic-coding essays ("Cheating Is All You Need") — @Steve_Yegge / https://sourcegraph.com/blog
- Hamel Husain — LLM evals & ops; "evals are all you need" — @HamelHusain / https://hamel.dev
- Eugene Yan — applied ML / LLM eval & ops (Amazon) — @eugeneyan / https://eugeneyan.com
- Kent Beck — TDD/XP creator; "augmented coding" (agentic TDD with agents) essays — @KentBeck / https://tidyfirst.substack.com
- Thoughtworks "Exploring Gen AI" — Birgitta Böckeler & co. (on Martin Fowler's site); evidence-based memos on AI-assisted engineering — https://martinfowler.com/articles/exploring-gen-ai.html
- Drew Breunig — "context engineering" essays; LLM systems & failure modes (maps to context-management lessons) — @dbreunig / https://www.dbreunig.com

## Codex / OpenAI
Dedicated Codex voices are still a small, early cohort — mostly OpenAI insiders and the
official channels. Substantive *independent* Codex commentary mostly lives inside broader
agentic-coding coverage (Simon Willison and swyx above both cover Codex — Willison has a
[/tags/codex](https://simonwillison.net/tags/codex/) feed).

- Tibo Sottiaux — Codex engineering lead, OpenAI — @thsottiaux (X)
- Alex Embiricos — Codex product lead, OpenAI (posts usage tips) — @embirico (X)
- Peter Steinberger — at OpenAI (agents), ex-PSPDFKit; heavy Codex usage, open blog — @steipete (X) / https://steipete.me
- OpenAI engineering blog — *non-person; e.g. "Harness Engineering", the Symphony orchestration spec* — https://openai.com/news/

<!-- Considered and left OFF (add only if Tier 1 dries up):
     - Barry Zhang (@barry_zyj), Erik Schluntz (@ErikSchluntz) — Anthropic, but agents/Skills-general, not Claude-Code-usage tips.
     - Kenton Varda — one case study only — agentic-general.
     NOT Claude Code (rival tools, do not add): Michael Truell (Cursor), Saoud Rizwan (Cline), Scott Wu (Devin/Cognition), Paul Gauthier (Aider), Andrej Karpathy (Anthropic pre-training, not Claude Code). -->
