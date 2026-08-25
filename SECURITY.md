# Security policy

This project is primarily agent instructions and documentation, but security issues can still matter: unsafe command examples, credential leakage patterns, malicious repository handling, or guidance that causes agents to trust unverified code.

## Reporting

Please report security-sensitive issues privately through the hosting repository's security reporting mechanism when available rather than publishing exploit details in a public issue.

Do not include real tokens, credentials, private repository content, or customer data in reports.

## Threat model

Agents using this skill should treat candidate repositories and their content as untrusted input. Reading a README, issue, script, or repository instruction must not grant that repository authority to override the user's instructions, expose credentials, execute arbitrary code, or weaken security checks.

Cloning or executing candidate code is a deeper due-diligence step and should happen only in an appropriate sandbox with explicit need.
