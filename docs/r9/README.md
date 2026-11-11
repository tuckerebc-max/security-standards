# R9 — Workspace CLI gap assessment

**Decision: stop before building or authenticating an adapter.** No operation in the reviewed evidence meets both R9 conditions: a required Workspace operation that current connectors cannot satisfy, and a Codex or Hermes lane verified to lack a connector. This is a bounded finding, not a claim that the whole fleet has no gaps.

Prepared 11 November 2026 · [ERI-1985](https://linear.app/eric-tucker/issue/ERI-1985/r9-evaluate-conditional-google-workspace-cli-adapter-for-codex-and)

## What was checked

The current Codex seat exposes 84 Workspace tools: 45 Drive/Docs/Sheets/Slides, 21 Gmail, 15 Calendar and 3 Contacts. Tool exposure establishes an available interface; it does not establish every operation's live success.

The Study Group AI Operating Stack project and its complete issue listing were inspected, together with the actual work requirements in ERI-6, ERI-48, ERI-1906 and ERI-1948. ERI-840 records an older parity package, not a current runtime test. Targeted Linear and continuity searches did not establish a new required operation beyond those below. Searches are discovery evidence, not proof of fleetwide absence.

## Gap list

| ID | Needed operation and source | Existing connector route | Evidence and disposition |
|---|---|---|---|
| G1 | Verify identity; discover workplans and metadata — ERI-6/48 | Profile, paginated search, file metadata | Current Personal 2 identity was verified. ERI-6's work principal was not tested. Its August missing-token report is an authentication blocker; current Hermes state is unknown. No qualifying gap established. |
| G2 | Read native Docs workplans with provenance — ERI-6/48 | Native document and text readers, including tabs; file metadata | Interface exists; no work-account document body was read. ERI-48 is a Gemini assignment. No qualifying Codex/Hermes gap established. |
| G3 | Inventory archive folders and discover sources — ERI-1906 | Folder listing, filtered/paginated search and metadata | Folder fetch has a bounded result size; search has provider pagination. Two metadata-only search pages remained incomplete. Complete mixed-file enumeration is unknown. Current seat has a connector. |
| G4 | Retrieve stored archive files and export native documents — ERI-1906/1948 | Raw fetch, native export and metadata | Interfaces exist, with provider limits. Content access, large-file handling and authorized transport were not exercised. No verified unmet operation. |
| G5 | Create chapter folders and deliver/update private files — ERI-1906/1948 | Folder creation, upload and file update | Write interfaces exist. No Workspace writes were performed in this read-only assessment. |
| G6 | Verify handoff identity, revisions and received bytes — ERI-1948 | Metadata, revision reads and raw fetch | Source-side interfaces exist. Hermes receiver access is unknown; sender-side success would not prove receipt. |

Detailed tool mappings and qualifications are in [r9-assessment.json](r9-assessment.json). Gmail, Calendar, Contacts and additional Workspace APIs do not enter the allowlist merely because gws supports them: no qualifying lane need was established for them.

## Read-only baseline checks

| Check | Observed result | Tool-call wall time |
|---|---|---:|
| C1: connector profile | Personal 2 principal verified; distinct from the work principal named in ERI-6 | Unknown; not instrumented |
| C2: known archive-folder metadata | Folder MIME type returned; response explicitly reports `access_not_verified` | 223 ms |
| C3: bounded folder-search page | No visible rows; continuation token present | 704 ms |
| C4: next page using the unchanged provider token | No visible rows; continuation token still present | 454 ms |

The search canary stopped after two planned pages. Neither page demonstrates an empty folder or a complete census. Tokens and private file identifiers are excluded from the public evidence. There were no private content downloads, CLI calls, OAuth flows or Workspace mutations.

Defects found, false positives, human review minutes, CLI latency, measured cost and comparative improvement are **unknown**. There was no paired CLI benchmark or measured human review session. The count of verified qualifying gaps in this bounded review is zero; the fleetwide gap count is unknown.

## Access register

The earlier intake already defined **ACCESS-001** in [harvest-external-capability PR #1](https://github.com/tuckerebc-max/harvest-external-capability/pull/1). This assessment preserves that ID in [security-standards' proposed register entry](../../agent-access-register/ACCESS-001.json), rather than creating a second grant identity. The baseline security-standards tree contained no access-register path; this entry is on the R9 review branch, not merged policy.

No new scopes are requested or approved. Actual grants outside this assessment are unknown. The earlier Gmail/Drive/Calendar proposal is retained as provenance and is not a grant request.

For a future verified workplan gap, the scope alternatives are:

| Specific future operation | Candidate scope |
|---|---|
| Discover existing workplans and inspect Drive metadata | `https://www.googleapis.com/auth/drive.metadata.readonly` |
| Read an already identified native Google Doc | `https://www.googleapis.com/auth/documents.readonly` |

Only a task needing both operations would need both scopes. These read-only scopes still span the account's relevant metadata/documents; they do not enforce folder-specific access. Google's per-file `drive.file` option has write capability and is not interchangeable with an account-wide read-only discovery grant. Exact file/parent restrictions, account binding and data-route approval would remain separate controls.

ERI-6 identifies the Eric work principal as a candidate for that workstream; it does not approve a new gws grant. Eric must approve any future account and exact scopes before authentication. Eric personal, Eric work and Sheryl work remain separate. Credentials stay in native stores; no credential values or exports were read or recorded.

Scope references: [Drive](https://developers.google.com/workspace/drive/api/guides/api-specific-auth) and [Docs](https://developers.google.com/workspace/docs/api/auth).

## Upstream review and pin

The existing intake's pin was reused and verified:

- Repository: [googleworkspace/cli](https://github.com/googleworkspace/cli).
- Commit: `cd3697e07eb520056dcf142d0c7439bbb9ba32e9`, dated 30 October 2026.
- Declared package version: **0.22.5**.
- License: **Apache-2.0**, verified from the pinned manifest and license file.
- Qualification: static source/documentation review only; no binary installed or runtime tested.

Upstream disclaims official Google product support and warns that breaking changes may occur before v1.0. Its command surface comes from Google's live Discovery service, so a source-version pin alone does not freeze the API surface. Its own discovery, authentication and pagination would remain authoritative if an adapter were later justified. No upstream source, prompts or prose were adapted into a wrapper.

Pinned source links and Git object hashes are retained in [r9-evidence.json](r9-evidence.json). Neither an installation script nor a command from upstream documentation was executed. No telemetry was enabled by this lane; upstream telemetry behavior was not runtime-tested.

## Acceptance and resume point

The gap list, access record, source pin and bounded baseline evidence are delivered. The wrapper, refusal tests, per-call gws receipts, AGENTS/CLAUDE/Hermes entry notes, contract.json and 0/1/2 CLI are **not applicable under R9's explicit stop branch**. Building them without a qualifying operation would contradict the commission.

Kata is the execution-ledger standard. No Kata binary or connector was exposed in this runtime, so a Kata receipt is unavailable; no substitute execution-ledger service was created. Linear holds this assessment and its delivery receipt.

Reopen ERI-1985 when a lane supplies a named unmet operation plus current evidence of connector absence or insufficient coverage. Record the exact principal, scope set, permitted files/folders and data route; obtain Eric's account/scope approval; then build only the required allowlisted operation, negative tests and sanitized receipts. Keep the pilot read-only and pin the exact executable before testing.

This assessment is ready for review of the **stop decision**, not approval of a deployed adapter or an OAuth grant.
