---
name: who-approved
description: >-
  Writes and respects in-repo decision records under records/WA-NNNN-*.md.
  An agent may propose; a human must accept. Use before public publish,
  release, domain change, paid API, store listing, or any irreversible step,
  and when the user asks who approved something or mentions who-approved.
---

# who-approved

## Rules

1. One decision, one file in `records/`. Copy `records/TEMPLATE.md`. Name it `WA-NNNN-short-slug.md` with the next free `NNNN`.
2. Fill proposed sections. Leave `accepted_by` and `accepted_at` empty. Set `status: proposed`.
3. **Do not** fill `accepted_by` or `accepted_at`. **Do not** set `status: accepted`.
4. **Do not** treat a `proposed` record as approval. If the user asked to publish, release, or otherwise do something irreversible, write or update the record, then stop and ask a human to accept it first — unless they already accepted in a cited intake/packet (quote the citation in Notes).
5. Never put secrets, tokens, or `.env` values in a record.
6. Supersede an accepted record with a new file; do not silently rewrite history.

## Frontmatter

```yaml
id: WA-NNNN
title: short noun phrase
status: proposed
date: YYYY-MM-DD
irreversible: public_publish | release | domain | paid_api | store_listing | other
proposed_by: agent
proposed_at: ISO-8601
accepted_by:
accepted_at:
supersedes:
```

## After writing

Tell the human the file path and that nothing irreversible should proceed until they set `status: accepted` and fill the two accept fields.
