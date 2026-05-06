import ctypes
from ctypes import wintypes
from dataclasses import dataclass
from typing import Any

from ._constants import BN_CLICKED
from ._constants import COLOR_WINDOW
from ._constants import CW_USEDEFAULT
from ._constants import DEFAULT_GUI_FONT
from ._constants import DETAILS_EDIT_ID
from ._constants import EM_SETLIMITTEXT
from ._constants import IDC_ARROW
from ._constants import INPUT_EDIT_ID
from ._constants import INPUT_PROMPT_ID
from ._constants import PM_REMOVE
from ._constants import PROGRESS_MESSAGE_ID
from ._constants import PROGRESS_STATUS_ID
from ._constants import SW_SHOW
from ._constants import ButtonStyle
from ._constants import DialogResult
from ._constants import EditStyle
from ._constants import StaticStyle
from ._constants import WindowExStyle
from ._constants import WindowMessage
from ._constants import WindowStyle
from ._win32 import MSG
from ._win32 import WNDCLASSW
from ._win32 import WndProc
from ._win32 import ensure_windows
from ._win32 import win_api


@dataclass(slots=True)
class ProgressDialog:
    title: str = "Progress"
    message: str = "Working..."
    status: str = "Starting"
    hwnd: int | None = None
    instance_handle: int | None = None
    class_name: str | None = None
    window_proc: Any = None

    def show(self) -> ProgressDialog:
        return _show_progress_dialog(self)

    def set_message(self, message: str) -> None:
        update_progress_message(self, message)

    def set_progress(self, current: int | None, *, total: int | None = None) -> None:
        update_progress_status(self, current, total=total)

    def pump(self) -> None:
        pump_progress_dialog(self)

    def close(self) -> None:
        close_progress_dialog(self)

    def __enter__(self) -> ProgressDialog:
        return self.show()

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: Any,
    ) -> None:
        del exc_type, exc, traceback
        self.close()


@dataclass(slots=True)
class _InputState:
    initial_value: str
    max_length: int
    result: str | None = None


