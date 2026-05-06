import ctypes
from ctypes import wintypes
from datetime import date
from datetime import datetime
from pathlib import Path

from ._constants import BN_CLICKED
from ._constants import CC_RGBINIT
from ._constants import CDM_GETFOLDERPATH
from ._constants import CDN_FILEOK
from ._constants import CDN_FOLDERCHANGE
from ._constants import CDN_INITDONE
from ._constants import CF_INITTOLOGFONTSTRUCT
from ._constants import CF_SCREENFONTS
from ._constants import COLOR_WINDOW
from ._constants import CW_USEDEFAULT
from ._constants import DATE_PICKER_CONTROL_ID
from ._constants import DATE_PICKER_PROMPT_ID
from ._constants import DATE_TIME_PICKER_TIME_ID
from ._constants import DEFAULT_GUI_FONT
from ._constants import DTM_GETSYSTEMTIME
from ._constants import DTM_SETSYSTEMTIME
from ._constants import DTS_TIMEFORMAT
from ._constants import DTS_UPDOWN
from ._constants import FILEOPEN_FILENAME_COMBO_ID
from ._constants import FILEOPEN_FILENAME_EDIT_ID
from ._constants import FILEOPEN_FILENAME_LABEL_ID
from ._constants import FILEOPEN_FILETYPE_COMBO_ID
from ._constants import FILEOPEN_FILETYPE_LABEL_ID
from ._constants import FOLDER_SENTINEL_NAME
from ._constants import GDT_VALID
from ._constants import ICC_DATE_CLASSES
from ._constants import IDC_ARROW
from ._constants import MCM_GETCURSEL
from ._constants import MCM_SETCURSEL
from ._constants import SW_HIDE
from ._constants import SW_SHOW
from ._constants import ButtonStyle
from ._constants import DialogResult
from ._constants import MessageBoxFlag
from ._constants import OpenFileNameFlag
from ._constants import StaticStyle
from ._constants import WindowMessage
from ._constants import WindowStyle
from ._models import ChosenColor
from ._models import ChosenFont
from ._win32 import CHOOSECOLORW
from ._win32 import CHOOSEFONTW
from ._win32 import INITCOMMONCONTROLSEX
from ._win32 import LOGFONTW
from ._win32 import MSG
from ._win32 import OFNOTIFYW
from ._win32 import OPENFILENAMEW
from ._win32 import SYSTEMTIME
from ._win32 import WNDCLASSW
from ._win32 import OpenFileHookProc
from ._win32 import WndProc
from ._win32 import ensure_windows
from ._win32 import win_api


def _normalize_filter(file_types: list[tuple[str, str]] | None) -> str | None:
    if not file_types:
        return None
    parts: list[str] = []
    for label, pattern in file_types:
        parts.append(label)
        parts.append(pattern)
    return "\x00".join(parts) + "\x00\x00"


def _message_box(text: str, title: str, flags: MessageBoxFlag) -> DialogResult:
    ensure_windows()
    result = win_api().user32.MessageBoxW(
        None,
        text,
        title,
        int(flags | MessageBoxFlag.SYSTEM_MODAL),
    )
    return DialogResult(result)


def show_info(message: str, title: str = "Information") -> DialogResult:
    return _message_box(message, title, MessageBoxFlag.OK | MessageBoxFlag.ICON_INFORMATION)


def show_warning(message: str, title: str = "Warning") -> DialogResult:
    return _message_box(message, title, MessageBoxFlag.OK | MessageBoxFlag.ICON_EXCLAMATION)


def show_alert(message: str, title: str = "Alert") -> DialogResult:
    return _message_box(message, title, MessageBoxFlag.OK | MessageBoxFlag.ICON_HAND)


def ask_yes_no(message: str, title: str = "Question") -> bool:
    return _message_box(message, title, MessageBoxFlag.YES_NO | MessageBoxFlag.ICON_QUESTION) is DialogResult.YES


def ask_ok_cancel(message: str, title: str = "Confirm") -> bool:
    return _message_box(message, title, MessageBoxFlag.OK_CANCEL | MessageBoxFlag.ICON_QUESTION) is DialogResult.OK


def ask_yes_no_cancel(
    message: str,
    title: str = "Question",
) -> DialogResult:
    return _message_box(
        message,
        title,
        MessageBoxFlag.YES_NO_CANCEL | MessageBoxFlag.ICON_QUESTION,
    )


def ask_retry_cancel(
    message: str,
    title: str = "Retry",
) -> DialogResult:
    return _message_box(
        message,
        title,
        MessageBoxFlag.RETRY_CANCEL | MessageBoxFlag.ICON_EXCLAMATION,
    )


