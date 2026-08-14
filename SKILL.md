---
name: security-standards
description: Review, design, and remediate application security controls in source code, configuration, dependencies, CI/CD, and incident-response plans. Use when Codex is asked for a security review, secure-coding guidance, threat-informed hardening, secret or dependency hygiene, vulnerability triage, a security checklist, or implementation of approved security fixes across Python, JavaScript/TypeScript, web, SQL, shell, and infrastructure projects.
---

# Security Standards

Treat security work as an evidence-backed engineering review. Separate verified vulnerabilities from suspicious patterns and general hardening advice. Never claim that a scan proves a system secure.

## Set the operating mode

Choose one mode from the request:

- **Design:** define controls and acceptance criteria before implementation.
- **Review:** inspect and report; do not modify files or external systems.
- **Remediate:** implement only the fixes the user authorized, then verify them.
- **Incident support:** contain likely active exposure without revealing secrets or destroying evidence.

Default to **Review** when the user asks to audit, assess, or diagnose. A request to fix or implement authorizes in-scope repository edits, not credential rotation, account changes, history rewriting, deployment, disclosure, or other external actions.

## Establish scope and risk context

1. Identify the repository or artifact boundary, languages, frameworks, manifests, deployment model, and existing security tooling.
2. Identify trust boundaries, exposed interfaces, privileged operations, authentication paths, sensitive data, third-party services, and untrusted inputs.
3. Note exclusions and inaccessible evidence. Do not inspect secrets, unrelated private data, generated dependencies, or production systems merely because they are reachable.
4. Calibrate depth to risk. Prioritize internet-facing, privileged, multi-tenant, financial, health, education-record, identity, and safety-critical paths.
5. Read [references/review-playbook.md](references/review-playbook.md) for the control areas, severity rules, and review prompts. Read [references/language-patterns.md](references/language-patterns.md) only for languages and stacks present.
6. Read [references/standards-map.md](references/standards-map.md) when the user requests a named standard, compliance mapping, current requirements, or citations. Verify time-sensitive claims against current official sources.

## Gather evidence safely

Use read-only inspection first. Review architecture and entry points before broad pattern searches so findings have context.

Run the bundled scanner when a fast local triage is useful:

```text
python scripts/security_scan.py PATH --format markdown
```

The scanner is dependency-free, skips common generated directories and symlinks, does not use the network, and reports rule IDs and locations without printing matched values. Treat every result as a candidate requiring manual confirmation. Do not install scanners, upload code, or query external vulnerability services without authorization.

For dependencies, identify manifests and lockfiles first. Prefer the ecosystem's existing audit command when available. Distinguish:

- package is present;
- vulnerable version is resolved in a lockfile or environment;
- vulnerable code is reachable;
- exploitability is demonstrated.

Do not infer the latter states from the former.

## Review in risk order

1. **Secrets and credentials:** committed secrets, secret exposure in logs/errors/build output, excessive scope, missing rotation or revocation paths.
2. **Authorization and isolation:** object-level access checks, tenant boundaries, privilege escalation, default-deny behavior, administrative functions.
3. **Injection and unsafe interpretation:** command, SQL/NoSQL, template, path, deserialization, SSRF, XSS, and dynamic code execution.
4. **Authentication and session security:** password handling, MFA for privileged access, token validation, cookie properties, replay and reset flows.
5. **Data protection:** collection minimization, encryption in transit and at rest where required, key handling, retention, deletion, backups, and sensitive logging.
6. **Supply chain and build:** resolved dependencies, provenance, lockfiles, build permissions, CI secret exposure, untrusted pull-request execution, artifact integrity.
7. **Configuration and operations:** secure defaults, debug exposure, TLS verification, CORS, headers, rate limits, observability, recovery, and patch processes.
8. **Business logic and abuse:** invariants, concurrency, quotas, enumeration, workflow bypass, and costly or irreversible operations.

Trace each candidate from attacker-controlled source to sensitive sink and then inspect guards. Confirm runtime context before assigning severity.

## Classify findings

Use these statuses:

- **Confirmed:** vulnerable behavior is supported by code/configuration and a plausible attack path.
- **Likely:** strong evidence exists, but one environmental or runtime fact is missing.
- **Needs verification:** suspicious pattern without enough context.
- **Hardening:** defense-in-depth improvement without a demonstrated vulnerability.
- **Not applicable / false positive:** evidence shows the candidate does not create the stated risk.

Rate severity by realistic impact and exploitability, not by pattern name alone:

- **Critical:** likely immediate compromise, active secret exposure, unauthenticated remote code execution, or broad sensitive-data loss.
- **High:** practical major confidentiality, integrity, availability, or privilege impact.
- **Medium:** bounded impact, meaningful preconditions, or a material control weakness.
- **Low:** limited impact or defense-in-depth with a concrete security benefit.

State assumptions and confidence. Do not attach a CVSS score unless enough inputs are known and the user needs it.

## Report contract

Lead with the security posture and urgent actions. For each finding provide:

`ID | Severity | Confidence | Status | Control area | File/condition | Evidence | Attack path | Impact | Recommended fix | Verification`

Keep evidence minimal and redact credentials, tokens, personal data, and exploit payloads. Include:

1. scope and exclusions;
2. prioritized findings;
3. hardening recommendations, clearly separated;
4. tests and commands run;
5. unknowns and residual risk;
6. disposition: `Ready`, `Ready with conditions`, or `Not ready` when a release decision was requested.

If there are no confirmed findings, say **No confirmed findings in the reviewed scope** rather than **secure**.

## Remediate with approval boundaries

1. Fix the root cause with the smallest coherent change.
2. Preserve compatibility unless the insecure behavior must fail closed; explain consequential behavior changes.
3. Add a regression test that demonstrates the security boundary without embedding a real secret or harmful payload.
4. Prefer parameterized APIs, allowlists, safe parsers, least privilege, short-lived credentials, and secure framework defaults over custom sanitizers or denylist regexes.
5. Re-run focused tests, the relevant scanner or audit, and the changed-path review.
6. Report what changed and remaining risks. Do not silently suppress a scanner rule to make the report pass.

Require explicit approval before rotating or revoking credentials, changing accounts or access policies, publishing a vulnerability, contacting a third party, deploying, deleting data, rewriting version-control history, or force-pushing.

## Handle suspected incidents

If a live secret, active exploitation, or data exposure is suspected:

1. Do not repeat the secret or sensitive evidence in output.
2. State what appears exposed, where it was found, and the confidence level.
3. Recommend immediate revocation or rotation through the credential owner; perform it only with explicit authority.
4. Preserve relevant logs and timestamps. Avoid commands that rewrite history or erase evidence.
5. Contain before cleaning history. Removing a value from a current file does not invalidate it or remove it from prior commits, caches, logs, or artifacts.
6. Escalate through the project's documented private security channel. Do not invent contacts or use public issues for suspected vulnerabilities.

## Completion criteria

Finish only when scope and exclusions are stated, every reported issue has evidence and a disposition, authorized fixes have focused verification, sensitive values remain redacted, and unresolved risks or required owner actions are explicit.