def _run_text_entry_dialog(
    prompt: str,
    *,
    title: str,
    default: str,
    max_length: int,
    edit_style: EditStyle,
    dialog_width: int,
    dialog_height: int,
    edit_height: int,
    button_y: int,
) -> str | None:
    ensure_windows()
    api = win_api()
    state = _InputState(initial_value=default, max_length=max_length)
    instance = api.kernel32.GetModuleHandleW(None)
    class_name = f"pywinpop_input_{id(state)}"
    gui_font = api.gdi32.GetStockObject(DEFAULT_GUI_FONT)
    finished = False

    @WndProc
    def window_proc(hwnd: int, msg: int, w_param: int, l_param: int) -> int:
        nonlocal finished
        if msg == WindowMessage.COMMAND:
            command_id = w_param & 0xFFFF
            notification = (w_param >> 16) & 0xFFFF
            if command_id == DialogResult.OK and notification == BN_CLICKED:
                text_buffer = ctypes.create_unicode_buffer(state.max_length + 1)
                api.user32.GetDlgItemTextW(hwnd, INPUT_EDIT_ID, text_buffer, len(text_buffer))
                state.result = text_buffer.value
                finished = True
                api.user32.DestroyWindow(hwnd)
                return 0
            if command_id == DialogResult.CANCEL and notification == BN_CLICKED:
                finished = True
                api.user32.DestroyWindow(hwnd)
                return 0
        if msg == WindowMessage.CLOSE:
            finished = True
            api.user32.DestroyWindow(hwnd)
            return 0
        return api.user32.DefWindowProcW(hwnd, msg, w_param, l_param)

    wnd_class = WNDCLASSW()
    wnd_class.lpfnWndProc = ctypes.cast(window_proc, wintypes.LPVOID)
    wnd_class.hInstance = instance
    wnd_class.lpszClassName = class_name
    wnd_class.hCursor = api.user32.LoadCursorW(None, ctypes.cast(IDC_ARROW, wintypes.LPCWSTR))
    wnd_class.hbrBackground = wintypes.HBRUSH(COLOR_WINDOW + 1)

    atom = api.user32.RegisterClassW(ctypes.byref(wnd_class))
    if not atom:
        msg = "Failed to register the input dialog window class."
        raise OSError(msg)

    try:
        hwnd = api.user32.CreateWindowExW(
            0,
            class_name,
            title,
            int(WindowStyle.POPUP | WindowStyle.CAPTION | WindowStyle.SYSMENU),
            CW_USEDEFAULT,
            CW_USEDEFAULT,
            dialog_width,
            dialog_height,
            None,
            None,
            instance,
            None,
        )
        if not hwnd:
            msg = "Failed to create the input dialog window."
            raise OSError(msg)

        prompt_hwnd = api.user32.CreateWindowExW(
            0,
            "STATIC",
            prompt,
            int(WindowStyle.CHILD | WindowStyle.VISIBLE | StaticStyle.LEFT),
            12,
            12,
            380,
            20,
            hwnd,
            wintypes.HMENU(INPUT_PROMPT_ID),
            instance,
            None,
        )
        edit_hwnd = api.user32.CreateWindowExW(
            int(WindowExStyle.CLIENT_EDGE),
            "EDIT",
            "",
            int(WindowStyle.CHILD | WindowStyle.VISIBLE | WindowStyle.TAB_STOP | edit_style),
            12,
            40,
            dialog_width - 40,
            edit_height,
            hwnd,
            wintypes.HMENU(INPUT_EDIT_ID),
            instance,
            None,
        )
        ok_hwnd = api.user32.CreateWindowExW(
            0,
            "BUTTON",
            "OK",
            int(
                WindowStyle.CHILD
                | WindowStyle.VISIBLE
                | WindowStyle.TAB_STOP
                | WindowStyle.GROUP
                | ButtonStyle.DEF_PUSHBUTTON
            ),
            dialog_width - 216,
            button_y,
            88,
            28,
            hwnd,
            wintypes.HMENU(DialogResult.OK),
            instance,
            None,
        )
        cancel_hwnd = api.user32.CreateWindowExW(
            0,
            "BUTTON",
            "Cancel",
            int(WindowStyle.CHILD | WindowStyle.VISIBLE | WindowStyle.TAB_STOP | ButtonStyle.PUSHBUTTON),
            dialog_width - 116,
            button_y,
            88,
            28,
            hwnd,
            wintypes.HMENU(DialogResult.CANCEL),
            instance,
            None,
        )

        for control in (prompt_hwnd, edit_hwnd, ok_hwnd, cancel_hwnd):
            if gui_font and control:
                api.user32.SendMessageW(control, WindowMessage.SET_FONT, gui_font, 1)

        api.user32.SendMessageW(edit_hwnd, EM_SETLIMITTEXT, state.max_length, 0)
        api.user32.SetDlgItemTextW(hwnd, INPUT_EDIT_ID, state.initial_value)
        api.user32.ShowWindow(hwnd, SW_SHOW)
        api.user32.UpdateWindow(hwnd)
        api.user32.SetFocus(edit_hwnd)

        message = MSG()
        while not finished:
            status = api.user32.GetMessageW(ctypes.byref(message), None, 0, 0)
            if status <= 0:
                break
            api.user32.TranslateMessage(ctypes.byref(message))
            api.user32.DispatchMessageW(ctypes.byref(message))
    finally:
        api.user32.UnregisterClassW(class_name, instance)

    return state.result


def input_box(
    prompt: str,
    *,
    title: str = "Input",
    default: str = "",
    max_length: int = 1024,
) -> str | None:
    return _run_text_entry_dialog(
        prompt,
        title=title,
        default=default,
        max_length=max_length,
        edit_style=EditStyle.LEFT | EditStyle.AUTO_HSCROLL,
        dialog_width=420,
        dialog_height=170,
        edit_height=24,
        button_y=84,
    )


def input_password(
    prompt: str,
    *,
    title: str = "Password",
    default: str = "",
    max_length: int = 1024,
) -> str | None:
    return _run_text_entry_dialog(
        prompt,
        title=title,
        default=default,
        max_length=max_length,
        edit_style=EditStyle.LEFT | EditStyle.AUTO_HSCROLL | EditStyle.PASSWORD,
        dialog_width=420,
        dialog_height=170,
        edit_height=24,
        button_y=84,
    )


def input_multiline(
    prompt: str,
    *,
    title: str = "Input",
    default: str = "",
    max_length: int = 4096,
) -> str | None:
    return _run_text_entry_dialog(
        prompt,
        title=title,
        default=default,
        max_length=max_length,
        edit_style=(EditStyle.LEFT | EditStyle.MULTILINE | EditStyle.AUTO_VSCROLL | EditStyle.WANT_RETURN),
        dialog_width=520,
        dialog_height=300,
        edit_height=130,
        button_y=214,
    )


