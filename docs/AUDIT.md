# Audit — who-approved

Audit date: 2026-11-13
Repo: https://github.com/konstantinbozukov/who-approved
Commit: `d162cbb393a969ef7da0a60dea9d8713a2e86b7a`
Commit subject: `Make who-approved installable from a public repo.`
Commit author: `bozukov` (GitHub login `konstantinbozukov`), committed 2026-09-12T15:20:17Z
Commit signature: unsigned (`verification.reason` was `unsigned`)
Scope: read-only. No application code, config, dependency, CI, or infrastructure files were changed. Checker bypasses were reproduced by copying `scripts/check.py` into a temp directory. Those fixtures were deleted and were never committed.

## Summary

who-approved is a public, file-based rule for small teams that ship with coding agents: one markdown decision record per irreversible step, an agent may propose it, and a human must accept it. The tree is a Cursor skill, a schema, a blank template, one accepted example (`WA-0001`), a 70-line standard-library checker, a short README, and an MIT license. Maturity: **working early v0**. A stranger can clone the public repo and copy the skill, which is the success test named in `WA-0001`, and `python3 scripts/check.py` exits 0 on the real records. Production-grade enforcement would require a checker that rejects forged accept fields, unit tests, CI, and branch protection. Those are absent today: the checker exits 0 for forged accept fields, `python3 -m unittest discover` runs 0 tests, GitHub Actions has 0 workflows, the releases list is empty, and `master` is unprotected. The only commit is from 2026-09-12. The record's own bar is `public_usable`.

## Stack and hosting

| Piece | What is in the repo |
| --- | --- |
| Records | Markdown plus YAML frontmatter, schema titled v0 in `SCHEMA.md` |
| Agent interface | `.cursor/skills/who-approved/SKILL.md` |
| Checker | `scripts/check.py` — Python 3, imports only `pathlib` and `sys` |
| License | MIT, copyright Konstantin Bozukov, 2026 |
| Host | Public GitHub repo, default branch `master`. Created 2026-09-12T15:21:39Z, pushed 2026-09-12T15:21:42Z. GitHub API `size` was 5 KB. Language reported as Python. |
| App host | None. `homepage` is null. `has_pages` is false. |
| Data store | The `records/` directory. No database. |

GitHub metadata read on 2026-11-13: 0 stars, 0 forks, 0 open issues, issues API with `state=all` returned an empty page (that API includes pull requests), 0 releases, 0 Actions workflows, topics empty, discussions off, `allow_forking` true, `delete_branch_on_merge` false, all three merge methods allowed, auto-merge off.

No Supabase, Vercel, AWS, or other vendor SDK appears in any tracked file.

## Deploy path

There is no deploy. Nothing in the repo builds or ships a service.

What exists instead:

1. Publish path already taken: one commit on `master`, public at `github.com/konstantinbozukov/who-approved`. `records/WA-0001-public-github.md` says that publish was accepted by Konstantin Bozukov, with the note that the accept happened in an intake interview rather than as a later edit of the file.
2. Install path for a consumer: copy `.cursor/skills/who-approved/SKILL.md` and `records/TEMPLATE.md` into their repo. README lines 7–15.
3. Optional local check: `python3 scripts/check.py`. No CI runs it. Workflow list `total_count` was 0. `master` protection object said `protected: false` and `required_status_checks.enforcement_level` was `off`.

`WA-0001` alternatives considered say npm and the Cursor directory were rejected for day one. TODO: confirm with Konstantin that this is still the only ship path.

## Environment variables

No environment-variable names are read anywhere. `scripts/check.py` does not call `os.environ` or `getenv`. No `.env`, `.env.example`, or other env file is tracked (`git ls-files` listed eight paths before this audit). `.gitignore` lines 6–7 ignore `.env` and `.env.*`.

## Tests

Nothing was installed. There is no dependency manifest to install.

Commands run on this machine (Python 3.12.3, `/usr/bin/python3`) against the repo at `d162cbb`:

| Command | Result |
| --- | --- |
| `python3 --version` | `Python 3.12.3` |
| `python3 -m py_compile scripts/check.py` | exit 0 |
| `python3 scripts/check.py` | exit 0, stdout `ok (1 record(s))` |
| `python scripts/check.py` (the README command, `README.md:33`) | `python: command not found`. `python` is not on `PATH` here. |
| `./scripts/check.py` | exit 126, `Permission denied`. Git mode of `scripts/check.py` is `100644`. The shebang on line 1 is `#!/usr/bin/env python3`. |
| `python3 -m unittest discover -s . -v` | `Ran 0 tests in 0.000s`, `NO TESTS RAN`, exit 5 |
| `python3 -m pytest -q` | `/usr/bin/python3: No module named pytest`, exit 1 |

