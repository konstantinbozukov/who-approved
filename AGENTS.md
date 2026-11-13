# Agent rules for who-approved

who-approved is a small public convention for coding agents. An agent may propose an irreversible decision. A human must accept it. The decision is a markdown file in `records/`. Chat is not approval. `status: proposed` is not approval.

Repository: https://github.com/konstantinbozukov/who-approved
Default branch: `master`
License: MIT (`LICENSE`, copyright Konstantin Bozukov, 2026)
Schema version in `SCHEMA.md`: v0
Latest commit audited: `d162cbb` (2026-09-12)

This file is operational. Evidence and findings are in `docs/AUDIT.md`.

## Stack

- Decision records: Markdown with YAML frontmatter (`SCHEMA.md`, `records/`).
- Agent skill: `.cursor/skills/who-approved/SKILL.md`.
- Checker: `scripts/check.py`, Python 3, standard library only (`pathlib`, `sys`). No application server, database, or third-party package.
- Hosting: the GitHub repository itself. No app deploy.

## Folder layout

```text
.cursor/skills/who-approved/SKILL.md   rules an agent must follow
records/TEMPLATE.md                    blank record; checker skips this filename
records/WA-NNNN-short-slug.md          one decision per file
scripts/check.py                       partial gate (see below)
SCHEMA.md                              field and body rules
README.md                              install text for a stranger
LICENSE                                MIT
.gitignore                             editor junk, .venv, __pycache__, .env
docs/AUDIT.md                          2026-11-13 read-only audit
```

Eight tracked files existed before this docs change. There is no `src/`, test suite, `.github/`, package manifest, Dockerfile, or deploy config.

## Install

Nothing to install. There is no `requirements.txt`, `pyproject.toml`, `package.json`, or lockfile. Do not add one for a drive-by task.

A consumer repo copies:

- `.cursor/skills/who-approved/SKILL.md`
- `records/TEMPLATE.md` (or keeps using this repo as the example)

Then it tells the agent to follow the skill before a public ship, a release, a domain change, a paid API, a store listing, or anything that cannot be cheaply undone.

## Run

Verified on 2026-11-13 with Python 3.12.3:

```text
python3 scripts/check.py
```

Stdout was `ok (1 record(s))`. Exit code was `0`.

`README.md` tells people to run `python scripts/check.py`. On this machine `python` is not on `PATH` (`command not found`). The script's shebang is `python3`, and the git mode is `100644`, so `./scripts/check.py` exits `126` (permission denied). Use `python3 scripts/check.py`.

TODO: confirm with Konstantin which command he runs locally.

What the checker actually does: it reads `records/*.md`, skips a file whose name uppercases to `TEMPLATE.MD`, and checks that `id` starts with `WA-`, `status` is `proposed` or `accepted`, an accepted record has both accept fields non-empty, and a proposed record has both accept fields empty. Exit `0` is that narrow check. It is not full `SCHEMA.md` compliance. Details and executed bypasses are in `docs/AUDIT.md`.

With only `TEMPLATE.md` present, stderr says `no records to check (template only is ok)` and stdout says `ok (0 record(s))`. Exit code is still `0`.

## Test

No unit tests exist. Verified 2026-11-13:

```text
python3 -m unittest discover -s . -v
```

Result: `Ran 0 tests`, `NO TESTS RAN`, exit `5`.

```text
python3 -m pytest -q
```

Result: `/usr/bin/python3: No module named pytest`, exit `1`. Pytest is not a project dependency. Do not install it unless Konstantin asks.

## Lint

No linter, formatter, or type-checker config is in the repo. Do not add Ruff, Black, or mypy unless asked.

Syntax check that was run:

```text
python3 -m py_compile scripts/check.py
```

Exit `0`. That writes `scripts/__pycache__/`, which `.gitignore` ignores. Delete it rather than committing it.

## Build

No build. No artifact, bundle, or image. `py_compile` is only a syntax check.

## Deploy

No deploy pipeline. GitHub Actions workflow count on 2026-11-13 was `0`. GitHub Pages is off. Releases API returned an empty list. `master` protection is off.

The ship path this repo documents is a file copy into the consumer's repo, plus this public GitHub repo as the place a stranger clones. `records/WA-0001-public-github.md` records the decision to publish `github.com/konstantinbozukov/who-approved`. That record is already `accepted`. Do not treat a new publish, release, domain change, paid API, or store listing as approved until a human accepts a record for that decision.

TODO: confirm with Konstantin that nothing is deployed outside this repository.

## External services

None are called by the code. No Supabase, Vercel, AWS, database, or HTTP client. GitHub hosts the git repo. The example record cites `ideas/007-production-factory/dogfood/who-approved/intake.md` in a repo named `tech-business-ideas`. That file is not in this workspace and was not opened.

TODO: confirm with Konstantin that the intake file is still the authority for `WA-0001`.

## How to change a decision

1. Read `.cursor/skills/who-approved/SKILL.md` and `SCHEMA.md`.
2. Copy `records/TEMPLATE.md` to `records/WA-NNNN-short-slug.md`. Use the next free zero-padded `NNNN`. `WA-0001` is taken.
3. Fill the proposed fields and the body sections (`Decision`, `Why`, `Alternatives considered`, `Blast radius`, optional `Notes`).
4. Leave `accepted_by` and `accepted_at` empty. Leave `status: proposed`.
5. Run `python3 scripts/check.py`.
6. If the human already accepted in a cited intake or packet, quote that citation in `Notes`. Still do not invent `accepted_by` or `accepted_at`.
7. To replace an accepted record, add a new file and set `supersedes`. Do not rewrite the accepted file in place.

## Coding conventions

Inferred from `scripts/check.py` and the markdown, not from a style guide:

- Python 3, standard library only. `from __future__ import annotations`. `pathlib` for paths. `main() -> int` and `raise SystemExit(main())`. Errors on stderr, one success line on stdout, exit `0` or `1`. Double quotes, four-space indent, a module docstring, no extra comments.
- Records: one decision per file. Filename `WA-NNNN-short-slug.md`. `id` is `WA-NNNN` and matches the filename. Dates and times are ISO-8601. `irreversible` is one of `public_publish`, `release`, `domain`, `paid_api`, `store_listing`, `other`.
- Prose in the README and schema is short and direct. No emoji, no dashboard, no prompt log.
- The worked example's accept fields name a human (`Konstantin Bozukov`). The checker does not enforce that. You still must not write a human's name into `accepted_by`.

## Never touch

- `accepted_by`, `accepted_at`, and any edit that sets `status: accepted`. A human writes those. An agent does not.
- Accepted records already in `records/`, including `records/WA-0001-public-github.md`. Supersede with a new file. Do not silently rewrite history.
- Secrets, tokens, passwords, private keys, and `.env` values. Never put them in a record, a commit, or a doc. `.gitignore` ignores `.env` and `.env.*`. None are tracked.
- Production data. There is no database. `records/` is the data. Do not invent a data store.
- Migrations. There are none. Do not add a migration framework.
- Store or deploy config. There is no Vercel, Supabase, AWS, Docker, or CI config. Do not add one unless Konstantin asks.
- `LICENSE` copyright and the MIT terms, unless Konstantin asks.
- Dependency manifests. The README promises Python 3 and the standard library. Do not add packages to make the checker "real YAML" unless he asks.

## Before an irreversible step

Public publish, release, domain change, paid API, store listing, or anything that cannot be cheaply undone: write a `proposed` record, then stop and ask Konstantin to accept it. A `proposed` record is not permission to do the thing.
