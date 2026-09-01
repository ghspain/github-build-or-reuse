# Reproducible README demo

The README demo is generated from one auditable source of truth rather than maintained as unrelated artwork and terminal output.

## Source of truth

`assets/demo.json` stores a dated evidence snapshot:

- the user requirement;
- the public GitHub candidate used in the example;
- license and activity evidence checked at that date;
- the capabilities verified from public repository evidence;
- the resulting `USE`, `CONTRIBUTE`, `FORK`, or `BUILD` verdict;
- confidence, rationale and the next reversible action.

The current scenario reuses the existing worked example in `skills/github-build-or-reuse/examples/presentation-generator.md`. On 2026-09-01, public GitHub repository metadata and the repository README for `presenton/presenton` were checked for the narrower demo requirements: self-hosting, editable PPTX output, multiple LLM providers and a presentation-generation API.

A snapshot is intentionally not presented as permanent truth. Refresh the evidence before changing its date or claims.

## Generate the tracked assets

The generator uses only the Python standard library:

```bash
python scripts/generate_demo.py
```

It deterministically creates:

- `assets/demo.svg` — the static README visual;
- `assets/demo.cast` — an asciicast v2 terminal recording.

CI runs:

```bash
python scripts/generate_demo.py --check
```

so a change to `demo.json` cannot be merged while the visible assets are stale.

## Replay the terminal demo

With Asciinema installed:

```bash
asciinema play assets/demo.cast
```

## Render an animated GIF

Do not build a custom terminal-to-GIF renderer. Reuse the official [`asciinema/agg`](https://github.com/asciinema/agg) project:

```bash
agg --theme github-dark --font-size 16 assets/demo.cast assets/demo.gif
```

The repository render workflow pins an `agg` release and verifies the downloaded binary checksum before rendering. The GIF is a presentation artifact; `demo.json` remains the evidence source of truth.

## Refreshing the evidence

1. Re-run the skill against the same scenario using current GitHub evidence.
2. Verify every consequential claim directly from repository metadata/files; do not copy old star counts or README marketing blindly.
3. Update `assets/demo.json`, including `checked_at` and any changed evidence.
4. Run `python scripts/generate_demo.py`.
5. Render the GIF with `agg` when the visual recording changed.
6. Run `python scripts/validate.py` and `python scripts/generate_demo.py --check` before opening the pull request.

If the current candidate no longer clears the requirements, change the verdict or candidate. The demo should demonstrate the skill's decision process, not preserve a preferred outcome.
