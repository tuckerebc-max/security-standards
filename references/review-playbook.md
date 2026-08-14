# Security review playbook

## Contents

- Review strategy
- Control prompts
- Severity calibration
- Evidence standards
- Remediation priorities

## Review strategy

Build a small system model before searching for defects: actors, assets, entry points, trust boundaries, privileged operations, data stores, third parties, and deployment boundaries. Review the highest-impact paths end to end. A pattern match without a reachable path is not a confirmed vulnerability.

Use this evidence ladder:

1. configuration or code pattern;
2. attacker-controlled source;
3. data/control flow to a sensitive sink;
4. missing or ineffective guard;
5. reachable runtime path;
6. demonstrated security impact.

Report the highest supported rung and name the missing evidence.

## Control prompts

### Secrets and credentials

- Are credentials stored outside source and delivered through an approved secret store or protected runtime configuration?
- Can secrets appear in errors, logs, traces, crash dumps, URLs, command arguments, client bundles, CI output, or test fixtures?
- Are credentials short-lived, scoped, auditable, rotatable, and revocable?
- If a secret is found, has it been validated as live without exposing it? Do not test a credential against a service without authority.

### Authentication and sessions

- Are password hashes produced by a purpose-built adaptive password hashing function with current project-approved parameters?
- Are token signature, algorithm, issuer, audience, expiry, and intended use validated?
- Are session identifiers rotated after authentication and privilege changes, invalidated at logout when required, and protected in transport/storage?
- Do account recovery, invitation, and MFA fallback resist enumeration, replay, and takeover?

### Authorization and tenancy

- Is access checked server-side for every object and action, including indirect identifiers and batch endpoints?
- Do administrative paths require explicit privileges and recent/strong authentication where appropriate?
- Are tenant identifiers derived from trusted identity context rather than accepted from the client without verification?
- Do background jobs, exports, caches, and search indexes preserve the same isolation rules?

### Input, interpretation, and output

- Is untrusted data passed through parameterized or structured APIs rather than assembled as code, commands, queries, markup, or paths?
- Are uploaded files constrained by size, type, storage location, naming, processing behavior, and retrieval authorization?
- Are URLs and network destinations constrained against SSRF, redirects, alternate IP forms, and internal metadata services?
- Is output encoded for its actual context? Sanitization and validation are not interchangeable with contextual encoding.

### Data protection and privacy

- Is sensitive data necessary, classified, access-controlled, encrypted where required, and retained only as long as needed?
- Are logs structured to omit or mask secrets and regulated identifiers?
- Are backups, exports, analytics, support tools, and lower environments covered by equivalent controls?
- Are deletion and incident-response processes operational rather than only documented?

### Supply chain and CI/CD

- Is the resolved dependency graph reproducible from lockfiles or equivalent controls?
- Are update decisions based on supported versions and current advisories rather than arbitrary pinning?
- Can untrusted pull requests or build scripts access secrets, privileged runners, package publication, or deployment credentials?
- Are build artifacts traceable to reviewed source and protected against unauthorized replacement?

### Configuration and operations

- Are production debug endpoints, verbose errors, directory listings, sample accounts, and default credentials disabled?
- Is certificate verification enabled and are insecure protocol fallbacks rejected?
- Are CORS, CSP, cookie flags, proxy trust, host validation, and security headers aligned with deployment architecture?
- Are rate limits and abuse controls applied to costly, sensitive, and anonymous operations?
- Can alerts, backups, restoration, key rotation, and patching be tested?

### Business logic

- Can steps be skipped, replayed, reordered, raced, duplicated, or performed under a different identity?
- Are quantities, ownership, approvals, state transitions, and irreversible effects enforced atomically on the server?
- Can identifiers or error differences enable enumeration?
- Are expensive operations bounded by user, tenant, origin, and global limits as needed?

## Severity calibration

Use environment-specific impact and exploitability. Increase priority for unauthenticated reachability, internet exposure, low complexity, broad tenant impact, privileged execution, sensitive data, weak detection, and difficult recovery. Reduce priority for strong preconditions, isolated non-production context, unreachable code, compensating controls, or negligible impact.

Do not downgrade a confirmed vulnerability solely because a scanner did not detect it. Do not upgrade a candidate solely because a tool labels it critical.

## Evidence standards

- Cite the smallest useful file and line/condition.
- Describe data flow and missing guard in plain language.
- Redact matched values; use rule names, hashes, or last four characters only when essential and safe.
- Distinguish source review, configuration review, dependency advisory, dynamic test, and inference.
- Avoid destructive proof. Use a harmless test value and the least privileged environment available.

## Remediation priorities

Order work by risk reduction and dependency:

1. contain active exposure and revoke compromised credentials;
2. block exploitable paths and privilege bypasses;
3. correct the vulnerable primitive or trust decision;
4. add regression tests and monitoring;
5. address defense-in-depth and process improvements.

Security fixes should fail safely, remain observable, and avoid creating a second parser, secret store, authentication system, or cryptographic design when a maintained platform facility exists.
