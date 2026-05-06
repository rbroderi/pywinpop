import ctypes
import sys
from ctypes import wintypes
from typing import Any
from typing import ClassVar
from typing import final


class OPENFILENAMEW(ctypes.Structure):
    _fields_: ClassVar[Any] = [
        ("lStructSize", wintypes.DWORD),
        ("hwndOwner", wintypes.HWND),
        ("hInstance", wintypes.HINSTANCE),
        ("lpstrFilter", wintypes.LPCWSTR),
        ("lpstrCustomFilter", wintypes.LPWSTR),
        ("nMaxCustFilter", wintypes.DWORD),
        ("nFilterIndex", wintypes.DWORD),
        ("lpstrFile", wintypes.LPWSTR),
        ("nMaxFile", wintypes.DWORD),
        ("lpstrFileTitle", wintypes.LPWSTR),
        ("nMaxFileTitle", wintypes.DWORD),
        ("lpstrInitialDir", wintypes.LPCWSTR),
        ("lpstrTitle", wintypes.LPCWSTR),
        ("Flags", wintypes.DWORD),
        ("nFileOffset", wintypes.WORD),
        ("nFileExtension", wintypes.WORD),
        ("lpstrDefExt", wintypes.LPCWSTR),
        ("lCustData", wintypes.LPARAM),
        ("lpfnHook", wintypes.LPVOID),
        ("lpTemplateName", wintypes.LPCWSTR),
        ("pvReserved", wintypes.LPVOID),
        ("dwReserved", wintypes.DWORD),
        ("FlagsEx", wintypes.DWORD),
    ]


class BROWSEINFOW(ctypes.Structure):
    _fields_: ClassVar[Any] = [
        ("hwndOwner", wintypes.HWND),
        ("pidlRoot", wintypes.LPVOID),
        ("pszDisplayName", wintypes.LPWSTR),
        ("lpszTitle", wintypes.LPCWSTR),
        ("ulFlags", wintypes.UINT),
        ("lpfn", wintypes.LPVOID),
        ("lParam", wintypes.LPARAM),
        ("iImage", ctypes.c_int),
    ]


class POINT(ctypes.Structure):
    _fields_: ClassVar[Any] = [("x", wintypes.LONG), ("y", wintypes.LONG)]


class MSG(ctypes.Structure):
    _fields_: ClassVar[Any] = [
        ("hwnd", wintypes.HWND),
        ("message", wintypes.UINT),
        ("wParam", wintypes.WPARAM),
        ("lParam", wintypes.LPARAM),
        ("time", wintypes.DWORD),
        ("pt", POINT),
        ("lPrivate", wintypes.DWORD),
    ]


class SYSTEMTIME(ctypes.Structure):
    _fields_: ClassVar[Any] = [
        ("wYear", wintypes.WORD),
        ("wMonth", wintypes.WORD),
        ("wDayOfWeek", wintypes.WORD),
        ("wDay", wintypes.WORD),
        ("wHour", wintypes.WORD),
        ("wMinute", wintypes.WORD),
        ("wSecond", wintypes.WORD),
        ("wMilliseconds", wintypes.WORD),
    ]


class INITCOMMONCONTROLSEX(ctypes.Structure):
    _fields_: ClassVar[Any] = [
        ("dwSize", wintypes.DWORD),
        ("dwICC", wintypes.DWORD),
    ]


class WNDCLASSW(ctypes.Structure):
    _fields_: ClassVar[Any] = [
        ("style", wintypes.UINT),
        ("lpfnWndProc", wintypes.LPVOID),
        ("cbClsExtra", ctypes.c_int),
        ("cbWndExtra", ctypes.c_int),
        ("hInstance", wintypes.HINSTANCE),
        ("hIcon", wintypes.HICON),
        ("hCursor", wintypes.HCURSOR),
        ("hbrBackground", wintypes.HBRUSH),
        ("lpszMenuName", wintypes.LPCWSTR),
        ("lpszClassName", wintypes.LPCWSTR),
    ]


class NMHDR(ctypes.Structure):
    _fields_: ClassVar[Any] = [
        ("hwndFrom", wintypes.HWND),
        ("idFrom", ctypes.c_size_t),
        ("code", ctypes.c_uint),
    ]


class OFNOTIFYW(ctypes.Structure):
    _fields_: ClassVar[Any] = [
        ("hdr", NMHDR),
        ("lpOFN", ctypes.POINTER(OPENFILENAMEW)),
        ("pszFile", wintypes.LPWSTR),
    ]


