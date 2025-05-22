import pyautogui
import pygetwindow as gw
import time
import threading
from datetime import datetime
from win10toast import ToastNotifier
import tkinter as tk
from tkinter import scrolledtext, messagebox

window_title = "OMNITRACKER Client"
notifier = ToastNotifier()

class OmniRefresherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("OMNITRACKER Auto Refresh — CYBER MODE")
        self.root.geometry("550x520")
        self.root.configure(bg="#0d0d0d")  # dark cyber background

        self.click_x = 100
        self.click_y = 200
        self.running = False
        self.pulse_index = 0

        # Neon color palette
        self.fg_main = "#00ffe1"
        self.bg_button = "#1a0033"
        self.fg_button = "#ff00cc"
        self.active_bg = "#330066"
        self.active_fg = "#00ffcc"
        self.text_font = ("Consolas", 10)

        # Gradient color palette for background and text pulsation
        self.colors = ["#ff00cc", "#ff33cc", "#00ffff", "#39ff14", "#ff00cc"]
        self.current_color_index = 0

        # === Input Field ===
        self.make_label("Refresh Interval (minutes):").pack(pady=(10, 0))
        self.interval_entry = tk.Entry(root, bg="#000000", fg=self.fg_main,
                                       insertbackground=self.fg_main,
                                       highlightthickness=1, highlightbackground=self.fg_main,
                                       font=self.text_font)
        self.interval_entry.insert(0, "5")
        self.interval_entry.pack(pady=(0, 10))

        # === Buttons ===
        self.start_button = self.make_button("▶ Start Auto Refresh", self.start_refresh)
        self.start_button.pack(pady=5)

        self.stop_button = self.make_button("⏹ Stop Auto Refresh", self.stop_refresh)
        self.stop_button.config(state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        self.coord_button = self.make_button("📍 Get Mouse Coordinates", self.get_coordinates)
        self.coord_button.pack(pady=5)

        # Track all buttons to animate
        self.buttons_to_glow = [self.start_button, self.stop_button, self.coord_button]

        # === Coordinate Display ===
        self.coord_label = tk.Label(root, text="Click Coordinates: (x, y)",
                                    bg="#0d0d0d", fg="#39ff14", font=self.text_font,
                                    width=40, height=2, relief="sunken")
        self.coord_label.pack(pady=10)

        # === Log Display ===
        self.log_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=12,
                                                 bg="#000000", fg=self.fg_main,
                                                 insertbackground=self.fg_main,
                                                 font=self.text_font)
        self.log_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.log("🧠 Cyber GUI Initialized", "cyan")

        # Start glow animation
        self.animate_all_buttons()
        self.animate_text()

        # Start background gradient animation
        self.animate_gradient_background()

        # === Copyright Notice ===
        self.copyright_label = tk.Label(root, text="©Hysspy Github - All rights reserved.", 
                                        bg="#0d0d0d", fg="#ff00cc", font=("Consolas", 8))
        self.copyright_label.pack(side=tk.BOTTOM, pady=5)

    def make_label(self, text):
        return tk.Label(self.root, text=text, bg="#0d0d0d", fg=self.fg_main, font=self.text_font)

    def make_button(self, text, command):
        return tk.Button(self.root, text=text, command=command,
                         bg=self.bg_button, fg=self.fg_button,
                         activebackground=self.active_bg, activeforeground=self.active_fg,
                         font=self.text_font, relief="groove", bd=2)

    def animate_all_buttons(self):
        pulse_colors = ["#ff00cc", "#ff33cc", "#ff66cc", "#ff33cc"]
        self.pulse_index = (self.pulse_index + 1) % len(pulse_colors)
        color = pulse_colors[self.pulse_index]
        for btn in self.buttons_to_glow:
            btn.config(fg=color)
        self.root.after(550, self.animate_all_buttons)

    def animate_text(self):
        text_colors = ["#ff00cc", "#ff33cc", "#00ffff", "#ff00cc"]
        self.pulse_index = (self.pulse_index + 1) % len(text_colors)
        color = text_colors[self.pulse_index]
        
        # Pulsate text for all labels, entries, and log box
        self.coord_label.config(fg=color)
        self.interval_entry.config(fg=color, insertbackground=color)
        self.log_box.config(fg=color, insertbackground=color)

        # Repeat the animation
        self.root.after(550, self.animate_text)

    def animate_gradient_background(self):
        # Simulate a gradient effect by changing the background color
        self.root.configure(bg=self.colors[self.current_color_index])
        self.current_color_index = (self.current_color_index + 1) % len(self.colors)

        # Repeat the background gradient animation every 100 ms
        self.root.after(550, self.animate_gradient_background)

    def log(self, message, tag="white"):
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        self.log_box.insert(tk.END, f"{timestamp} {message}\n", tag)
        self.log_box.tag_config("cyan", foreground="#00ffff")
        self.log_box.tag_config("green", foreground="#39ff14")
        self.log_box.tag_config("pink", foreground="#ff00ff")
        self.log_box.tag_config("yellow", foreground="#ffff00")
        self.log_box.tag_config("red", foreground="#ff4444")
        self.log_box.tag_config("white", foreground="#ffffff")
        self.log_box.see(tk.END)

    def activate_window(self):
        try:
            window = gw.getWindowsWithTitle(window_title)[0]
            if window.isMinimized:
                window.restore()
            window.activate()
            return True
        except IndexError:
            self.log(f"[ERROR] Window '{window_title}' not found!", "red")
            return False

    def refresh_omnitracker(self):
        if self.activate_window():
            time.sleep(0.5)
            pyautogui.click(self.click_x, self.click_y)
            time.sleep(0.2)
            pyautogui.press('f5')
            self.log("🚀 OMNITRACKER Refreshed", "green")
            notifier.show_toast("OMNITRACKER Auto Refresh", "OMNITRACKER was refreshed successfully.", duration=3, threaded=True)

    def start_refresh(self):
        if self.running:
            messagebox.showinfo("Already Running", "The auto-refresh loop is already running.")
            return
        try:
            interval = int(self.interval_entry.get())
            if interval <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid positive number.")
            return

        self.running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.log(f"⏱ Starting refresh every {interval} minute(s)...", "cyan")
        threading.Thread(target=self.refresh_loop, args=(interval,), daemon=True).start()

    def stop_refresh(self):
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.log("🛑 Auto-refresh stopped.", "yellow")

    def refresh_loop(self, interval_minutes):
        while self.running:
            self.refresh_omnitracker()
            for _ in range(interval_minutes * 60):
                if not self.running:
                    break
                time.sleep(1)

    def get_coordinates(self):
        self.log("🎯 Move your mouse — capturing in 5 seconds...", "pink")
        self.coord_label.config(text="⏳ Waiting to capture...")
        self.root.update()

        def delayed_capture():
            time.sleep(5)
            x, y = pyautogui.position()
            self.click_x = x
            self.click_y = y
            self.coord_label.config(text=f"📌 Click Coordinates: ({x}, {y})")
            self.log(f"✅ Coordinates set to ({x}, {y})", "cyan")

        threading.Thread(target=delayed_capture, daemon=True).start()

    def stop(self):
        self.running = False
        self.log("🛑 Auto-refresh stopped.", "yellow")


if __name__ == "__main__":
    root = tk.Tk()
    app = OmniRefresherGUI(root)
    root.protocol("WM_DELETE_WINDOW", lambda: (app.stop(), root.destroy()))
    root.mainloop()