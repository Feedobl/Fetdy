import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkFont
from tkinter import filedialog
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_scaling_factor(root):
    try:
        import ctypes
        user32 = ctypes.windll.user32
        dpi = user32.GetDpiForWindow(root.winfo_id())
        return dpi / 96.0
    except:
        return root.winfo_fpixels('1i') / 72.0

def appGui(download_manager):
    root = tk.Tk()
    scale = get_scaling_factor(root)
    headerFont = tkFont.Font(family='Poppins Bold', size=int(24 * scale))
    subheaderFont = tkFont.Font(family='Poppins Bold', size=int(18 * scale))
    normalFont = tkFont.Font(family='Poppins', size=int(14 * scale))
    buttonFont = tkFont.Font(family='Poppins Bold', size=int(12 * scale))
    statusFont = tkFont.Font(family='Poppins', size=int(12 * scale))
    window_width = int(800 * scale)
    window_height = int(650 * scale)
    root.title("Fetdy")
    icon_path = resource_path("assets/Fetdy.ico")
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/1.8)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    primaryColor = "#504B38"
    secondaryColor = "#B9B28A"
    accentColor = "#EBE5C2"
    bgColor = "#F2E9E4"
    textColor = "#1f1d1d"
    highlightColor = "#635C48"
    cardBgColor = "#FFFFFF"
    style = ttk.Style()
    style.theme_use('clam')
    root.configure(bg=bgColor)
    style.configure("Card.TFrame", background=cardBgColor, relief="flat", borderwidth=0)
    style.configure("header.TLabel", font=headerFont, background=bgColor, foreground=primaryColor)
    style.configure("subheader.TLabel", font=subheaderFont, background=cardBgColor, foreground=primaryColor)
    style.configure("section.TLabel", font=subheaderFont, background=cardBgColor, foreground=textColor)
    style.configure("TLabel", background=cardBgColor, font=normalFont, foreground=textColor)
    style.configure("normal.TLabel", background=cardBgColor, font=normalFont, foreground=textColor)
    style.configure("subtitle.TLabel", background=bgColor, font=normalFont, foreground=textColor)
    style.configure("TFrame", background=cardBgColor)
    style.configure("header.TFrame", background=bgColor)
    style.configure("TEntry", foreground=textColor, fieldbackground="#FFFFFF", bordercolor=secondaryColor, font=normalFont)
    style.configure("normal.TRadiobutton", font=normalFont, background=cardBgColor, foreground=textColor)
    style.map("normal.TRadiobutton",
        background=[('active', cardBgColor)],
        highlightcolor=[('focus', cardBgColor)],
        indicatorcolor=[('selected', primaryColor)],
        focuscolor=[('focus', cardBgColor)])
    style.configure("TCombobox", font=normalFont, background=accentColor, foreground=textColor, arrowcolor=primaryColor)
    style.map("TCombobox",
        background=[('active', accentColor)],
        fieldbackground=[('readonly', "#FFFFFF")],
        foreground=[('readonly', textColor)])
    style.configure("TButton", font=buttonFont, background=primaryColor, foreground="#FFFFFF",
                   bordercolor=primaryColor, relief="flat", padding=(15, 8))
    style.map("TButton",
              background=[('active', highlightColor), ('pressed', "#403C2D")],
              foreground=[('active', "#FFFFFF"), ('pressed', "#FFFFFF")])
    style.configure("Secondary.TButton", font=buttonFont, background=secondaryColor,
                   foreground=textColor, padding=(8, 2))
    style.configure("status.TLabel", font=statusFont, background=cardBgColor, foreground="#555555")
    style.configure("TProgressbar", background=primaryColor, troughcolor=accentColor, thickness=8, borderwidth=0)
    root.tk.call('tk', 'scaling', scale)
    style.configure("TButton", padding=(int(15 * scale), int(8 * scale)))
    style.configure("TEntry", padding=(int(5 * scale)))
    mainFrame = ttk.Frame(root, style="TFrame")
    mainFrame.pack(expand=True, fill='both')
    headerFrame = ttk.Frame(mainFrame, style="header.TFrame")
    headerFrame.pack(fill='x')
    header = ttk.Label(headerFrame, text="Fetdy", style="header.TLabel")
    header.pack(pady=(10, 0))
    subtitle = ttk.Label(headerFrame, text="Media Downloader", style="subtitle.TLabel")
    subtitle.pack(pady=(0, 10))
    cardFrame = ttk.Frame(mainFrame, style="Card.TFrame")
    cardFrame.pack(expand=True, fill='both', padx=30, pady=(0, 20))
    contentFrame = ttk.Frame(cardFrame)
    contentFrame.pack(expand=True, fill='both', padx=20, pady=15)
    urlFrame = ttk.Frame(contentFrame)
    urlFrame.pack(fill='x', pady=(0, 12))
    urlLabel = ttk.Label(urlFrame, text="Enter URL:", style="section.TLabel")
    urlLabel.pack(anchor='w', pady=(0, 5))
    urlInput = ttk.Entry(urlFrame)
    urlInput.pack(fill='x', ipady=3)
    ttk.Separator(contentFrame, orient='horizontal').pack(fill='x', pady=10)
    optionsLabel = ttk.Label(contentFrame, text="Download Options", style="section.TLabel")
    optionsLabel.pack(anchor='w', pady=(0, 10))
    options = ttk.Frame(contentFrame)
    options.pack(fill='x', pady=(0, 10))
    audio_qualities = ["64kbps", "128kbps", "192kbps", "256kbps", "320kbps"]
    video_qualities = ["144p", "240p", "360p", "480p", "720p", "1080p", "1440p", "2160p"]
    audio_formats = ["MP3", "M4A", "WAV", "FLAC", "OGG"]
    video_formats = ["MP4", "MKV", "WEBM", "AVI", "MOV"]
    qualityComboBox = None
    formatComboBox = None
    def update_options():
        if formatVar.get() == "audio":
            qualityComboBox['values'] = audio_qualities
            qualityComboBox.set(audio_qualities[2])
            formatComboBox['values'] = audio_formats
            formatComboBox.set(audio_formats[0])
        else:
            qualityComboBox['values'] = video_qualities
            qualityComboBox.set("720p")
            formatComboBox['values'] = video_formats
            formatComboBox.set(video_formats[0])
    formatVar = tk.StringVar(value="audio")
    audioOrVideoFrame = ttk.Frame(options)
    audioOrVideoFrame.pack(side='left', padx=(0, 20))
    typeLabel = ttk.Label(audioOrVideoFrame, text="Type:", style="normal.TLabel")
    typeLabel.pack(anchor='w', pady=(0, 3))
    audioButton = ttk.Radiobutton(audioOrVideoFrame, text="Audio", value="audio", 
                                variable=formatVar, style="normal.TRadiobutton",
                                command=update_options)
    audioButton.pack(anchor='w', pady=1)
    videoButton = ttk.Radiobutton(audioOrVideoFrame, text="Video", value="video", 
                                variable=formatVar, style="normal.TRadiobutton",
                                command=update_options)
    videoButton.pack(anchor='w', pady=1)
    optionsPanel = ttk.Frame(options)
    optionsPanel.pack(side='left', fill='x', expand=True)
    qualityFrame = ttk.Frame(optionsPanel)
    qualityFrame.pack(fill='x', pady=(0, 8))
    qualityLabel = ttk.Label(qualityFrame, text="Quality:", style="normal.TLabel")
    qualityLabel.pack(anchor='w', pady=(0, 3))
    qualityComboBox = ttk.Combobox(qualityFrame, values=audio_qualities, state="readonly")
    qualityComboBox.set(audio_qualities[2])
    qualityComboBox.pack(fill='x')
    formatFrame = ttk.Frame(optionsPanel)
    formatFrame.pack(fill='x', pady=(8, 0))
    formatLabel = ttk.Label(formatFrame, text="Format:", style="normal.TLabel")
    formatLabel.pack(anchor='w', pady=(0, 3))
    formatComboBox = ttk.Combobox(formatFrame, values=audio_formats, state="readonly")
    formatComboBox.set(audio_formats[0])
    formatComboBox.pack(fill='x')
    ttk.Separator(contentFrame, orient='horizontal').pack(fill='x', pady=10)
    downloadPathLabel = ttk.Label(contentFrame, text="Download Location", style="section.TLabel")
    downloadPathLabel.pack(anchor='w', pady=(0, 10))
    downloadPathFrame = ttk.Frame(contentFrame)
    downloadPathFrame.pack(fill='x', pady=(0, 10))
    default_path = os.path.join(os.path.expanduser("~"), "Downloads")
    downloadPath = tk.StringVar(value=default_path)
    def browse_folder():
        folder_selected = filedialog.askdirectory(initialdir=downloadPath.get())
        if folder_selected:
            downloadPath.set(folder_selected)
    pathLabel = ttk.Label(downloadPathFrame, text="Save to:", style="normal.TLabel")
    pathLabel.pack(side='left', padx=(0, 5))
    pathEntry = ttk.Entry(downloadPathFrame, textvariable=downloadPath)
    pathEntry.pack(side='left', fill='x', expand=True, padx=(0, 5))
    browseButton = ttk.Button(downloadPathFrame, text="Browse", style="Secondary.TButton", 
                             command=browse_folder, width=10)
    browseButton.pack(side='right')
    ttk.Separator(contentFrame, orient='horizontal').pack(fill='x', pady=10)
    
    bottomFrame = ttk.Frame(contentFrame)
    bottomFrame.pack(fill='x', side='bottom', pady=(10, 0))

    downloadButton = ttk.Button(bottomFrame, text="Download", style="TButton")


    progressFrame = ttk.Frame(bottomFrame)
    progressFrame.pack(fill='x')
    progressBar = ttk.Progressbar(progressFrame, orient="horizontal", length=100, mode="determinate", style="TProgressbar")

    statusFrame = ttk.Frame(bottomFrame)
    statusFrame.pack(fill='x', pady=(5, 0))
    statusLabel = ttk.Label(statusFrame, text="Ready to download", style="status.TLabel")


    statusLabel.pack(anchor='w')
    progressBar.pack(fill='x')
    downloadButton.pack(pady=(0, 10), fill='x')

    def start_download():
        url = urlInput.get().strip()
        if not url:
            statusLabel.config(text="Please enter a valid URL")
            return
        downloadButton.config(state="disabled")
        progressBar["value"] = 0
        media_type = formatVar.get()
        quality = qualityComboBox.get()
        format_type = formatComboBox.get()
        save_path = downloadPath.get()
        def update_progress(progress_data):
            if progress_data['status'] == 'downloading':
                percent = progress_data['percent']
                speed = progress_data['speed']
                eta = progress_data['eta']
                filename = progress_data['filename']
                progressBar["value"] = percent
                statusLabel.config(text=f"Downloading {filename} - {speed} - ETA: {eta}")
                root.update_idletasks()
            elif progress_data['status'] == 'finished':
                statusLabel.config(text="Processing download...")
        def on_complete(result):
            downloadButton.config(state="normal")
            if result['success']:
                statusLabel.config(text=f"Download complete! Saved to {save_path}")
                progressBar["value"] = 100
            else:
                statusLabel.config(text=f"Error: {result['error']}")
                progressBar["value"] = 0
        statusLabel.config(text="Starting download...")
        download_manager.download(
            url=url,
            output_path=save_path,
            media_type=media_type,
            quality=quality,
            format_type=format_type,
            progress_callback=update_progress,
            completion_callback=on_complete
        )
    downloadButton.config(command=start_download)
    root.mainloop()

if __name__ == "__main__":
    from src.dw import download_manager
    appGui(download_manager)