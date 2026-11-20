# who-approved

[![License: MIT](https://img.shields.io/github/license/konstantinbozukov/who-approved)](./LICENSE)

In-repo decision records for work done with coding agents: **an agent may propose, a human must accept.** Chat is not approval.

## Why this exists

Small teams who ship with coding agents get asked "who approved this?" A chat transcript is not an answer, and a compliance suite is the wrong product. `who-approved` is a markdown file in the repo. Until a human accepts the record, do not treat publish, release, a domain change, or any other irreversible step as approved.

## 30-second look (nothing to install)

```bash
git clone https://github.com/konstantinbozukov/who-approved
cd who-approved
python3 scripts/check.py
```

On this repository that prints `ok (1 record(s))` and exits 0. The accepted example is [`records/WA-0001-public-github.md`](records/WA-0001-public-github.md). (`python scripts/check.py` is the same script, if `python` is what you have on PATH.)

The checker has no flags. It exits 0 when every file in `records/` is either the template, still `proposed`, or `accepted` with both accept fields filled. It exits 1 if a record claims `accepted` without `accepted_by` and `accepted_at`, or if a `proposed` record already has those fields. It is a lint over frontmatter, not proof that a human typed the name.

## Use it in your repo

Copy the skill and a blank record:

```text
.cursor/skills/who-approved/SKILL.md
records/TEMPLATE.md
```

Tell the agent to use the **who-approved** skill before a public ship, a release, a domain change, a paid API, a store listing, or anything you cannot cheaply undo.

## Record

One decision, one file, under `records/`.

- Filename: `WA-NNNN-short-slug.md`
- Agent fills the proposed sections. Status stays `proposed`.
- A human fills `accepted_by` and `accepted_at` and sets `status: accepted`. An agent must not.
- `status: proposed` is not approval.

See [SCHEMA.md](SCHEMA.md) (schema v0) and the worked example [records/WA-0001-public-github.md](records/WA-0001-public-github.md).

## Scope and non-goals

Not a dashboard. Not a prompt log. Not Jira. Not auto-approve. Not an npm or PyPI package. Not a cryptographic signature over the accept fields. Adjacent in spirit to portable, file-based decision records — this is a thin, in-repo binding: plain files, human accept, vendor-neutral.

## Related

- Read-only inventory of local MCP servers and extensions that can act as you: [who-can-act](https://github.com/konstantinbozukov/who-can-act)
- Optional runtime consult before an x402 payment: [agent-trust-layer](https://github.com/konstantinbozukov/agent-trust-layer)

## License

MIT. See [LICENSE](LICENSE).