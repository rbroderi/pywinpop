from __future__ import annotations

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


def main() -> int:
    show_info("This is an information popup.", title="pywinpop Example")
    show_warning("This is a warning popup.", title="pywinpop Example")
    show_alert("This is an alert popup.", title="pywinpop Example")

    wants_to_continue = ask_yes_no(
        "Do you want to continue to the next popup?",
        title="pywinpop Example",
    )
    print(f"ask_yes_no -> {wants_to_continue}")

    confirmed = ask_ok_cancel(
        "Do you want to open the input and picker dialogs?",
        title="pywinpop Example",
    )
    print(f"ask_ok_cancel -> {confirmed}")
    if not confirmed:
        return 0

    name = input_box(
        "Enter your name:",
        title="pywinpop Example",
        default="Richard",
    )
    print(f"input_box -> {name!r}")

    password = input_password("Enter your password:", title="pywinpop Example")
    print(f"input_password -> {password!r}")

    notes = input_multiline(
        "Enter some notes:",
        title="pywinpop Example",
        default="Line 1",
    )
    print(f"input_multiline -> {notes!r}")

    selected_file = browse_for_file(
        title="Choose a file",
        file_types=[("Python files", "*.py"), ("All files", "*.*")],
    )
    print(f"browse_for_file -> {selected_file}")

    selected_folder = browse_for_folder(title="Choose a folder")
    print(f"browse_for_folder -> {selected_folder}")

    selected_date = pick_date(title="Choose a date")
    print(f"pick_date -> {selected_date!r}")

    selected_datetime = pick_datetime(title="Choose a date and time")
    print(f"pick_datetime -> {selected_datetime!r}")

    selected_color = pick_color(initial_rgb=0x336699)
    print(f"pick_color -> {selected_color!r}")

    selected_font = pick_font(initial_face_name="Segoe UI", initial_point_size=10.0)
    print(f"pick_font -> {selected_font!r}")

    show_error_details(
        "Example error dialog.",
        details="Extra details go here.",
        title="pywinpop Example",
    )

    with ProgressDialog(title="pywinpop Example", message="Working") as dialog:
        dialog.set_progress(1, total=3)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
