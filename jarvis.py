import os
import sys
import time
import threading
import subprocess
from tkinter import Tk, Canvas, Label, Frame, Button, StringVar, END
from tkinter import ttk

try:
    import pyttsx3
except Exception:
    pyttsx3 = None

try:
    import psutil
except Exception:
    psutil = None


class JarvisApp(Tk):
    def __init__(self):
        super().__init__()
        self.title("JARVIS")
        self.geometry("1400x900")
        self.minsize(1200, 780)
        self.configure(bg="#040b16")

        self.iconphoto(False, None)

        self.current_mode = "ONLINE"
        self.emergency_number = "+15551234567"
        self.boss_name = "Boss"
        self.native_voice_enabled = False
        self.voice_engine = None

        self.setup_voice()
        self.build_ui()
        self.start_background_tasks()
        self.speak("Good evening, Boss. JARVIS online and ready.")

    def setup_voice(self):
        if pyttsx3 is not None:
            try:
                self.voice_engine = pyttsx3.init()
                self.voice_engine.setProperty("rate", 165)
                voices = self.voice_engine.getProperty("voices")
                if voices:
                    for voice in voices:
                        name = (voice.name or "").lower()
                        if "david" in name or "zira" in name or "aria" in name:
                            self.voice_engine.setProperty("voice", voice.id)
                            break
                self.native_voice_enabled = True
            except Exception:
                self.native_voice_enabled = False
                self.voice_engine = None

    def speak(self, text):
        if not text:
            return
        if self.voice_engine is not None:
            try:
                self.voice_engine.say(text)
                self.voice_engine.runAndWait()
                return
            except Exception:
                pass

        try:
            if os.name == "nt":
                import winsound
                winsound.Beep(900, 180)
        except Exception:
            pass

        print(f"JARVIS: {text}")

    def build_ui(self):
        self.title_bar = Frame(self, bg="#071521", height=70)
        self.title_bar.pack(fill="x", padx=0, pady=0)

        self.lbl_time = Label(
            self.title_bar,
            text="--:--:--",
            fg="#b7ebff",
            bg="#071521",
            font=("Segoe UI", 22, "bold"),
        )
        self.lbl_time.pack(side="left", padx=28, pady=14)

        self.lbl_status = Label(
            self.title_bar,
            text="SYSTEM ONLINE",
            fg="#8af0a7",
            bg="#071521",
            font=("Segoe UI", 16, "bold"),
        )
        self.lbl_status.pack(side="right", padx=28, pady=14)

        self.center_frame = Frame(self, bg="#040b16")
        self.center_frame.pack(fill="both", expand=True, padx=30, pady=10)

        self.title_label = Label(
            self.center_frame,
            text="JARVIS",
            fg="#7fe7ff",
            bg="#040b16",
            font=("Segoe UI", 52, "bold"),
            pady=20,
        )
        self.title_label.pack(anchor="center")

        self.canvas = Canvas(
            self.center_frame,
            width=620,
            height=360,
            bg="#040b16",
            highlightthickness=0,
        )
        self.canvas.pack(anchor="center", pady=10)

        self.draw_brain()

        self.card_frame = Frame(self.center_frame, bg="#040b16")
        self.card_frame.pack(anchor="center", pady=10)

        self.cards = []
        for label, value in [
            ("Core", "STABLE"),
            ("Memory", "READY"),
            ("Voice", "ACTIVE"),
            ("Threat", "LOW"),
        ]:
            card = Frame(self.card_frame, bg="#0d1b2a", bd=1, relief="solid")
            card.grid(row=0, column=len(self.cards), padx=10, pady=5, ipadx=18, ipady=12)
            card_label = Label(card, text=label, fg="#9db7ca", bg="#0d1b2a", font=("Segoe UI", 14))
            card_label.pack(pady=(10, 2))
            card_value = Label(card, text=value, fg="#dff8ff", bg="#0d1b2a", font=("Segoe UI", 20, "bold"))
            card_value.pack(pady=(0, 10))
            self.cards.append((card, card_label, card_value))

        self.nav_frame = Frame(self.center_frame, bg="#040b16")
        self.nav_frame.pack(anchor="center", pady=16)

        for text in ["HOME", "TASKS", "AUTO", "EMERGENCY"]:
            btn = Button(
                self.nav_frame,
                text=text,
                bg="#0a1f2f",
                fg="#8ad5ff",
                activebackground="#123b59",
                activeforeground="#dff8ff",
                bd=1,
                relief="solid",
                font=("Segoe UI", 11, "bold"),
                width=12,
                height=1,
                command=lambda value=text: self.on_nav_click(value),
            )
            btn.pack(side="left", padx=8)

        self.bottom_panel = Frame(self.center_frame, bg="#040b16")
        self.bottom_panel.pack(anchor="center", pady=12)

        self.action_btns = []
        actions = [
            ("Open Browser", self.open_browser),
            ("Open Notepad", self.open_notepad),
            ("Emergency Call", self.trigger_emergency),
            ("Status", self.status_report),
        ]
        for text, command in actions:
            btn = Button(
                self.bottom_panel,
                text=text,
                bg="#0b2238",
                fg="#dff8ff",
                activebackground="#123b59",
                activeforeground="#ffffff",
                bd=1,
                relief="solid",
                font=("Segoe UI", 11, "bold"),
                width=16,
                command=command,
            )
            btn.pack(side="left", padx=10)
            self.action_btns.append(btn)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_nav_click(self, value):
        if value == "EMERGENCY":
            self.trigger_emergency()
            return
        text = {
            "HOME": "Home system online, Boss.",
            "TASKS": "All tasks synchronized.",
            "AUTO": "Automation protocols ready.",
        }.get(value, "System online.")
        self.speak(text)
        self.lbl_status.config(text=f"{value} ACTIVE")

    def draw_brain(self):
        self.canvas.delete("all")
        cx = 310
        cy = 180
        radius = 120

        glow = self.canvas.create_oval(
            cx - radius - 22,
            cy - radius - 18,
            cx + radius + 22,
            cy + radius + 18,
            outline="#7fe7ff",
            width=3,
            stipple="gray25",
            fill="",
        )

        inner = self.canvas.create_oval(
            cx - radius,
            cy - radius,
            cx + radius,
            cy + radius,
            outline="#9feeff",
            width=2,
            fill="#061827",
            stipple="gray50",
        )

        brain_lines = [
            (0, -60, 80, -30),
            (0, -60, -80, -30),
            (0, -20, 90, 0),
            (0, -20, -90, 0),
            (0, 25, 70, 35),
            (0, 25, -70, 35),
            (0, 75, 60, 50),
            (0, 75, -60, 50),
        ]

        for x1, y1, x2, y2 in brain_lines:
            self.canvas.create_line(
                cx + x1,
                cy + y1,
                cx + x2,
                cy + y2,
                fill="#7fe7ff",
                width=3,
                smooth=True,
            )

        for a, b in [(0, 0), (-40, 40), (40, 40), (-90, 90), (90, 90)]:
            self.canvas.create_oval(
                cx + a - 12,
                cy + b - 12,
                cx + a + 12,
                cy + b + 12,
                outline="#7fe7ff",
                width=2,
                fill="",
            )

        self.canvas.create_text(cx, cy + 10, text="AI", fill="#dff8ff", font=("Segoe UI", 20, "bold"))
        self.canvas.tag_lower(glow)
        self.canvas.tag_lower(inner)

    def animate_brain(self):
        self.draw_brain()
        try:
            self.after(1200, self.animate_brain)
        except Exception:
            pass

    def start_background_tasks(self):
        self.update_clock()
        self.animate_brain()
        self.update_system_status()

    def update_clock(self):
        from datetime import datetime
        current = datetime.now().strftime("%H:%M:%S")
        self.lbl_time.config(text=current)
        self.after(1000, self.update_clock)

    def update_system_status(self):
        if psutil is not None:
            try:
                cpu = psutil.cpu_percent(interval=None)
                ram = psutil.virtual_memory().percent
                self.cards[0][2].config(text=f"{cpu}%")
                self.cards[1][2].config(text=f"{ram}%")
            except Exception:
                pass
        self.after(2500, self.update_system_status)

    def status_report(self):
        text = "All systems stable, Boss. JARVIS is online and ready to assist."
        self.speak(text)

    def open_notepad(self):
        try:
            if os.name == "nt":
                os.startfile("notepad.exe")
                self.speak("Notepad opened, Boss.")
            else:
                subprocess.Popen(["notepad" if os.name == "nt" else "gedit"])
                self.speak("Application launched, Boss.")
        except Exception as exc:
            self.speak("Unable to launch notepad, Boss.")
            print(exc)

    def open_browser(self):
        try:
            url = "https://www.google.com"
            if os.name == "nt":
                os.startfile(url)
            else:
                import webbrowser
                webbrowser.open(url)
            self.speak("Browser opened, Boss.")
        except Exception:
            self.speak("Unable to open browser, Boss.")

    def trigger_emergency(self):
        number = self.emergency_number
        self.speak("Emergency protocol engaged. Initiating emergency call, Boss.")
        try:
            if os.name == "nt":
                subprocess.Popen(["cmd", "/c", f"start ms-call:tel:{number}"])
            else:
                subprocess.Popen(["open", f"tel:{number}"])
            self.lbl_status.config(text="EMERGENCY ACTIVE")
            self.speak("Emergency call initialized.")
        except Exception as exc:
            self.speak("Emergency call failed. Please verify the number. ")
            print(exc)

    def on_close(self):
        self.speak("Shutting down JARVIS. Good night, Boss.")
        self.destroy()


if __name__ == "__main__":
    app = JarvisApp()
    app.mainloop()