def show_error_details(
    message: str,
    *,
    details: str,
    title: str = "Error Details",
) -> DialogResult:
    ensure_windows()
    api = win_api()
    instance = api.kernel32.GetModuleHandleW(None)
    class_name = f"pywinpop_details_{id(details)}"
    gui_font = api.gdi32.GetStockObject(DEFAULT_GUI_FONT)
    finished = False

    @WndProc
    def window_proc(hwnd: int, msg: int, w_param: int, l_param: int) -> int:
        nonlocal finished
        if msg == WindowMessage.COMMAND:
            command_id = w_param & 0xFFFF
            notification = (w_param >> 16) & 0xFFFF
            if command_id == DialogResult.OK and notification == BN_CLICKED:
                finished = True
                api.user32.DestroyWindow(hwnd)
                return 0
        if msg == WindowMessage.CLOSE:
            finished = True
            api.user32.DestroyWindow(hwnd)
            return 0
        return api.user32.DefWindowProcW(hwnd, msg, w_param, l_param)

    wnd_class = WNDCLASSW()
    wnd_class.lpfnWndProc = ctypes.cast(window_proc, wintypes.LPVOID)
    wnd_class.hInstance = instance
    wnd_class.lpszClassName = class_name
    wnd_class.hCursor = api.user32.LoadCursorW(None, ctypes.cast(IDC_ARROW, wintypes.LPCWSTR))
    wnd_class.hbrBackground = wintypes.HBRUSH(COLOR_WINDOW + 1)

    atom = api.user32.RegisterClassW(ctypes.byref(wnd_class))
    if not atom:
        msg = "Failed to register the error details dialog window class."
        raise OSError(msg)

    try:
        hwnd = api.user32.CreateWindowExW(
            0,
            class_name,
            title,
            int(WindowStyle.POPUP | WindowStyle.CAPTION | WindowStyle.SYSMENU),
            CW_USEDEFAULT,
            CW_USEDEFAULT,
            620,
            360,
            None,
            None,
            instance,
            None,
        )
        if not hwnd:
            msg = "Failed to create the error details dialog window."
            raise OSError(msg)

        message_hwnd = api.user32.CreateWindowExW(
            0,
            "STATIC",
            message,
            int(WindowStyle.CHILD | WindowStyle.VISIBLE | StaticStyle.LEFT),
            12,
            12,
            580,
            44,
            hwnd,
            None,
            instance,
            None,
        )
        details_hwnd = api.user32.CreateWindowExW(
            int(WindowExStyle.CLIENT_EDGE),
            "EDIT",
            details,
            int(
                WindowStyle.CHILD
                | WindowStyle.VISIBLE
                | WindowStyle.TAB_STOP
                | WindowStyle.VSCROLL
                | EditStyle.LEFT
                | EditStyle.MULTILINE
                | EditStyle.AUTO_VSCROLL
                | EditStyle.READ_ONLY
            ),
            12,
            64,
            580,
            220,
            hwnd,
            wintypes.HMENU(DETAILS_EDIT_ID),
            instance,
            None,
        )
        ok_hwnd = api.user32.CreateWindowExW(
            0,
            "BUTTON",
            "OK",
            int(
                WindowStyle.CHILD
                | WindowStyle.VISIBLE
                | WindowStyle.TAB_STOP
                | WindowStyle.GROUP
                | ButtonStyle.DEF_PUSHBUTTON
            ),
            504,
            296,
            88,
            28,
            hwnd,
            wintypes.HMENU(DialogResult.OK),
            instance,
            None,
        )

        for control in (message_hwnd, details_hwnd, ok_hwnd):
            if gui_font and control:
                api.user32.SendMessageW(control, WindowMessage.SET_FONT, gui_font, 1)

        api.user32.ShowWindow(hwnd, SW_SHOW)
        api.user32.UpdateWindow(hwnd)
        api.user32.SetFocus(ok_hwnd)

        message_loop = MSG()
        while not finished:
            status = api.user32.GetMessageW(ctypes.byref(message_loop), None, 0, 0)
            if status <= 0:
                break
            api.user32.TranslateMessage(ctypes.byref(message_loop))
            api.user32.DispatchMessageW(ctypes.byref(message_loop))
    finally:
        api.user32.UnregisterClassW(class_name, instance)

    return DialogResult.OK


def _format_progress_status(current: int | None, total: int | None) -> str:
    if current is None:
        return "Working..."
    if total is None or total <= 0:
        return f"{current} complete"
    percent = max(0, min(100, round((current / total) * 100)))
    return f"{current} of {total} ({percent}%)"


def _pump_pending_messages() -> None:
    api = win_api()
    message = MSG()
    while api.user32.PeekMessageW(ctypes.byref(message), None, 0, 0, PM_REMOVE):
        api.user32.TranslateMessage(ctypes.byref(message))
        api.user32.DispatchMessageW(ctypes.byref(message))


