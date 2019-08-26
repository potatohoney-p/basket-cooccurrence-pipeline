# Basket Cooccurrence Pipeline

Build item cooccurrence recommendations from a disk-backed stream of synthetic basket events.

## Run locally

Use a currently supported Python 3 interpreter. No third-party packages, credentials, downloads, or network access are required.

```sh
python -m unittest discover -s tests -v
python demo.py
```

Run from the repository directory. The demo reads `examples/input.json`; inputs are reproducible, authored examples.

## Scope and behavior

Input rows are customer/item pairs with binary membership semantics: repeated purchases do not raise support. A SQL self-join computes unordered pairs, then query-time aggregation excludes already-owned items. Batching bounds Python ingestion memory, but pair construction can be quadratic in basket width and use substantial database space. No production-scale performance or recommendation quality is claimed.

## Layout

- `core.py`: primary algorithm or storage contract.
- `features.py`: pipeline or integration layer.
- `tests/`: independent behavioral assertions, failure cases, and regressions.
- `demo.py` and `examples/input.json`: repeatable end-to-end example.

## Example output

```json
{
  "coverage": {
    "customers": 3,
    "events": 5,
    "items": 3
  },
  "recommendations": [
    [
      "cake",
      1
    ],
    [
      "fruit",
      1
    ]
  ]
}
```

## Compatibility and license

The implementation uses language features and standard-library APIs available in [Python 3.4](https://docs.python.org/3.4/library/index.html), released in [March 2014](https://www.python.org/downloads/release/python-340/). Use a supported runtime; an old interpreter is not required. Compatibility with a historical runtime is not certified by current-runtime tests.

MIT licensed. No third-party source code or datasets are bundled.