def browse_for_file(
    *,
    title: str = "Select a file",
    initial_dir: str | Path | None = None,
    file_types: list[tuple[str, str]] | None = None,
) -> Path | None:
    ensure_windows()
    buffer = ctypes.create_unicode_buffer(4096)
    dialog = OPENFILENAMEW()
    dialog.lStructSize = ctypes.sizeof(OPENFILENAMEW)
    dialog.hwndOwner = None
    dialog.lpstrFilter = _normalize_filter(file_types)
    dialog.nFilterIndex = 1
    dialog.lpstrFile = ctypes.cast(buffer, wintypes.LPWSTR)
    dialog.nMaxFile = len(buffer)
    dialog.lpstrInitialDir = None if initial_dir is None else str(Path(initial_dir))
    dialog.lpstrTitle = title
    dialog.Flags = int(
        OpenFileNameFlag.EXPLORER
        | OpenFileNameFlag.FILE_MUST_EXIST
        | OpenFileNameFlag.HIDE_READ_ONLY
        | OpenFileNameFlag.NO_CHANGE_DIR
        | OpenFileNameFlag.PATH_MUST_EXIST
    )
    if not win_api().comdlg32.GetOpenFileNameW(ctypes.byref(dialog)):
        return None
    return Path(buffer.value)


def save_file(
    *,
    title: str = "Save a file",
    initial_dir: str | Path | None = None,
    default_name: str = "",
    default_extension: str | None = None,
    file_types: list[tuple[str, str]] | None = None,
) -> Path | None:
    ensure_windows()
    buffer = ctypes.create_unicode_buffer(4096)
    if default_name:
        buffer.value = default_name
    dialog = OPENFILENAMEW()
    dialog.lStructSize = ctypes.sizeof(OPENFILENAMEW)
    dialog.hwndOwner = None
    dialog.lpstrFilter = _normalize_filter(file_types)
    dialog.nFilterIndex = 1
    dialog.lpstrFile = ctypes.cast(buffer, wintypes.LPWSTR)
    dialog.nMaxFile = len(buffer)
    dialog.lpstrInitialDir = None if initial_dir is None else str(Path(initial_dir))
    dialog.lpstrTitle = title
    dialog.lpstrDefExt = default_extension
    dialog.Flags = int(
        OpenFileNameFlag.EXPLORER
        | OpenFileNameFlag.HIDE_READ_ONLY
        | OpenFileNameFlag.NO_CHANGE_DIR
        | OpenFileNameFlag.PATH_MUST_EXIST
        | OpenFileNameFlag.OVERWRITE_PROMPT
    )
    if not win_api().comdlg32.GetSaveFileNameW(ctypes.byref(dialog)):
        return None
    return Path(buffer.value)


def pick_color(*, initial_rgb: int = 0x000000) -> ChosenColor | None:
    ensure_windows()
    custom_colors = (wintypes.DWORD * 16)()
    dialog = CHOOSECOLORW()
    dialog.lStructSize = ctypes.sizeof(CHOOSECOLORW)
    dialog.hwndOwner = None
    dialog.rgbResult = initial_rgb
    dialog.lpCustColors = custom_colors
    dialog.Flags = CC_RGBINIT
    if not win_api().comdlg32.ChooseColorW(ctypes.byref(dialog)):
        return None
    rgb = int(dialog.rgbResult)
    return ChosenColor(
        red=rgb & 0xFF,
        green=(rgb >> 8) & 0xFF,
        blue=(rgb >> 16) & 0xFF,
        rgb=rgb,
    )


def pick_font(
    *,
    initial_face_name: str = "Segoe UI",
    initial_point_size: float = 9.0,
) -> ChosenFont | None:
    ensure_windows()
    log_font = LOGFONTW()
    log_font.lfFaceName = initial_face_name
    dialog = CHOOSEFONTW()
    dialog.lStructSize = ctypes.sizeof(CHOOSEFONTW)
    dialog.hwndOwner = None
    dialog.lpLogFont = ctypes.pointer(log_font)
    dialog.iPointSize = int(initial_point_size * 10)
    dialog.Flags = CF_SCREENFONTS | CF_INITTOLOGFONTSTRUCT
    if not win_api().comdlg32.ChooseFontW(ctypes.byref(dialog)):
        return None
    color = ChosenColor(
        red=int(dialog.rgbColors) & 0xFF,
        green=(int(dialog.rgbColors) >> 8) & 0xFF,
        blue=(int(dialog.rgbColors) >> 16) & 0xFF,
        rgb=int(dialog.rgbColors),
    )
    return ChosenFont(
        face_name=log_font.lfFaceName.rstrip("\x00"),
        point_size=dialog.iPointSize / 10.0,
        weight=int(log_font.lfWeight),
        italic=bool(log_font.lfItalic),
        underline=bool(log_font.lfUnderline),
        strike_out=bool(log_font.lfStrikeOut),
        color=color,
    )