def _destroy_progress_dialog(dialog: ProgressDialog) -> None:
    api = win_api()
    if dialog.hwnd:
        api.user32.DestroyWindow(dialog.hwnd)
        dialog.hwnd = None
    if dialog.class_name and dialog.instance_handle:
        api.user32.UnregisterClassW(dialog.class_name, dialog.instance_handle)
        dialog.class_name = None
        dialog.instance_handle = None
        dialog.window_proc = None


def _show_progress_dialog(dialog: ProgressDialog) -> ProgressDialog:
    if dialog.hwnd:
        dialog.pump()
        return dialog

    ensure_windows()
    api = win_api()
    instance = api.kernel32.GetModuleHandleW(None)
    class_name = f"pywinpop_progress_{id(dialog)}"
    gui_font = api.gdi32.GetStockObject(DEFAULT_GUI_FONT)

    @WndProc
    def window_proc(hwnd: int, msg: int, w_param: int, l_param: int) -> int:
        if msg == WindowMessage.CLOSE:
            _destroy_progress_dialog(dialog)
            return 0
        return api.user32.DefWindowProcW(hwnd, msg, w_param, l_param)

    wnd_class = WNDCLASSW()
    wnd_class.lpfnWndProc = ctypes.cast(window_proc, wintypes.LPVOID)
    wnd_class.hInstance = instance
    wnd_class.lpszClassName = class_name
    wnd_class.hCursor = api.user32.LoadCursorW(None, ctypes.cast(IDC_ARROW, wintypes.LPCWSTR))
    wnd_class.hbrBackground = wintypes.HBRUSH(COLOR_WINDOW + 1)

    atom = api.user32.RegisterClassW(ctypes.byref(wnd_class))
    if not atom:
        msg = "Failed to register the progress dialog window class."
        raise OSError(msg)

    hwnd = api.user32.CreateWindowExW(
        0,
        class_name,
        dialog.title,
        int(WindowStyle.POPUP | WindowStyle.CAPTION | WindowStyle.SYSMENU),
        CW_USEDEFAULT,
        CW_USEDEFAULT,
        420,
        160,
        None,
        None,
        instance,
        None,
    )
    if not hwnd:
        api.user32.UnregisterClassW(class_name, instance)
        msg = "Failed to create the progress dialog window."
        raise OSError(msg)

    message_hwnd = api.user32.CreateWindowExW(
        0,
        "STATIC",
        dialog.message,
        int(WindowStyle.CHILD | WindowStyle.VISIBLE | StaticStyle.LEFT),
        12,
        18,
        380,
        32,
        hwnd,
        wintypes.HMENU(PROGRESS_MESSAGE_ID),
        instance,
        None,
    )
    status_hwnd = api.user32.CreateWindowExW(
        0,
        "STATIC",
        dialog.status,
        int(WindowStyle.CHILD | WindowStyle.VISIBLE | StaticStyle.LEFT),
        12,
        64,
        380,
        24,
        hwnd,
        wintypes.HMENU(PROGRESS_STATUS_ID),
        instance,
        None,
    )

    for control in (message_hwnd, status_hwnd):
        if gui_font and control:
            api.user32.SendMessageW(control, WindowMessage.SET_FONT, gui_font, 1)

    dialog.hwnd = hwnd
    dialog.instance_handle = instance
    dialog.class_name = class_name
    dialog.window_proc = window_proc

    api.user32.ShowWindow(hwnd, SW_SHOW)
    api.user32.UpdateWindow(hwnd)
    dialog.pump()
    return dialog


def update_progress_message(dialog: ProgressDialog, message: str) -> None:
    dialog.show()
    dialog.message = message
    if dialog.hwnd:
        win_api().user32.SetDlgItemTextW(dialog.hwnd, PROGRESS_MESSAGE_ID, message)
    dialog.pump()


def update_progress_status(
    dialog: ProgressDialog,
    current: int | None,
    *,
    total: int | None = None,
) -> None:
    dialog.show()
    dialog.status = _format_progress_status(current, total)
    if dialog.hwnd:
        win_api().user32.SetDlgItemTextW(dialog.hwnd, PROGRESS_STATUS_ID, dialog.status)
    dialog.pump()


def pump_progress_dialog(dialog: ProgressDialog) -> None:
    if dialog.hwnd:
        _pump_pending_messages()


def close_progress_dialog(dialog: ProgressDialog) -> None:
    _destroy_progress_dialog(dialog)
    _pump_pending_messages()
