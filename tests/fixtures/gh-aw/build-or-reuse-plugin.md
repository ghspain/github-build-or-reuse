---
on: workflow_dispatch
engine: copilot
permissions:
  contents: read
plugins:
  - ghspain/github-build-or-reuse@v1.2.2
---

# Agent Plugin compile smoke test

Use the installed `github-build-or-reuse` capability only as a compilation fixture. No model execution is required by this test.