def browse_for_folder(*, title: str = "Select a folder") -> Path | None:
    ensure_windows()
    api = win_api()
    selected_folder: Path | None = None
    file_buffer = ctypes.create_unicode_buffer(4096)
    file_buffer.value = FOLDER_SENTINEL_NAME
    hidden_filter = _normalize_filter([("Folders", "*.pywinpop-folder-picker-no-match")])

    def sync_folder_state(parent_hwnd: int) -> None:
        nonlocal selected_folder
        folder_buffer = ctypes.create_unicode_buffer(4096)
        api.user32.SendMessageW(
            parent_hwnd,
            CDM_GETFOLDERPATH,
            len(folder_buffer),
            ctypes.addressof(folder_buffer),
        )
        api.user32.SetDlgItemTextW(
            parent_hwnd,
            FILEOPEN_FILENAME_EDIT_ID,
            FOLDER_SENTINEL_NAME,
        )
        if folder_buffer.value:
            selected_folder = Path(folder_buffer.value)

    @OpenFileHookProc
    def hook_proc(hwnd: int, msg: int, _w_param: int, l_param: int) -> int:
        if msg == WindowMessage.INITDIALOG:
            parent_hwnd = api.user32.GetParent(hwnd)
            for control_id in (
                FILEOPEN_FILETYPE_LABEL_ID,
                FILEOPEN_FILETYPE_COMBO_ID,
                FILEOPEN_FILENAME_LABEL_ID,
                FILEOPEN_FILENAME_COMBO_ID,
            ):
                control = api.user32.GetDlgItem(parent_hwnd, control_id)
                if control:
                    api.user32.ShowWindow(control, SW_HIDE)
            sync_folder_state(parent_hwnd)
            return 0
        if msg == WindowMessage.COMMAND:
            return 0
        if msg == 0x004E:
            notify = ctypes.cast(l_param, ctypes.POINTER(OFNOTIFYW)).contents
            parent_hwnd = api.user32.GetParent(hwnd)
            if notify.hdr.code in (CDN_INITDONE, CDN_FOLDERCHANGE, CDN_FILEOK):
                sync_folder_state(parent_hwnd)
            return 0
        return 0

    dialog = OPENFILENAMEW()
    dialog.lStructSize = ctypes.sizeof(OPENFILENAMEW)
    dialog.hwndOwner = None
    dialog.lpstrFilter = hidden_filter
    dialog.nFilterIndex = 1
    dialog.lpstrFile = ctypes.cast(file_buffer, wintypes.LPWSTR)
    dialog.nMaxFile = len(file_buffer)
    dialog.lpstrTitle = title
    dialog.Flags = int(
        OpenFileNameFlag.EXPLORER
        | OpenFileNameFlag.HIDE_READ_ONLY
        | OpenFileNameFlag.NO_CHANGE_DIR
        | OpenFileNameFlag.PATH_MUST_EXIST
        | OpenFileNameFlag.ENABLE_HOOK
        | OpenFileNameFlag.NO_VALIDATE
    )
    dialog.lpfnHook = ctypes.cast(hook_proc, wintypes.LPVOID)

    if not api.comdlg32.GetOpenFileNameW(ctypes.byref(dialog)):
        return None
    result_folder = selected_folder
    if result_folder is None:
        raw_path = Path(file_buffer.value)
        if raw_path.name == FOLDER_SENTINEL_NAME:
            return raw_path.parent
        return raw_path
    return result_folder