Coverage: there are no tests, so coverage is zero. The checker is a script, not a test suite. It passed on the one real record and missed the bypasses below.

A temp copy of the checker was also run against fixtures that are not in git. Those results are cited under bugs. The real-repo command remained `ok (1 record(s))`.

## Bugs and likely bugs

### Confirmed by running the checker

1. **Forged acceptance exits 0.** `scripts/check.py:49-54` treats any non-empty stripped string as `accepted_by` / `accepted_at`. The docstring at `scripts/check.py:2` and `README.md:36` say the script fails when a record claims accepted without a human. The code never looks at who the human is. Temp-copy results, each file alone:
   - `status: accepted`, `accepted_by: ""`, `accepted_at: ""` → `ok (1 record(s))`, exit 0.
   - `status: accepted`, `accepted_by: agent`, `accepted_at: 2026-09-12T15:11:00Z` → exit 0.
   - `status: accepted`, `accepted_by: null`, `accepted_at: ~` → exit 0.
2. **The same quote token fails the other way on a proposed record.** `scripts/check.py:23-24` keeps the quotes. `status: proposed` and `accepted_by: ""` hit `scripts/check.py:55-60` and exit 1 with `proposed record must not have accept fields`. A YAML empty string would be empty. This parser sees two quote characters.
3. **A later duplicate key overwrites the earlier one, and the forged accept passes.** Same split, stored in a dict (`scripts/check.py:23-24`). A frontmatter that set `status: proposed` and empty accept fields, then later set `status: accepted`, `accepted_by: agent`, and a timestamp, printed `ok (1 record(s))` and exited 0.
4. **`id` only has to start with `WA-`.** `scripts/check.py:43`. `id: WA-NNNN` with `status: proposed` exited 0. `SCHEMA.md:15` says the id is `WA-NNNN` and matches the filename. A copied template that was renamed on disk and not edited inside would pass.
5. **Filename, enum, body, supersedes, and time order are not read.** `scripts/check.py:39-60` never checks them. One temp record named `WA-0006-mismatch.md` with `id: WA-9999`, `irreversible: not-an-enum`, `supersedes: WA-DOES-NOT-EXIST`, and no body exited 0. `SCHEMA.md:19` lists the allowed `irreversible` values. `SCHEMA.md:32-49` requires `Decision`, `Why`, `Alternatives considered`, and `Blast radius`.
6. **Duplicate ids pass.** Two temp files, both `id: WA-0008`, one of them `accepted_by: agent`, printed `ok (2 record(s))` and exited 0.
7. **The shipped example inverts the two timestamps, and the real checker still passes.** `records/WA-0001-public-github.md:8` is `proposed_at: 2026-09-12T15:10:00Z`. Line 10 is `accepted_at: 2026-09-12T15:07:00Z`. Accept is three minutes before propose. `python3 scripts/check.py` on the repo still exits 0. Line 33 says the governor accept happened in the intake interview, not as a later edit of the file. TODO: confirm with Konstantin that the earlier accept time is intentional. Do not "fix" this by editing the accepted record in place. The skill says to supersede, and only a human writes accept fields.
8. **Inline comments are kept as part of the value.** `status: accepted # not really` exited 1 (`status must be proposed or accepted`). That one fails closed. It shows the parser is not YAML.

### From the code, not given its own forged fixture

9. **Any file whose name uppercases to `TEMPLATE.MD` is skipped** (`scripts/check.py:35-36`). The real template-only case prints `no records to check (template only is ok)` on stderr and `ok (0 record(s))` on stdout, exit 0, which matches a blank repo. A decision stored under that filename would not be checked. That specific forgery was not executed.
10. **README command and executable bit disagree with this machine.** See the test table. `README.md:33` says `python scripts/check.py`. The file mode is `100644`.

## Security

No committed secret was found. Report is paths and settings only.

- Tracked paths before this audit: `.cursor/skills/who-approved/SKILL.md`, `.gitignore`, `LICENSE`, `README.md`, `SCHEMA.md`, `records/TEMPLATE.md`, `records/WA-0001-public-github.md`, `scripts/check.py`.
- Search for `os.environ`, `getenv`, `API_KEY`, `secret`, `token`, `password`, `AKIA`, private-key blocks, and vendor names hit only the skill and schema sentences that forbid secrets (`SKILL.md:18`, `SCHEMA.md:49`).
- `git grep` for `ghp_`, `github_pat_`, `xox[baprs]-`, `AKIA[0-9A-Z]{16}`, `sk_live_`, and `BEGIN … PRIVATE KEY` returned no matches.
- `.gitignore:6-7` ignores `.env` and `.env.*`. No env file is tracked.

