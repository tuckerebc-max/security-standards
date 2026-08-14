# Language and stack patterns

Read only the sections relevant to the project. These are review prompts, not automatic findings.

## Python

- Prefer `subprocess` argument arrays with `shell=False`; validate executable choice and untrusted arguments. Timeouts limit hangs but do not prevent injection.
- Resolve user-influenced paths against an allowed root and verify containment. Handle symlinks and platform case rules explicitly. String checks for `..` are insufficient.
- Avoid `eval`, `exec`, unsafe `pickle`, and unsafe YAML/object deserialization for untrusted data.
- Use database-driver parameters for values. Identifiers require a strict allowlist or driver-supported identifier composition.
- Do not disable TLS verification or suppress certificate warnings as a fix.
- Use `secrets`, not `random`, for security tokens. Use maintained cryptographic libraries and project-approved algorithms.
- Return generic client errors while retaining redacted diagnostic context in protected logs.

## JavaScript and TypeScript

- Avoid dynamic code evaluation and string-based process execution with untrusted data. Prefer `spawn`/`execFile` argument arrays and a fixed executable.
- Treat template literals in SQL, shell, HTML, and URLs as context-sensitive sinks; use parameterized or structured APIs.
- Prevent prototype pollution when recursively merging or assigning attacker-controlled object keys.
- Validate authorization on the server; client-side route guards and hidden UI controls are not enforcement.
- Keep tokens out of URLs and browser storage when exposure to script execution would be unacceptable. Prefer secure, HttpOnly, SameSite cookies when the architecture supports them and address CSRF accordingly.
- Constrain redirect and fetch destinations; parse URLs with a trusted parser and validate the final destination after redirects and DNS resolution where relevant.

## Web applications and APIs

- Apply contextual output encoding. Use a maintained sanitizer only when the product intentionally accepts HTML.
- Enforce object- and function-level authorization on each request.
- Validate content type, size, schema, and semantic bounds; reject unknown fields when ambiguity creates risk.
- Configure cookies, CORS, CSP, host/proxy trust, and cache behavior for the actual deployment topology.
- Protect state-changing browser requests from CSRF when ambient credentials are used.
- Rate-limit authentication, recovery, enumeration, expensive search/export, and resource-creation paths.
- Avoid placing secrets or personal data in URLs, analytics events, or client-visible error details.

## SQL and data stores

- Parameterize values. Do not build queries with concatenation, interpolation, or escaping alone.
- Allowlist dynamic table, column, order, or operator choices; parameters generally cannot represent identifiers.
- Use a least-privileged database principal and separate migration/administrative permissions from runtime permissions.
- Make authorization and tenant filters unavoidable, including joins, aggregates, exports, and background jobs.
- Review NoSQL operator injection, query selector injection, and mass assignment; schema validation alone may not neutralize query semantics.

## Shell and automation

- Quote is not a universal defense. Prefer direct process APIs or fixed commands with argument arrays.
- Do not evaluate user-controlled strings, source untrusted files, or expand untrusted glob/options.
- Treat filenames beginning with `-`, newline-containing values, environment inheritance, temporary-file races, and PATH lookup as security concerns.
- Use least-privileged CI tokens, separate trusted and untrusted workflows, and prevent forked code from accessing protected secrets.
- Never print secret-bearing environment variables or enable command tracing around secrets.

## Infrastructure and containers

- Avoid privileged containers, host namespace sharing, writable host mounts, and unnecessary Linux capabilities.
- Run as a non-root identity where feasible; use read-only filesystems and explicit writable paths.
- Pin deployable artifacts by immutable digest when provenance matters; update through a controlled process rather than freezing old versions indefinitely.
- Keep secrets out of images, build arguments, layers, state files, and public outputs.
- Restrict cloud IAM by action, resource, condition, and lifetime; test denial paths.

## Cryptography

- Do not design custom cryptographic protocols.
- Use authenticated encryption for confidentiality plus integrity, unique nonces as required by the selected construction, and a managed key lifecycle.
- Store passwords with a purpose-built adaptive password hashing function, not a fast general-purpose hash.
- Verify signatures and tokens with fixed acceptable algorithms and required claims; do not trust header-selected algorithms or keys without policy validation.
- Treat algorithm and parameter recommendations as time-sensitive; verify them against current official guidance and project constraints.
