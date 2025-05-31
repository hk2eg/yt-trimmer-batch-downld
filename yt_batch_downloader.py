import os
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from yt_dlp import YoutubeDL

# === YDL OPTIONS ===
ydl_opts = {
    'format': 'bestvideo+bestaudio/best',
    'merge_output_format': 'mp4',
    'noplaylist': True,
    'ffmpeg_location': 'C:\\ffmpeg\\bin\\ffmpeg.exe',  
    'quiet': True,
}

class BatchDownloaderApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("YouTube Batch Downloader")
        self.geometry("800x600")
        self.download_dir = os.path.join(os.getcwd(), "downloads")

        # --- Control Buttons ---
        ctrl = tk.Frame(self)
        ctrl.pack(fill=tk.X, pady=5)
        tk.Button(ctrl, text="Add Row", command=self.add_row).pack(side=tk.LEFT, padx=2)
        tk.Button(ctrl, text="Delete Row", command=self.del_row).pack(side=tk.LEFT, padx=2)
        tk.Button(ctrl, text="Choose Output Dir", command=self.choose_output_dir).pack(side=tk.LEFT, padx=2)
        tk.Button(ctrl, text="Start Download", command=self.start_download).pack(side=tk.RIGHT, padx=2)

        # --- Table ---
        cols = ('url', 'start', 'end')
        self.table = ttk.Treeview(self, columns=cols, show='headings', selectmode='extended')
        self.table.heading('url', text='Video URL')
        self.table.heading('start', text='Start (HH:MM:SS)')
        self.table.heading('end', text='End   (HH:MM:SS)')
        self.table.column('url', width=450)
        self.table.column('start', width=120)
        self.table.column('end', width=120)
        self.table.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Bind double-click for editing
        self.table.bind('<Double-1>', self.on_double_click)

        # --- Log Box ---
        self.log_box = scrolledtext.ScrolledText(self, height=8, bg='#f0f0f0')
        self.log_box.pack(fill=tk.BOTH, expand=False, padx=10, pady=5)
        self.log("Ready.")

    def add_row(self):
        self.table.insert('', 'end', values=('', '', ''))

    def del_row(self):
        for sel in self.table.selection():
            self.table.delete(sel)

    def choose_output_dir(self):
        d = filedialog.askdirectory(title="Select download directory")
        if d:
            self.download_dir = d
            self.log(f"Output directory: {d}")

    def start_download(self):
        rows = [self.table.item(r)['values'] for r in self.table.get_children()]
        if not any(r[0].strip() for r in rows):
            messagebox.showwarning("No URLs", "Please add at least one URL.")
            return
        # disable controls
        for w in self.winfo_children():
            w.configure(state='disabled') if isinstance(w, tk.Button) else None
        threading.Thread(target=self.download_videos, args=(rows,), daemon=True).start()

    def download_videos(self, rows):
        os.makedirs(self.download_dir, exist_ok=True)
        for url, start, end in rows:
            url = url.strip()
            if not url:
                continue
            opts = dict(ydl_opts)
            opts['outtmpl'] = os.path.join(self.download_dir, '%(title)s.%(ext)s')
            if start.strip() and end.strip():
                opts['download_sections'] = [f"*{start.strip()}-{end.strip()}"]
                self.log(f"Trimming {url} from {start} to {end}")
            else:
                self.log(f"Downloading full video: {url}")
            try:
                with YoutubeDL(opts) as ydl:
                    print("⏱  download_sections =", opts.get('download_sections'))
                    print("⏱  ffmpeg_location =", opts.get('ffmpeg_location'))
                    ydl.download([url])
                self.log(f"Done: {url}")
            except Exception as e:
                self.log(f"Error ({url}): {e}")
        self.log("All tasks complete.")
        # re-enable controls
        for w in self.winfo_children():
            w.configure(state='normal') if isinstance(w, tk.Button) else None

    def on_double_click(self, event):
        """Edit cell on double-click"""
        region = self.table.identify('region', event.x, event.y)
        if region != 'cell':
            return
        row = self.table.identify_row(event.y)
        col = self.table.identify_column(event.x)
        x, y, width, height = self.table.bbox(row, col)
        value = self.table.set(row, col)
        # create entry widget
        entry = tk.Entry(self.table)
        entry.place(x=x, y=y, width=width, height=height)
        entry.insert(0, value)
        entry.focus_set()

        def on_focus_out(event):
            self.table.set(row, col, entry.get())
            entry.destroy()
        entry.bind('<FocusOut>', on_focus_out)
        entry.bind('<Return>', on_focus_out)

    def log(self, msg):
        self.log_box.insert(tk.END, msg + "\n")
        self.log_box.see(tk.END)

if __name__ == '__main__':
    app = BatchDownloaderApp()
    app.mainloop()
