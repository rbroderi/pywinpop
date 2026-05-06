# pywinpop

Reference documentation for `pywinpop`.

`pywinpop` provides Windows-native popups and picker dialogs using
`ctypes` and Win32 APIs.

## What it includes

- message boxes and confirmation dialogs
- text-entry dialogs for plain text, passwords, and multiline text
- file, save-file, and folder pickers
- date, date-time, color, and font pickers
- an error/details dialog
- a lightweight modeless progress dialog

## Install

```bash
pip install pywinpop
```

Or with uv:

```bash
uv add pywinpop
```

## Python entry point

Import from `pywinpop` directly:

```python
from pywinpop import ask_yes_no
from pywinpop import browse_for_file
from pywinpop import pick_date
from pywinpop import show_info

show_info("Backup completed.")

if ask_yes_no("Open a file?"):
    print(browse_for_file(title="Choose a file"))

print(pick_date(title="Pick a due date"))
```

## Python API

See [Python API](python-api.md) for the exported symbols, return types,
and usage examples.

## Development docs

```bash
# Install dependencies
uv sync

# Build docs
just docs-build

# Serve docs locally
just docs-serve
```
