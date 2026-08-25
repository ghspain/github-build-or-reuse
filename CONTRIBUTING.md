# Contributing

Contributions that improve evidence quality, decision logic, portability, or examples are welcome.

## Before opening a change

1. Keep the main `SKILL.md` focused on runtime behavior.
2. Put detailed guidance under `references/` and worked scenarios under `examples/`.
3. Verify any GitHub CLI/API syntax against current official documentation.
4. Avoid adding product-specific assumptions unless they are framed as optional evidence.
5. Do not weaken hard gates simply to produce a recommendation.
6. Run `python scripts/validate.py`.

## Pull requests

Explain:

- the decision failure or evidence gap being addressed;
- why the change belongs in the runtime skill versus supporting references;
- whether scoring/verdict behavior changes;
- how the change was validated.

Do not include secrets, private repository data, customer details, or copied proprietary prompts.