def pick_date(
    prompt: str = "Choose a date:",
    *,
    title: str = "Select Date",
    initial_date: date | None = None,
) -> date | None:
    ensure_windows()
    api = win_api()
    instance = api.kernel32.GetModuleHandleW(None)
    class_name = f"pywinpop_date_{id(initial_date) ^ id(prompt)}"
    gui_font = api.gdi32.GetStockObject(DEFAULT_GUI_FONT)
    selected_date: date | None = None
    finished = False

    init_controls = INITCOMMONCONTROLSEX()
    init_controls.dwSize = ctypes.sizeof(INITCOMMONCONTROLSEX)
    init_controls.dwICC = ICC_DATE_CLASSES
    if not api.comctl32.InitCommonControlsEx(ctypes.byref(init_controls)):
        msg = "Failed to initialize common controls for the date picker."
        raise OSError(msg)

    @WndProc
    def window_proc(hwnd: int, msg: int, w_param: int, l_param: int) -> int:
        nonlocal finished, selected_date
        if msg == WindowMessage.COMMAND:
            command_id = w_param & 0xFFFF
            notification = (w_param >> 16) & 0xFFFF
            if command_id == DialogResult.OK and notification == BN_CLICKED:
                system_time = SYSTEMTIME()
                picker_hwnd = api.user32.GetDlgItem(hwnd, DATE_PICKER_CONTROL_ID)
                status = api.user32.SendMessageW(
                    picker_hwnd,
                    MCM_GETCURSEL,
                    0,
                    ctypes.addressof(system_time),
                )
                if status:
                    selected_date = date(
                        system_time.wYear,
                        system_time.wMonth,
                        system_time.wDay,
                    )
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
        msg = "Failed to register the date picker window class."
        raise OSError(msg)

    try:
        hwnd = api.user32.CreateWindowExW(
            0,
            class_name,
            title,
            int(WindowStyle.POPUP | WindowStyle.CAPTION | WindowStyle.SYSMENU),
            CW_USEDEFAULT,
            CW_USEDEFAULT,
            280,
            290,
            None,
            None,
            instance,
            None,
        )
        if not hwnd:
            msg = "Failed to create the date picker window."
            raise OSError(msg)

        prompt_hwnd = api.user32.CreateWindowExW(
            0,
            "STATIC",
            prompt,
            int(WindowStyle.CHILD | WindowStyle.VISIBLE | StaticStyle.LEFT),
            12,
            12,
            240,
            20,
            hwnd,
            wintypes.HMENU(DATE_PICKER_PROMPT_ID),
            instance,
            None,
        )
        picker_hwnd = api.user32.CreateWindowExW(
            0,
            "SysMonthCal32",
            None,
            int(WindowStyle.CHILD | WindowStyle.VISIBLE | WindowStyle.TAB_STOP),
            12,
            40,
            240,
            160,
            hwnd,
            wintypes.HMENU(DATE_PICKER_CONTROL_ID),
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
            84,
            218,
            80,
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
            172,
            218,
            80,
            28,
            hwnd,
            wintypes.HMENU(DialogResult.CANCEL),
            instance,
            None,
        )

        if initial_date is None:
            initial_date = date.today()
        system_time = SYSTEMTIME(
            wYear=initial_date.year,
            wMonth=initial_date.month,
            wDayOfWeek=initial_date.weekday(),
            wDay=initial_date.day,
            wHour=0,
            wMinute=0,
            wSecond=0,
            wMilliseconds=0,
        )
        api.user32.SendMessageW(
            picker_hwnd,
            MCM_SETCURSEL,
            0,
            ctypes.addressof(system_time),
        )

        for control in (prompt_hwnd, ok_hwnd, cancel_hwnd):
            if gui_font and control:
                api.user32.SendMessageW(control, WindowMessage.SET_FONT, gui_font, 1)

        api.user32.ShowWindow(hwnd, SW_SHOW)
        api.user32.UpdateWindow(hwnd)
        api.user32.SetFocus(picker_hwnd)

        message = MSG()
        while not finished:
            status = api.user32.GetMessageW(ctypes.byref(message), None, 0, 0)
            if status <= 0:
                break
            api.user32.TranslateMessage(ctypes.byref(message))
            api.user32.DispatchMessageW(ctypes.byref(message))
    finally:
        api.user32.UnregisterClassW(class_name, instance)

    return selected_date


