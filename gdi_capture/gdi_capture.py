import os
import ctypes.wintypes
import numpy as np

dll_path = os.path.join(os.path.dirname(__file__), "gdi_capture.dll")
gdi_capture_dll = ctypes.WinDLL(dll_path)

gdi_capture_dll.FindWindowFromExecutableName.restype = ctypes.wintypes.HWND
gdi_capture_dll.FindWindowFromExecutableName.argtype = [ctypes.wintypes.LPCWSTR]

gdi_capture_dll.CaptureWindow.restype = ctypes.wintypes.HBITMAP
gdi_capture_dll.CaptureWindow.argtype = [ctypes.wintypes.HWND, ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.POINTER(ctypes.c_uint8))]

gdi_capture_dll.FreeBitmapHandle.restype = None
gdi_capture_dll.FreeBitmapHandle.argtype = [ctypes.wintypes.HBITMAP]

def find_window_from_executable_name(name):
	return gdi_capture_dll.FindWindowFromExecutableName(name)

class CaptureWindow:
	def __init__(self, hwnd):
		self.hwnd = hwnd

	def __enter__(self):
		width = ctypes.c_long()
		height = ctypes.c_long()
		bitmap_ptr = ctypes.POINTER(ctypes.c_uint8)()

		self.bitmap_handle = gdi_capture_dll.CaptureWindow(self.hwnd, ctypes.byref(width), ctypes.byref(height), ctypes.byref(bitmap_ptr))
		if self.bitmap_handle is None:
			return

		return np.ctypeslib.as_array(bitmap_ptr, shape=(height.value, width.value, 4))

	def __exit__(self, exc_type, exc_value, traceback):
		if self.bitmap_handle is None:
			return

		gdi_capture_dll.FreeBitmapHandle(ctypes.wintypes.HBITMAP(self.bitmap_handle))
