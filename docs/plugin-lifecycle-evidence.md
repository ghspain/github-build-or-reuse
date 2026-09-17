# Agent Plugin lifecycle evidence

Last updated: 2026-09-17.

This document records evidence that is stronger than package conformance or install/discovery. It complements `docs/agent-plugin-compatibility.md` and issue #35.

## Evidence levels

1. **Conformance** — package/schema/path validation passes.
2. **Install/discovery verified** — a named client installs/discovers the plugin and reports it enabled/available.
3. **Lifecycle/update verified** — the supported native client lifecycle installs an older real release, discovers a newer real release, updates through the native update mechanism, preserves canonical skill identity, and supports uninstall/rollback behavior where available.
4. **Behavioral runtime verified** — a real model/session activates the skill and produces representative Build-or-Reuse behavior with sanitized evidence.

A stronger level must never be inferred from a weaker one.

## Current matrix

| Client | Install/discovery | Lifecycle/update | Behavioral runtime | Adapter decision |
| --- | --- | --- | --- | --- |
| GitHub Copilot CLI 1.0.85 | verified | **verified** across v1.2.2 -> v1.2.3 | pending | retirement candidate only; behavior still required |
| OpenAI Codex CLI 0.154.0 | verified by current CI baseline once this change passes | no native `plugin update` equivalent currently exposed | pending | keep / retirement candidate at most |
| Claude Code 2.1.263 | verified | not evaluated | not evaluated | keep |
| Gemini CLI 0.58.0 | verified | not evaluated | not evaluated | keep |
| Cursor | vendor-native support documented; repository headless install not captured | not evaluated | not evaluated | keep |
| GitHub Agentic Workflows 0.88.4 | compile/consumption verified | N/A for this client role | model execution not captured | keep as distribution/orchestration surface |

## Copilot lifecycle evidence

PR #38 / issue #37 provide the repository-owned lifecycle rehearsal.

The passing run uses GitHub Copilot CLI 1.0.85 in isolated HOME/cache state and verifies two already-published immutable releases:

```text
v1.2.2 -> 74f8cfeca5c0ed5799a0ab71be88d06fc9e2afb1
v1.2.3 -> 24af1931681bb03b0282472c4d4b6900359418c7
```

Observed sequence:

1. verify each tag resolves to the expected commit;
2. register a temporary smart-HTTP Git marketplace;
3. install v1.2.2 through the marketplace;
4. require `plugin list --json` to report v1.2.2 enabled;
5. require the installed canonical `skills/github-build-or-reuse/SKILL.md` to report v1.2.2;
6. advance the same marketplace to v1.2.3;
7. run `copilot plugin marketplace update`;
8. run native `copilot plugin update`;
9. require the client to report `v1.2.2 -> v1.2.3` and v1.2.3 enabled;
10. require the installed canonical `SKILL.md` to report v1.2.3;
11. run native uninstall and verify removal.

No model credentials, provider credentials, PATs, OAuth material, or fake releases are used.

## Codex lifecycle boundary

The current Codex CLI plugin command surface exposes install/add, list, marketplace management, and remove. Marketplace snapshots can be upgraded, but there is currently no direct native plugin-update command equivalent to Copilot's `plugin update`.

Therefore install/discovery evidence must not be promoted to lifecycle parity. In particular, `remove` followed by `add` is not treated as a substitute for an atomic/supported update mechanism merely to satisfy the retirement checklist.

## Remaining strongest gate

Issue #35 remains open until at least Copilot and Codex execute the same representative Build-or-Reuse scenario in trusted model sessions and produce sanitized behavioral evidence. Adapter removal, if any, must be a separate PR after those gates are met.