class CHOOSECOLORW(ctypes.Structure):
    _fields_: ClassVar[Any] = [
        ("lStructSize", wintypes.DWORD),
        ("hwndOwner", wintypes.HWND),
        ("hInstance", wintypes.HWND),
        ("rgbResult", wintypes.DWORD),
        ("lpCustColors", ctypes.POINTER(wintypes.DWORD)),
        ("Flags", wintypes.DWORD),
        ("lCustData", wintypes.LPARAM),
        ("lpfnHook", wintypes.LPVOID),
        ("lpTemplateName", wintypes.LPCWSTR),
    ]


class LOGFONTW(ctypes.Structure):
    _fields_: ClassVar[Any] = [
        ("lfHeight", wintypes.LONG),
        ("lfWidth", wintypes.LONG),
        ("lfEscapement", wintypes.LONG),
        ("lfOrientation", wintypes.LONG),
        ("lfWeight", wintypes.LONG),
        ("lfItalic", wintypes.BYTE),
        ("lfUnderline", wintypes.BYTE),
        ("lfStrikeOut", wintypes.BYTE),
        ("lfCharSet", wintypes.BYTE),
        ("lfOutPrecision", wintypes.BYTE),
        ("lfClipPrecision", wintypes.BYTE),
        ("lfQuality", wintypes.BYTE),
        ("lfPitchAndFamily", wintypes.BYTE),
        ("lfFaceName", ctypes.c_wchar * 32),
    ]


class CHOOSEFONTW(ctypes.Structure):
    _fields_: ClassVar[Any] = [
        ("lStructSize", wintypes.DWORD),
        ("hwndOwner", wintypes.HWND),
        ("hDC", wintypes.HDC),
        ("lpLogFont", ctypes.POINTER(LOGFONTW)),
        ("iPointSize", ctypes.c_int),
        ("Flags", wintypes.DWORD),
        ("rgbColors", wintypes.DWORD),
        ("lCustData", wintypes.LPARAM),
        ("lpfnHook", wintypes.LPVOID),
        ("lpTemplateName", wintypes.LPCWSTR),
        ("hInstance", wintypes.HINSTANCE),
        ("lpszStyle", wintypes.LPWSTR),
        ("nFontType", wintypes.WORD),
        ("___MISSING_ALIGNMENT__", wintypes.WORD),
        ("nSizeMin", ctypes.c_int),
        ("nSizeMax", ctypes.c_int),
    ]


WndProc = ctypes.WINFUNCTYPE(
    ctypes.c_ssize_t,
    wintypes.HWND,
    wintypes.UINT,
    wintypes.WPARAM,
    wintypes.LPARAM,
)

OpenFileHookProc = ctypes.WINFUNCTYPE(
    ctypes.c_uint,
    wintypes.HWND,
    wintypes.UINT,
    wintypes.WPARAM,
    wintypes.LPARAM,
)


