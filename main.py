from src.dw import download_manager
from src.gui import appGui
import ctypes
import os
import sys

def set_dpi_awareness():
    if hasattr(ctypes, 'windll'):
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except Exception:
            try:
                ctypes.windll.user32.SetProcessDPIAware()
            except Exception:
                pass

def main():
    set_dpi_awareness()
    appGui(download_manager)

if __name__ == "__main__":
    main()