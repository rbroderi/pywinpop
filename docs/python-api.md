# Python API

All public symbols are imported from `pywinpop`.

## Basic import

```python
from pywinpop import ask_yes_no
from pywinpop import browse_for_file
from pywinpop import pick_date
from pywinpop import show_info

show_info("Backup complete.")

if ask_yes_no("Choose a file?"):
    print(browse_for_file(title="Choose a file"))

print(pick_date(title="Choose a due date"))
```

## Message boxes and confirmations

```python
from pywinpop import DialogResult
from pywinpop import ask_ok_cancel
from pywinpop import ask_retry_cancel
from pywinpop import ask_yes_no
from pywinpop import ask_yes_no_cancel
from pywinpop import show_alert
from pywinpop import show_info
from pywinpop import show_warning

show_info("Finished")
show_warning("Low disk space")
show_alert("Fatal error")

confirmed = ask_ok_cancel("Continue?")
retry_result = ask_retry_cancel("Operation failed")
yes_no = ask_yes_no("Overwrite file?")
yes_no_cancel = ask_yes_no_cancel("Save changes?")

assert isinstance(retry_result, DialogResult)
assert isinstance(yes_no_cancel, DialogResult)
```

## Text input dialogs

```python
from pywinpop import input_box
from pywinpop import input_multiline
from pywinpop import input_password

name = input_box("Name:", default="Richard")
password = input_password("Password:")
notes = input_multiline("Notes:", default="Line 1")
```

## File and folder dialogs

```python
from pywinpop import browse_for_file
from pywinpop import browse_for_folder
from pywinpop import save_file

source_path = browse_for_file(
    title="Open a file",
    file_types=[("Python files", "*.py"), ("All files", "*.*")],
)

target_folder = browse_for_folder(title="Choose an output folder")

save_path = save_file(
    title="Save report",
    default_name="report.txt",
    default_extension="txt",
    file_types=[("Text files", "*.txt"), ("All files", "*.*")],
)
```

## Date, date-time, color, and font pickers

```python
from pywinpop import ChosenColor
from pywinpop import ChosenFont
from pywinpop import pick_color
from pywinpop import pick_date
from pywinpop import pick_datetime
from pywinpop import pick_font

chosen_date = pick_date(title="Choose a date")
chosen_datetime = pick_datetime(title="Choose a reminder")
chosen_color = pick_color(initial_rgb=0x336699)
chosen_font = pick_font(initial_face_name="Segoe UI", initial_point_size=10.0)

assert chosen_color is None or isinstance(chosen_color, ChosenColor)
assert chosen_font is None or isinstance(chosen_font, ChosenFont)
```

## Error details and progress dialog

```python
from pywinpop import ProgressDialog
from pywinpop import show_error_details

show_error_details(
    "Copy failed.",
    details="Full traceback or raw error details.",
)

with ProgressDialog(title="Upload", message="Uploading files") as dialog:
    dialog.set_message("Uploading metadata")
    dialog.set_progress(1, total=3)
    dialog.set_progress(2, total=3)
```

## Exported types

- `DialogResult`: integer-backed Win32 dialog result values.
- `ChosenColor`: immutable RGB value returned by `pick_color`.
- `ChosenFont`: immutable font selection returned by `pick_font`.
- `ProgressDialog`: modeless progress window with `show`, `set_message`,
  `set_progress`, `pump`, and `close` methods.