def pick_datetime(
    prompt: str = "Choose a date and time:",
    *,
    title: str = "Select Date and Time",
    initial_value: datetime | None = None,
) -> datetime | None:
    ensure_windows()
    api = win_api()
    instance = api.kernel32.GetModuleHandleW(None)
    class_name = f"pywinpop_datetime_{id(initial_value) ^ id(prompt)}"
    gui_font = api.gdi32.GetStockObject(DEFAULT_GUI_FONT)
    selected_value: datetime | None = None
    finished = False

    init_controls = INITCOMMONCONTROLSEX()
    init_controls.dwSize = ctypes.sizeof(INITCOMMONCONTROLSEX)
    init_controls.dwICC = ICC_DATE_CLASSES
    if not api.comctl32.InitCommonControlsEx(ctypes.byref(init_controls)):
        msg = "Failed to initialize common controls for the date-time picker."
        raise OSError(msg)

    @WndProc
    def window_proc(hwnd: int, msg: int, w_param: int, l_param: int) -> int:
        nonlocal finished, selected_value
        if msg == WindowMessage.COMMAND:
            command_id = w_param & 0xFFFF
            notification = (w_param >> 16) & 0xFFFF
            if command_id == DialogResult.OK and notification == BN_CLICKED:
                date_time = SYSTEMTIME()
                time_value = SYSTEMTIME()
                calendar_hwnd = api.user32.GetDlgItem(hwnd, DATE_PICKER_CONTROL_ID)
                time_hwnd = api.user32.GetDlgItem(hwnd, DATE_TIME_PICKER_TIME_ID)
                date_status = api.user32.SendMessageW(
                    calendar_hwnd,
                    MCM_GETCURSEL,
                    0,
                    ctypes.addressof(date_time),
                )
                time_status = api.user32.SendMessageW(
                    time_hwnd,
                    DTM_GETSYSTEMTIME,
                    0,
                    ctypes.addressof(time_value),
                )
                if date_status and time_status == GDT_VALID:
                    selected_value = datetime(
                        date_time.wYear,
                        date_time.wMonth,
                        date_time.wDay,
                        time_value.wHour,
                        time_value.wMinute,
                        time_value.wSecond,
                    )
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
        msg = "Failed to register the date-time picker window class."
        raise OSError(msg)

    try:
        hwnd = api.user32.CreateWindowExW(
            0,
            class_name,
            title,
            int(WindowStyle.POPUP | WindowStyle.CAPTION | WindowStyle.SYSMENU),
            CW_USEDEFAULT,
            CW_USEDEFAULT,
            300,
            340,
            None,
            None,
            instance,
            None,
        )
        if not hwnd:
            msg = "Failed to create the date-time picker window."
            raise OSError(msg)

        prompt_hwnd = api.user32.CreateWindowExW(
            0,
            "STATIC",
            prompt,
            int(WindowStyle.CHILD | WindowStyle.VISIBLE | StaticStyle.LEFT),
            12,
            12,
            260,
            20,
            hwnd,
            wintypes.HMENU(DATE_PICKER_PROMPT_ID),
            instance,
            None,
        )
        calendar_hwnd = api.user32.CreateWindowExW(
            0,
            "SysMonthCal32",
            None,
            int(WindowStyle.CHILD | WindowStyle.VISIBLE | WindowStyle.TAB_STOP),
            12,
            40,
            260,
            160,
            hwnd,
            wintypes.HMENU(DATE_PICKER_CONTROL_ID),
            instance,
            None,
        )
        time_hwnd = api.user32.CreateWindowExW(
            0,
            "SysDateTimePick32",
            None,
            int(WindowStyle.CHILD | WindowStyle.VISIBLE | WindowStyle.TAB_STOP | DTS_TIMEFORMAT | DTS_UPDOWN),
            12,
            214,
            160,
            24,
            hwnd,
            wintypes.HMENU(DATE_TIME_PICKER_TIME_ID),
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
            104,
            258,
            80,
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
            192,
            258,
            80,
            28,
            hwnd,
            wintypes.HMENU(DialogResult.CANCEL),
            instance,
            None,
        )

        if initial_value is None:
            initial_value = datetime.now().replace(microsecond=0)
        system_time = SYSTEMTIME(
            wYear=initial_value.year,
            wMonth=initial_value.month,
            wDayOfWeek=initial_value.weekday(),
            wDay=initial_value.day,
            wHour=initial_value.hour,
            wMinute=initial_value.minute,
            wSecond=initial_value.second,
            wMilliseconds=0,
        )
        api.user32.SendMessageW(
            calendar_hwnd,
            MCM_SETCURSEL,
            0,
            ctypes.addressof(system_time),
        )
        api.user32.SendMessageW(
            time_hwnd,
            DTM_SETSYSTEMTIME,
            GDT_VALID,
            ctypes.addressof(system_time),
        )

        for control in (prompt_hwnd, time_hwnd, ok_hwnd, cancel_hwnd):
            if gui_font and control:
                api.user32.SendMessageW(control, WindowMessage.SET_FONT, gui_font, 1)

        api.user32.ShowWindow(hwnd, SW_SHOW)
        api.user32.UpdateWindow(hwnd)
        api.user32.SetFocus(time_hwnd)

        message = MSG()
        while not finished:
            status = api.user32.GetMessageW(ctypes.byref(message), None, 0, 0)
            if status <= 0:
                break
            api.user32.TranslateMessage(ctypes.byref(message))
            api.user32.DispatchMessageW(ctypes.byref(message))
    finally:
        api.user32.UnregisterClassW(class_name, instance)

    return selected_value
