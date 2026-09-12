# who-approved

Small teams who ship with coding agents get asked **who approved this?**

Chat is not an answer. A compliance suite is the wrong product. **who-approved** is a markdown file in the repo: an agent may propose the decision; a human must accept it. Until then, do not treat publish, release, or any other irreversible step as approved.

## Install

Copy the skill into your repo:

```text
.cursor/skills/who-approved/SKILL.md
```

Copy `records/TEMPLATE.md` to `records/` (or keep using this repo as the example).

Tell the agent to use the **who-approved** skill before a public ship, a release, a domain change, or anything you cannot cheaply undo.

## Record

One decision, one file, under `records/`.

- Filename: `WA-NNNN-short-slug.md`
- Agent fills the proposed sections.
- A human fills `accepted_by` and `accepted_at`. An agent must not.
- `status: proposed` is not approval. Only `status: accepted` with both accept fields counts.

See [SCHEMA.md](SCHEMA.md) and the worked example [records/WA-0001-public-github.md](records/WA-0001-public-github.md).

Optional check (Python 3, stdlib only):

```text
python scripts/check.py
```

Exits `0` when every file in `records/` is either a template, still `proposed`, or honestly `accepted`. Exits `1` if a record claims accepted without a human.

## What this is not

Not a dashboard. Not a prompt log. Not Jira. Not auto-approve. Not FINOS konspekt’s full graph — this is a thin, in-repo binding with the same idea: plain files, human accept, vendor-neutral.

## License

MIT. See [LICENSE](LICENSE).
