# Record schema (v0)

Plain markdown plus YAML frontmatter. Inspired by portable AI decision records (human propose → accept, files in git). Not a konspekt graph implementation.

## Filename

`records/WA-NNNN-short-slug.md`

`NNNN` is a zero-padded integer unique in `records/`. Skip `TEMPLATE.md`.

## Frontmatter

| Field | Who writes it | Rules |
|-------|----------------|-------|
| `id` | Agent | `WA-NNNN`, matches filename |
| `title` | Agent | Short noun phrase |
| `status` | Agent proposes `proposed`. Human sets `accepted`. | Never `accepted` without accept fields |
| `date` | Agent | ISO date the record was opened |
| `irreversible` | Agent | `public_publish` \| `release` \| `domain` \| `paid_api` \| `store_listing` \| `other` |
| `proposed_by` | Agent | `agent` or a named agent/chat |
| `proposed_at` | Agent | ISO datetime |
| `accepted_by` | **Human only** | Name or stable handle. Empty while proposed |
| `accepted_at` | **Human only** | ISO datetime. Empty while proposed |
| `supersedes` | Agent or human | Optional `WA-NNNN` of an older record |

Supersede; do not silently rewrite an accepted record.

## Body

```markdown
## Decision

One sentence: what becomes true if this is accepted.

## Why

Short. What broke or what window exists.

## Alternatives considered

At least one, even if “do nothing.”

## Blast radius

What goes wrong if this was a bad call.

## Notes

Optional links to PRs, chats, or packets. No secrets.
```

## Accepting

A human edits the file:

```yaml
status: accepted
accepted_by: Ada
accepted_at: 2026-09-12T15:00:00Z
```

An agent must not fill those two fields. An agent must not treat `proposed` as approved.
