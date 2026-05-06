import importlib

from pywinpop import ChosenColor
from pywinpop import ChosenFont
from pywinpop import DialogResult
from pywinpop import ProgressDialog


def test_package_importable() -> None:
    module = importlib.import_module("pywinpop")
    assert module is not None


def test_public_api_exports_expected_symbols() -> None:
    module = importlib.import_module("pywinpop")
    assert module.DialogResult is DialogResult
    assert callable(module.show_alert)
    assert callable(module.show_warning)
    assert callable(module.show_info)
    assert callable(module.ask_yes_no)
    assert callable(module.ask_ok_cancel)
    assert callable(module.ask_yes_no_cancel)
    assert callable(module.ask_retry_cancel)
    assert callable(module.input_box)
    assert callable(module.input_password)
    assert callable(module.input_multiline)
    assert callable(module.browse_for_file)
    assert callable(module.browse_for_folder)
    assert callable(module.save_file)
    assert callable(module.pick_color)
    assert callable(module.pick_date)
    assert callable(module.pick_datetime)
    assert callable(module.pick_font)
    assert callable(module.show_error_details)
    assert callable(module.ProgressDialog)


def test_dialog_result_matches_win32_ids() -> None:
    assert int(DialogResult.OK) == 1
    assert int(DialogResult.CANCEL) == 2
    assert int(DialogResult.RETRY) == 4
    assert int(DialogResult.YES) == 6
    assert int(DialogResult.NO) == 7


def test_picker_result_types_are_importable() -> None:
    assert ChosenColor(red=1, green=2, blue=3, rgb=0x030201).rgb == 0x030201
    font = ChosenFont(
        face_name="Segoe UI",
        point_size=9.0,
        weight=400,
        italic=False,
        underline=False,
        strike_out=False,
        color=ChosenColor(red=0, green=0, blue=0, rgb=0),
    )
    assert font.face_name == "Segoe UI"


def test_progress_dialog_state_is_constructible() -> None:
    dialog = ProgressDialog(title="Progress", message="Working", status="Starting")
    dialog.set_progress(1, total=4)
    assert dialog.status == "1 of 4 (25%)"