@final
class _WinApi:
    def __init__(self) -> None:
        self.user32: Any = ctypes.WinDLL("user32", use_last_error=True)
        self.comdlg32: Any = ctypes.WinDLL("comdlg32", use_last_error=True)
        self.comctl32: Any = ctypes.WinDLL("comctl32", use_last_error=True)
        self.shell32: Any = ctypes.WinDLL("shell32", use_last_error=True)
        self.ole32: Any = ctypes.WinDLL("ole32", use_last_error=True)
        self.gdi32: Any = ctypes.WinDLL("gdi32", use_last_error=True)
        self.kernel32: Any = ctypes.WinDLL("kernel32", use_last_error=True)

        self.user32.MessageBoxW.argtypes = [
            wintypes.HWND,
            wintypes.LPCWSTR,
            wintypes.LPCWSTR,
            wintypes.UINT,
        ]
        self.user32.MessageBoxW.restype = ctypes.c_int
        self.comdlg32.GetOpenFileNameW.argtypes = [ctypes.POINTER(OPENFILENAMEW)]
        self.comdlg32.GetOpenFileNameW.restype = wintypes.BOOL
        self.comdlg32.GetSaveFileNameW.argtypes = [ctypes.POINTER(OPENFILENAMEW)]
        self.comdlg32.GetSaveFileNameW.restype = wintypes.BOOL
        self.comdlg32.ChooseColorW.argtypes = [ctypes.POINTER(CHOOSECOLORW)]
        self.comdlg32.ChooseColorW.restype = wintypes.BOOL
        self.comdlg32.ChooseFontW.argtypes = [ctypes.POINTER(CHOOSEFONTW)]
        self.comdlg32.ChooseFontW.restype = wintypes.BOOL
        self.comctl32.InitCommonControlsEx.argtypes = [ctypes.POINTER(INITCOMMONCONTROLSEX)]
        self.comctl32.InitCommonControlsEx.restype = wintypes.BOOL
        self.shell32.SHBrowseForFolderW.argtypes = [ctypes.POINTER(BROWSEINFOW)]
        self.shell32.SHBrowseForFolderW.restype = wintypes.LPVOID
        self.shell32.SHGetPathFromIDListW.argtypes = [wintypes.LPVOID, wintypes.LPWSTR]
        self.shell32.SHGetPathFromIDListW.restype = wintypes.BOOL
        self.ole32.CoTaskMemFree.argtypes = [wintypes.LPVOID]
        self.ole32.CoTaskMemFree.restype = None
        self.user32.SetDlgItemTextW.argtypes = [
            wintypes.HWND,
            ctypes.c_int,
            wintypes.LPCWSTR,
        ]
        self.user32.SetDlgItemTextW.restype = wintypes.BOOL
        self.user32.GetDlgItemTextW.argtypes = [
            wintypes.HWND,
            ctypes.c_int,
            wintypes.LPWSTR,
            ctypes.c_int,
        ]
        self.user32.GetDlgItemTextW.restype = ctypes.c_uint
        self.user32.SendMessageW.argtypes = [
            wintypes.HWND,
            wintypes.UINT,
            wintypes.WPARAM,
            wintypes.LPARAM,
        ]
        self.user32.SendMessageW.restype = ctypes.c_ssize_t
        self.user32.GetDlgItem.argtypes = [wintypes.HWND, ctypes.c_int]
        self.user32.GetDlgItem.restype = wintypes.HWND
        self.user32.DefWindowProcW.argtypes = [
            wintypes.HWND,
            wintypes.UINT,
            wintypes.WPARAM,
            wintypes.LPARAM,
        ]
        self.user32.DefWindowProcW.restype = ctypes.c_ssize_t
        self.user32.RegisterClassW.argtypes = [ctypes.POINTER(WNDCLASSW)]
        self.user32.RegisterClassW.restype = wintypes.ATOM
        self.user32.UnregisterClassW.argtypes = [wintypes.LPCWSTR, wintypes.HINSTANCE]
        self.user32.UnregisterClassW.restype = wintypes.BOOL
        self.user32.CreateWindowExW.argtypes = [
            wintypes.DWORD,
            wintypes.LPCWSTR,
            wintypes.LPCWSTR,
            wintypes.DWORD,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            wintypes.HWND,
            wintypes.HMENU,
            wintypes.HINSTANCE,
            wintypes.LPVOID,
        ]
        self.user32.CreateWindowExW.restype = wintypes.HWND
        self.user32.DestroyWindow.argtypes = [wintypes.HWND]
        self.user32.DestroyWindow.restype = wintypes.BOOL
        self.user32.ShowWindow.argtypes = [wintypes.HWND, ctypes.c_int]
        self.user32.ShowWindow.restype = wintypes.BOOL
        self.user32.UpdateWindow.argtypes = [wintypes.HWND]
        self.user32.UpdateWindow.restype = wintypes.BOOL
        self.user32.GetMessageW.argtypes = [
            ctypes.POINTER(MSG),
            wintypes.HWND,
            wintypes.UINT,
            wintypes.UINT,
        ]
        self.user32.GetMessageW.restype = wintypes.BOOL
        self.user32.TranslateMessage.argtypes = [ctypes.POINTER(MSG)]
        self.user32.TranslateMessage.restype = wintypes.BOOL
        self.user32.DispatchMessageW.argtypes = [ctypes.POINTER(MSG)]
        self.user32.DispatchMessageW.restype = ctypes.c_ssize_t
        self.user32.LoadCursorW.argtypes = [wintypes.HINSTANCE, wintypes.LPCWSTR]
        self.user32.LoadCursorW.restype = wintypes.HCURSOR
        self.user32.SetFocus.argtypes = [wintypes.HWND]
        self.user32.SetFocus.restype = wintypes.HWND
        self.user32.GetParent.argtypes = [wintypes.HWND]
        self.user32.GetParent.restype = wintypes.HWND
        self.user32.PeekMessageW.argtypes = [
            ctypes.POINTER(MSG),
            wintypes.HWND,
            wintypes.UINT,
            wintypes.UINT,
            wintypes.UINT,
        ]
        self.user32.PeekMessageW.restype = wintypes.BOOL
        self.kernel32.GetModuleHandleW.argtypes = [wintypes.LPCWSTR]
        self.kernel32.GetModuleHandleW.restype = wintypes.HMODULE
        self.gdi32.GetStockObject.argtypes = [ctypes.c_int]
        self.gdi32.GetStockObject.restype = wintypes.HGDIOBJ


_win_api_cache: _WinApi | None = None


def win_api() -> _WinApi:
    global _win_api_cache
    if _win_api_cache is None:
        _win_api_cache = _WinApi()
    return _win_api_cache


def ensure_windows() -> None:
    if sys.platform != "win32" or not hasattr(ctypes, "WinDLL"):
        msg = "pywinpop requires Windows."
        raise OSError(msg)
