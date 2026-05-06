# pywinpop

Windows popup helpers built with ctypes.

## Features

- info, warning, and alert message boxes
- yes/no, yes/no/cancel, ok/cancel, and retry/cancel confirmations
- single-line, password, and multiline text input dialogs
- open file, save file, Explorer-style folder dialogs, plus date and
  date-time pickers
- native color and font pickers
- error/details dialog and a lightweight progress dialog object
- value/result types for dialog results, colors, and fonts

## Install

```bash
pip install pywinpop
```

For local development in this repository:

```bash
uv sync
```

## Public API

The package exports these public symbols from `pywinpop` directly.

### Message boxes and confirmation dialogs

- `show_info(message, title="Information") -> DialogResult`
- `show_warning(message, title="Warning") -> DialogResult`
- `show_alert(message, title="Alert") -> DialogResult`
- `ask_yes_no(message, title="Question") -> bool`
- `ask_ok_cancel(message, title="Confirm") -> bool`
- `ask_yes_no_cancel(message, title="Question") -> DialogResult`
- `ask_retry_cancel(message, title="Retry") -> DialogResult`

### File, folder, and value pickers

- `browse_for_file(...) -> Path | None`
- `save_file(...) -> Path | None`
- `browse_for_folder(title="Select a folder") -> Path | None`
- `pick_date(...) -> date | None`
- `pick_datetime(...) -> datetime | None`
- `pick_color(initial_rgb=0x000000) -> ChosenColor | None`
- `pick_font(...) -> ChosenFont | None`

### Custom dialogs

- `input_box(...) -> str | None`
- `input_password(...) -> str | None`
- `input_multiline(...) -> str | None`
- `show_error_details(message, *, details, title="Error Details")   -> DialogResult`
- `ProgressDialog(...)`

### Exported types

- `DialogResult`
- `ChosenColor`
- `ChosenFont`
- `ProgressDialog`

## Example

```python
from pywinpop import ProgressDialog
from pywinpop import ask_ok_cancel
from pywinpop import ask_yes_no
from pywinpop import browse_for_file
from pywinpop import browse_for_folder
from pywinpop import input_box
from pywinpop import input_multiline
from pywinpop import input_password
from pywinpop import pick_color
from pywinpop import pick_date
from pywinpop import pick_datetime
from pywinpop import pick_font
from pywinpop import show_alert
from pywinpop import show_error_details
from pywinpop import show_info
from pywinpop import show_warning

show_info("Backup completed.")
show_warning("This action cannot be undone.")
show_alert("A fatal error occurred.")

if ask_yes_no("Do you want to continue?"):
    name = input_box("Enter your name:", default="Richard")
    password = input_password("Enter your password:")
    notes = input_multiline("Enter notes:", default="Line 1")
    chosen_file = browse_for_file(title="Select a document")
    chosen_folder = browse_for_folder(title="Select an output folder")
    chosen_date = pick_date(title="Select a due date")
    chosen_datetime = pick_datetime(title="Select a reminder")
    chosen_color = pick_color(initial_rgb=0x336699)
    chosen_font = pick_font(initial_face_name="Segoe UI", initial_point_size=10.0)

    if ask_ok_cancel("Show a details dialog?"):
        show_error_details(
            "The backup failed.",
            details="Raw Win32 or traceback details can go here.",
        )

    with ProgressDialog(title="Example Progress", message="Working") as dialog:
        dialog.set_progress(1, total=3)

    print(
        name,
        password,
        notes,
        chosen_file,
        chosen_folder,
        chosen_date,
        chosen_datetime,
        chosen_color,
        chosen_font,
    )
```

See `example.py` in the repository for a fuller interactive walkthrough.

## Notes

- This package is Windows-only.
- The dialogs use Win32 APIs through ctypes rather than external GUI frameworks.
- `ProgressDialog` is modeless; call `set_message`, `set_progress`, or
  `pump` during long-running work so it stays responsive.
- The folder picker uses the standard file-open dialog with Win32 control
  manipulation to present an Explorer-style folder selection flow.
