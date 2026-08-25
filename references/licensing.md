# License triage

This is engineering triage, not legal advice. Verify the repository's actual license text and the intended use/distribution model before making consequential licensing decisions.

## Practical first pass

- **MIT / BSD / ISC:** generally permissive; preserve required notices and confirm bundled dependencies separately.
- **Apache-2.0:** permissive with explicit patent provisions and notice requirements; inspect `NOTICE` where present.
- **MPL-2.0:** file-level copyleft; can be compatible with proprietary larger works under conditions, but modifications to covered files carry obligations.
- **GPL:** strong copyleft generally matters when distributing derivative/combined works; exact boundary questions can be fact-specific.
- **AGPL:** adds network-interaction/source obligations beyond ordinary GPL distribution scenarios; SaaS use needs deliberate review.
- **LGPL:** weaker copyleft focused on the covered library, with linking/modification conditions that depend on usage.
- **SSPL / BUSL / Commons Clause / custom licenses:** do not assume they are OSI open-source or suitable for commercial hosted use.
- **No license:** public source code is not automatically permission to copy, modify, or distribute.

## Dependency licenses

A permissive top-level license does not guarantee all vendored code, assets, models, datasets, fonts, plugins, or dependencies have equivalent rights. Deep diligence should inspect the dependency graph and non-code assets.

## Decision gates

Record license as:

- `PASS` — intended use is clearly compatible based on verified license evidence.
- `FAIL` — known incompatibility with the intended distribution/use model.
- `UNKNOWN` — custom terms, unclear derivation/linking boundary, missing license, or legal interpretation required.

Never turn `UNKNOWN` into `PASS` to improve a candidate's score.
