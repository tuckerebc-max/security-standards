# Standards and source map

Use standards as verification and communication aids, not as substitutes for threat modeling or system-specific evidence. Verify current versions and requirement text at the official source before making a compliance claim.

## Primary references

- [OWASP Application Security Verification Standard](https://owasp.org/www-project-application-security-verification-standard/): detailed application-security verification requirements. Select a target ASVS level with the system owner; do not imply certification from an informal review.
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/): implementation guidance for focused topics such as authentication, authorization, secrets, input handling, logging, and dependency management.
- [NIST SP 800-218, Secure Software Development Framework](https://csrc.nist.gov/pubs/sp/800/218/final): organization- and lifecycle-level secure software development practices.
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework): governance and cybersecurity risk-management outcomes.
- [CISA Secure by Design](https://www.cisa.gov/securebydesign): product principles that place responsibility for customer security outcomes on software producers.
- [MITRE CWE](https://cwe.mitre.org/): weakness taxonomy. Use a CWE identifier only after confirming the described weakness matches the finding.
- [FIRST CVSS](https://www.first.org/cvss/): severity scoring method. Do not invent environmental inputs or use a score as a replacement for remediation priority.

## Practical mapping

| Review area | Useful reference families |
|---|---|
| Secure development process and governance | NIST SSDF, NIST CSF, CISA Secure by Design |
| Application control verification | OWASP ASVS, OWASP Cheat Sheets |
| Weakness classification | MITRE CWE |
| Severity communication | FIRST CVSS plus system-specific impact |
| Secrets lifecycle | OWASP Secrets Management Cheat Sheet, platform owner documentation |
| Dependency and build security | NIST SSDF, ecosystem and vendor advisories |

## Compliance boundary

Do not state that a repository, application, or organization is compliant based solely on source inspection. Name the exact artifact, version, requirement subset, evidence reviewed, testing method, exclusions, and assessor limitations. Record `meets`, `partially meets`, `does not meet`, or `not assessed` for each mapped requirement.

## Adaptation provenance

This skill was inspired by Alireza Rezvani's [`security-standards.md`](https://github.com/alirezarezvani/claude-skills/blob/main/standards/security/security-standards.md). The operational workflow, safety boundaries, evidence model, incident handling, language coverage, and reporting contract here are a substantial rewrite for Codex. The upstream document should be treated as background material, not as authoritative or executable instructions.