The risk that matters is integrity of an "accepted" decision, not credential theft.

- The checker exits 0 for `accepted_by: agent`, `null`, `~`, and `""` (bugs 1–3, 6). Anyone who can commit a record can mark it accepted and the only advertised check agrees.
- `master` is unprotected (`protected: false`, required status checks off). Direct pushes are allowed for accounts that already have push. A collaborator list was not fetched, so this audit does not name any writer besides the owner account that owns `master`. `web_commit_signoff_required` is false. The only commit is unsigned.
- No workflow runs the checker, so a pull request does not fail closed.
- `scripts/check.py` has no network, shell, or `eval`. It only reads `records/*.md`. The script itself is not an injection sink.
- Record bodies are free text an agent may read later. `WA-0001` does not contain an instruction payload. A future record could. The skill already says a proposed file is not approval.
- `WA-0001` blast radius says no user data is hosted. The code matches that: no database and no app.
- GitHub secret scanning and secret-scanning push protection are `enabled`. Dependabot security updates are `disabled`. Non-provider secret patterns are `disabled`. Secret-scanning validity checks are `disabled`. With no dependency manifest, Dependabot has nothing to update. That setting becomes a gap only if dependencies are added later.

## Dependencies and staleness

No third-party dependencies. Nothing to upgrade, and nothing pinned.

- No `requirements.txt`, `pyproject.toml`, `Pipfile`, `package.json`, `go.mod`, `Cargo.toml`, `Dockerfile`, or lockfile.
- Imports are `pathlib` and `sys` (`scripts/check.py:5-6`).
- Runtime used for this audit: Python 3.12.3. The repo does not pin a version (no `.python-version`, `runtime.txt`, or `requires-python`). TODO: confirm with Konstantin which Python versions must keep working.
- Project staleness: one commit, pushed 2026-09-12, audited 2026-11-13. No git tags. Releases API returned `[]`. `SCHEMA.md` is titled v0. No changelog. Open issue count was 0.
- Dependabot security updates disabled, which matches "no manifest" and leaves no automated nag if a dependency is added later.

## Top 5 improvements

Ranked by value to the promise "a human must accept," then by how small the change is.

1. **Fail closed on fake accept fields.** Value: highest. This is the bug the README claims not to have. Effort: small, local to `scripts/check.py` (`fields` and the two accept branches). Stay on the standard library. Reject a blank YAML string, `""`, `null`, `~`, `none`, and `agent`, and reject a second key that flips `status`.
2. **Add standard-library unit tests for the cases in this audit.** Value: high. `python3 -m unittest discover` currently runs 0 tests and exits 5, which is how bugs 1–6 stayed invisible. Effort: small, a new `tests/` module and `python3 -m unittest`. Pytest is not installed and is not required.
3. **Run that check on pull requests, and protect `master`.** Value: high. Zero workflows and `protected: false` mean a perfect script still never runs. Effort: one Actions workflow that runs `python3 scripts/check.py` and the tests. Branch protection and required reviews are a GitHub setting, and only Konstantin can turn them on.
4. **Enforce the rest of `SCHEMA.md`.** Value: medium. Stops template leftovers, mismatched filenames, duplicate ids, bad `irreversible` values, missing body sections, dangling `supersedes`, and accept-before-propose. Effort: still inside `scripts/check.py`, no new dependency. The `WA-0001` timestamp question should be answered by Konstantin before anyone rewrites that file.
5. **Make the stranger instructions match a machine like this one, and mark a version.** Value: smaller, and it is the success test `WA-0001` names (a stranger following the README). `python` was missing here; `python3 scripts/check.py` worked. Schema text says v0, and there is no tag or release. Effort: a README command line, plus a version or tag if Konstantin wants one. TODO: confirm with Konstantin before tagging.

## Open questions

1. Is `accepted_at` three minutes before `proposed_at` in `records/WA-0001-public-github.md` intentional, because the chat accept (15:07Z) preceded the file's `proposed_at` (15:10Z)?
2. Should `master` require a review and a green check before a record can become `accepted`? Protection is off today.
3. Are npm and the Cursor directory still out of scope, as `WA-0001` alternatives considered say?
4. Which Python versions must `scripts/check.py` support? Only 3.12.3 was executed here, and `python` was not on `PATH`.
5. Is `ideas/007-production-factory/dogfood/who-approved/intake.md` in `tech-business-ideas` still the authority cited in `WA-0001` notes? It is not in this repo and was not opened.
6. Is any non-human `accepted_by` (for example the literal `agent`) always invalid, or is there a human handle the checker should allow-list?
7. Is there a deploy, secret, or hosted environment outside this repository? None is referenced in the tracked files.
