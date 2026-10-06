import math
import time
from datetime import datetime
import tkinter as tk
from tkinter import ttk


class JarvisDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("JARVIS")
        self.geometry("1600x920")
        self.minsize(1400, 850)
        self.configure(bg="#031b2b")
        self.overrideredirect(False)

        self.dark = "#031b2b"
        self.deep = "#061e34"
        self.panel = "#0b2438"
        self.panel_alt = "#0d2a44"
        self.line = "#1a4d73"
        self.accent = "#6fe9ff"
        self.accent2 = "#46d9ff"
        self.green = "#6ef7bf"
        self.warn = "#ffbf5f"
        self.text = "#dff9ff"
        self.text2 = "#8bb7d0"

        self.sidebar_items = [
            "Command Center",
            "AI Core",
            "Agents",
            "Tasks",
            "Calendar",
            "Memory",
            "Conversations",
            "Knowledge Base",
            "Tools & Skills",
            "Workflows",
        ]

        self.style = {
            "bg": self.dark,
            "fg": self.text,
            "font_title": ("Segoe UI", 36, "bold"),
            "font_h1": ("Segoe UI", 22, "bold"),
            "font_h2": ("Segoe UI", 16, "bold"),
            "font_small": ("Segoe UI", 12),
            "font_med": ("Segoe UI", 14),
        }

        self.build_layout()
        self.bind("<Configure>", self.on_resize)
        self.update_clock()
        self.animate()

    def build_layout(self):
        self.background = tk.Canvas(self, bg=self.dark, highlightthickness=0)
        self.background.pack(fill="both", expand=True)

        self.sidebar = tk.Frame(self.background, bg="#061b2d", width=220, height=920)
        self.sidebar.place(x=0, y=0)

        self.brand = tk.Label(
            self.sidebar,
            text="JARVIS",
            bg="#061b2d",
            fg=self.accent,
            font=("Segoe UI", 24, "bold"),
        )
        self.brand.place(x=24, y=20)

        self.brand_dot = tk.Canvas(self.sidebar, width=18, height=18, bg="#061b2d", highlightthickness=0)
        self.brand_dot.place(x=150, y=28)
        self.brand_dot.create_oval(2, 2, 16, 16, outline=self.accent, width=2, fill="")
        self.brand_dot.create_oval(5, 5, 13, 13, outline=self.accent, width=2, fill="")

        self.sidebar_items_frame = tk.Frame(self.sidebar, bg="#061b2d")
        self.sidebar_items_frame.place(x=18, y=90)

        for idx, item in enumerate(self.sidebar_items):
            color = self.accent if idx == 0 else self.text2
            active = "#0f324a" if idx == 0 else "#061b2d"
            label = tk.Label(
                self.sidebar_items_frame,
                text=item,
                bg=active,
                fg=color,
                font=("Segoe UI", 12),
                anchor="w",
                padx=16,
                pady=10,
                width=18,
                justify="left",
            )
            label.grid(row=idx, column=0, sticky="ew", pady=2)

        self.voice_bar = tk.Frame(self.sidebar, bg="#061b2d")
        self.voice_bar.place(x=18, y=710)
        tk.Label(self.voice_bar, text="VOICE STATUS", bg="#061b2d", fg=self.text2, font=("Segoe UI", 11, "bold")).pack(anchor="w")
        self.voice_wave = tk.Canvas(self.voice_bar, width=150, height=36, bg="#061b2d", highlightthickness=0)
        self.voice_wave.pack(anchor="w", pady=(8, 0))
        self.voice_wave_lines = []
        for i in range(12):
            item = self.voice_wave.create_rectangle(4 + i * 10, 22, 10 + i * 10, 22, fill=self.accent, outline="")
            self.voice_wave_lines.append(item)

        self.voice_status = tk.Label(self.voice_bar, text="Listening...", bg="#061b2d", fg=self.accent, font=("Segoe UI", 11, "bold"), padx=4)
        self.voice_status.pack(anchor="w")

        self.mic_button = tk.Button(
            self.sidebar,
            text="Tap to Speak",
            bg="#0b2339",
            fg=self.accent,
            activebackground="#103150",
            activeforeground="#dff9ff",
            font=("Segoe UI", 12, "bold"),
            bd=1,
            relief="solid",
            width=15,
            height=2,
            command=self.speak_prompt,
        )
        self.mic_button.place(x=18, y=790)

        self.focus_button = tk.Button(
            self.sidebar,
            text="Focus Mode",
            bg="#0b2339",
            fg=self.text,
            activebackground="#103150",
            activeforeground="#dff9ff",
            font=("Segoe UI", 10, "bold"),
            bd=1,
            relief="solid",
            width=15,
            height=2,
            command=self.focus_shortcut,
        )
        self.focus_button.place(x=18, y=850)

        self.main = tk.Frame(self.background, bg="#071b2e")
        self.main.place(x=220, y=0, width=1380, height=920)

        self.topbar = tk.Frame(self.main, bg="#071b2e")
        self.topbar.place(x=30, y=20, width=1290, height=60)

        self.date_label = tk.Label(self.topbar, text="Monday, 15 June 2026", bg="#071b2e", fg=self.text2, font=("Segoe UI", 13))
        self.date_label.place(x=0, y=14)

        self.time_label = tk.Label(self.topbar, text="11:18:21 am", bg="#071b2e", fg=self.text, font=("Segoe UI", 20, "bold"))
        self.time_label.place(x=420, y=8)

        self.search_bar = tk.Frame(self.topbar, bg="#0b2137", height=40, width=300)
        self.search_bar.place(x=825, y=8)
        tk.Label(self.search_bar, text="Search...", bg="#0b2137", fg=self.text2, font=("Segoe UI", 12)).place(x=12, y=9)
        self.search_icon = tk.Label(self.search_bar, text="⌕", bg="#0b2137", fg=self.text2, font=("Segoe UI", 18)).place(x=258, y=5)

        self.top_icons = tk.Frame(self.topbar, bg="#071b2e")
        self.top_icons.place(x=1130, y=8)
        for i, char in enumerate(["◫", "◌", "◍", "◐", "◊"]):
            tk.Label(self.top_icons, text=char, bg="#071b2e", fg=self.text2, font=("Segoe UI", 15)).place(x=i*26, y=0)

        self.operator_label = tk.Label(self.topbar, text="Operator", bg="#071b2e", fg=self.text, font=("Segoe UI", 11))
        self.operator_label.place(x=1235, y=6)
        self.user_pill = tk.Label(self.topbar, text="Commander", bg="#0d2740", fg=self.accent, font=("Segoe UI", 10, "bold"), padx=12, pady=4)
        self.user_pill.place(x=1230, y=26)

        self.left_panel = tk.Frame(self.main, bg="#0a1d30", highlightbackground=self.line, highlightthickness=1)
        self.left_panel.place(x=30, y=95, width=320, height=250)
        tk.Label(self.left_panel, text="AI CORE OVERVIEW", bg="#0a1d30", fg=self.text2, font=("Segoe UI", 12, "bold")).place(x=18, y=15)

        sysinfo = [
            ("AI Core", "Active"),
            ("Memory", "3,380 Stored"),
            ("Voice", "Online"),
            ("Agents", "2 Running"),
            ("LLMs", "4 Connected"),
            ("System", "Optimal"),
        ]
        for row, (label, val) in enumerate(sysinfo):
            r = row // 2
            c = row % 2
            x = 18 + c * 143
            y = 48 + r * 48
            tk.Label(self.left_panel, text=label, bg="#0a1d30", fg=self.text2, font=("Segoe UI", 11)).place(x=x, y=y)
            tk.Label(self.left_panel, text=val, bg="#0a1d30", fg=self.text, font=("Segoe UI", 11, "bold")).place(x=x, y=y+18)

        self.center_arc = tk.Canvas(self.main, width=570, height=360, bg="#071b2e", highlightthickness=0)
        self.center_arc.place(x=370, y=110)
        self.orbit_items = []

        self.live_feed = tk.Frame(self.main, bg="#0a1d30", highlightbackground=self.line, highlightthickness=1)
        self.live_feed.place(x=980, y=95, width=350, height=310)
        tk.Label(self.live_feed, text="LIVE INTELLIGENCE FEED", bg="#0a1d30", fg=self.text2, font=("Segoe UI", 12, "bold")).place(x=18, y=16)
        self.live_feed_cards = [
            ("Meeting", "Info", "2 tasks are overdue"),
            ("Overdue", "Warn", "3 pull requests are awaiting review"),
            ("GitHub", "Tip", "Your deep-work block is 2-4 PM"),
            ("Focus", "Tip", "CPU usage at 15%"),
        ]
        cy = 52
        for title, tag, desc in self.live_feed_cards:
            card = tk.Frame(self.live_feed, bg="#0d243a", highlightbackground=self.line, highlightthickness=1)
            card.place(x=18, y=cy, width=312, height=52)
            tk.Label(card, text=title, bg="#0d243a", fg=self.text, font=("Segoe UI", 11, "bold")).place(x=8, y=8)
            tk.Label(card, text=tag, bg="#0d243a", fg=self.green if tag == "Info" else self.warn if tag == "Warn" else self.accent, font=("Segoe UI", 8, "bold")).place(x=220, y=6)
            tk.Label(card, text=desc, bg="#0d243a", fg=self.text2, font=("Segoe UI", 9)).place(x=8, y=26)
            cy += 58

        self.mid_bottom = tk.Frame(self.main, bg="#0a1d30", highlightbackground=self.line, highlightthickness=1)
        self.mid_bottom.place(x=30, y=360, width=320, height=250)
        tk.Label(self.mid_bottom, text="ACTIVE AGENTS", bg="#0a1d30", fg=self.text2, font=("Segoe UI", 12, "bold")).place(x=18, y=16)

        agent_cards = [
            ("Coing Agent", "Active"),
            ("Research Agent", "Active"),
            ("Memory Agent", "Standby"),
            ("Task Agent", "Standby"),
            ("System Agent", "Standby"),
        ]
        cx = 14
        cy = 50
        for i, (name, state) in enumerate(agent_cards):
            if i == 3:
                cx = 14
                cy = 140
            elif i == 4:
                cx = 150
                cy = 140
            agent = tk.Frame(self.mid_bottom, bg="#0d243a", highlightbackground=self.line, highlightthickness=1)
            agent.place(x=cx, y=cy, width=120, height=70)
            tk.Label(agent, text=name, bg="#0d243a", fg=self.text, font=("Segoe UI", 10, "bold")).place(x=8, y=8)
            tk.Label(agent, text=state, bg="#0d243a", fg=self.green if state == "Active" else self.text2, font=("Segoe UI", 9)).place(x=8, y=28)
            cx += 136

        self.timeline = tk.Frame(self.main, bg="#0a1d30", highlightbackground=self.line, highlightthickness=1)
        self.timeline.place(x=370, y=510, width=480, height=220)
        tk.Label(self.timeline, text="MISSION TIMELINE", bg="#0a1d30", fg=self.text2, font=("Segoe UI", 12, "bold")).place(x=18, y=16)

        tasks = [
            ("Daily Standup", "09:30", "Done"),
            ("Finalize HUD panel spacing", "12:00", "In 42 min"),
            ("Deep-work block: Voice pipeline", "12:20", "In 2h 4m"),
            ("Design review - Command Center VI", "04:30", "In 5h 12m"),
        ]
        y = 50
        for title, time_s, status in tasks:
            tk.Label(self.timeline, text=time_s, bg="#0a1d30", fg=self.text2, font=("Segoe UI", 9)).place(x=18, y=y)
            bar = tk.Frame(self.timeline, bg="#0d243a", highlightbackground=self.line, highlightthickness=1)
            bar.place(x=120, y=y-2, width=280, height=18)
            inner = tk.Frame(bar, bg=self.accent)
            inner.place(x=0, y=0, width=180 if status != "Done" else 260, height=18)
            tk.Label(self.timeline, text=title, bg="#0a1d30", fg=self.text, font=("Segoe UI", 9)).place(x=120, y=y+18)
            tk.Label(self.timeline, text=status, bg="#0a1d30", fg=self.green if status == "Done" else self.accent, font=("Segoe UI", 8)).place(x=408, y=y+2)
            y += 38

        self.quick = tk.Frame(self.main, bg="#0a1d30", highlightbackground=self.line, highlightthickness=1)
        self.quick.place(x=980, y=420, width=350, height=220)
        tk.Label(self.quick, text="QUICK COMMANDS", bg="#0a1d30", fg=self.text2, font=("Segoe UI", 12, "bold")).place(x=18, y=16)
        cmds = [
            "Start Task",
            "Open Calendar",
            "Start Voice Chat",
            "Run Workflow",
        ]
        py = 54
        for c in cmds:
            btn = tk.Button(self.quick, text=c, bg="#0d243a", fg=self.text, activebackground="#12395a", activeforeground=self.text, bd=1, relief="solid", width=22, height=1, command=lambda x=c: self.quick_reply(x))
            btn.place(x=18, y=py)
            py += 34

        self.monitor_panel = tk.Frame(self.main, bg="#0a1d30", highlightbackground=self.line, highlightthickness=1)
        self.monitor_panel.place(x=30, y=630, width=320, height=220)
        tk.Label(self.monitor_panel, text="SYSTEM MONITOR", bg="#0a1d30", fg=self.text2, font=("Segoe UI", 12, "bold")).place(x=18, y=18)

        self.cpu = tk.Canvas(self.monitor_panel, width=80, height=80, bg="#0a1d30", highlightthickness=0)
        self.cpu.place(x=22, y=56)
        self.ram = tk.Canvas(self.monitor_panel, width=80, height=80, bg="#0a1d30", highlightthickness=0)
        self.ram.place(x=118, y=56)
        self.disk = tk.Canvas(self.monitor_panel, width=80, height=80, bg="#0a1d30", highlightthickness=0)
        self.disk.place(x=214, y=56)

        tk.Label(self.monitor_panel, text="CPU", bg="#0a1d30", fg=self.text2, font=("Segoe UI", 10)).place(x=42, y=142)
        tk.Label(self.monitor_panel, text="RAM", bg="#0a1d30", fg=self.text2, font=("Segoe UI", 10)).place(x=142, y=142)
        tk.Label(self.monitor_panel, text="Disk", bg="#0a1d30", fg=self.text2, font=("Segoe UI", 10)).place(x=240, y=142)

        self.memory_panel = tk.Frame(self.main, bg="#0a1d30", highlightbackground=self.line, highlightthickness=1)
        self.memory_panel.place(x=370, y=740, width=330, height=130)
        tk.Label(self.memory_panel, text="MEMORY INSIGHTS", bg="#0a1d30", fg=self.text2, font=("Segoe UI", 12, "bold")).place(x=18, y=14)
        tk.Label(self.memory_panel, text="3,380", bg="#0a1d30", fg=self.text, font=("Segoe UI", 18, "bold")).place(x=18, y=40)
        tk.Label(self.memory_panel, text="Session Turns", bg="#0a1d30", fg=self.text2, font=("Segoe UI", 10)).place(x=20, y=72)
        tk.Label(self.memory_panel, text="22", bg="#0a1d30", fg=self.text, font=("Segoe UI", 18, "bold")).place(x=170, y=40)
        tk.Label(self.memory_panel, text="Tool Calls", bg="#0a1d30", fg=self.text2, font=("Segoe UI", 10)).place(x=170, y=72)

        self.llm_panel = tk.Frame(self.main, bg="#0a1d30", highlightbackground=self.line, highlightthickness=1)
        self.llm_panel.place(x=720, y=740, width=610, height=130)
        tk.Label(self.llm_panel, text="LLM STATUS", bg="#0a1d30", fg=self.text2, font=("Segoe UI", 12, "bold")).place(x=18, y=14)
        providers = [
            ("Claude", "Connected"),
            ("OpenAI", "Connected"),
            ("Gemini", "Connected"),
            ("OpenRouter", "Connected"),
        ]
        x = 18
        for provider, state in providers:
            p = tk.Frame(self.llm_panel, bg="#0d243a", highlightbackground=self.line, highlightthickness=1)
            p.place(x=x, y=46, width=118, height=58)
            tk.Label(p, text=provider, bg="#0d243a", fg=self.text, font=("Segoe UI", 10, "bold")).place(x=10, y=10)
            tk.Label(p, text=state, bg="#0d243a", fg=self.green, font=("Segoe UI", 8)).place(x=10, y=30)
            x += 130

        self.bottom_talk = tk.Frame(self.main, bg="#0a1d30", highlightbackground=self.line, highlightthickness=1)
        self.bottom_talk.place(x=30, y=850, width=1300, height=60)
        self.talk_field = tk.Label(self.bottom_talk, text="I am listening...", bg="#0a1d30", fg=self.text2, font=("Segoe UI", 12, "bold"), width=50, anchor="w")
        self.talk_field.place(x=20, y=14)
        self.talk_button = tk.Button(self.bottom_talk, text="Execute Briefing", bg="#0d3147", fg=self.accent, activebackground="#133c5d", activeforeground=self.text, bd=1, relief="solid", font=("Segoe UI", 10, "bold"), width=18, command=self.speak_prompt)
        self.talk_button.place(x=1100, y=12)

        self.draw_orbit()
        self.draw_gauges()

    def on_resize(self, event):
        pass

    def speak_prompt(self):
        self.voice_status.config(text="Listening...")
        self.talk_field.config(text="I am listening...")
        self.blink_voice()

    def focus_shortcut(self):
        self.voice_status.config(text="Focus mode")
        self.talk_field.config(text="Focus mode engaged, Boss.")

    def quick_reply(self, text):
        self.talk_field.config(text=f"{text} queued, Boss.")

    def update_clock(self):
        now = datetime.now()
        self.time_label.config(text=now.strftime("%I:%M:%S %p").lower())
        self.date_label.config(text=now.strftime("%A, %d %B %Y"))
        self.after(1000, self.update_clock)

    def blink_voice(self):
        for idx in range(12):
            h = 8 + (idx % 6) * 5
            self.voice_wave.coords(self.voice_wave_lines[idx], 4 + idx * 10, 22, 10 + idx * 10, 22 - h)
        self.after(250, lambda: self.reset_voice_wave())

    def reset_voice_wave(self):
        for idx in range(12):
            self.voice_wave.coords(self.voice_wave_lines[idx], 4 + idx * 10, 22, 10 + idx * 10, 22)

    def draw_orbit(self):
        self.center_arc.delete("all")
        cx = 285
        cy = 160
        radius = 120

        for i in range(2):
            self.center_arc.create_oval(cx - radius - 20 - i * 12, cy - radius - 10 - i * 12, cx + radius + 20 + i * 12, cy + radius + 10 + i * 12, outline="#1b6b9a", width=1)

        for angle in range(0, 360, 18):
            rad = math.radians(angle)
            x1 = cx + (radius + 8) * math.cos(rad)
            y1 = cy + (radius + 8) * math.sin(rad)
            x2 = cx + (radius + 26) * math.cos(rad)
            y2 = cy + (radius + 26) * math.sin(rad)
            self.center_arc.create_line(x1, y1, x2, y2, fill="#3dc7ff", width=1, dash=(3, 8))

        for y in range(-6, 7, 2):
            xoff = 50 * math.sin((y * 0.7))
            self.center_arc.create_line(cx + xoff - 90, cy + y * 8, cx + xoff + 90, cy + y * 8, fill="#32bfff", width=1, dash=(2, 10))

        outer = self.center_arc.create_oval(cx - radius, cy - radius, cx + radius, cy + radius, outline="#75ebff", width=2, fill="#071e32")
        inner = self.center_arc.create_oval(cx - radius * 0.82, cy - radius * 0.82, cx + radius * 0.82, cy + radius * 0.82, outline="#7fe9ff", width=2, fill="#071e32")
        self.orbit_items = [outer, inner]

        self.center_arc.create_text(cx, cy, text="JARVIS", fill="#7fe9ff", font=("Segoe UI", 30, "bold"))
        self.center_arc.create_text(cx, cy + 36, text="AI CORE", fill="#bfebff", font=("Segoe UI", 12, "bold"))
        self.center_arc.create_text(cx, cy + 58, text="v3.0.0", fill="#7fe9ff", font=("Segoe UI", 10, "bold"))

    def draw_gauges(self):
        self.draw_ring(self.cpu, 15, "#7ae8ff")
        self.draw_ring(self.ram, 54, "#7ae8ff")
        self.draw_ring(self.disk, 40, "#7ae8ff")

    def draw_ring(self, canvas, pct, color):
        canvas.delete("all")
        center = 40
        radius = 28
        canvas.create_oval(center - radius, center - radius, center + radius, center + radius, outline="#183a52", width=8)
        arc = canvas.create_arc(
            center - radius,
            center - radius,
            center + radius,
            center + radius,
            start=270,
            extent=-(pct / 100.0) * 360,
            outline=color,
            width=7,
            style="arc",
            capstyle="round",
        )
        canvas.create_text(center, center + 8, text=f"{pct}%", fill="#dff9ff", font=("Segoe UI", 12, "bold"))

    def animate(self):
        self.rotation = getattr(self, "rotation", 0)
        self.rotation += 1
        if hasattr(self, "center_arc"):
            self.center_arc.delete("all")
            self.draw_orbit()
        self.after(35, self.animate)


if __name__ == "__main__":
    app = JarvisDashboard()
    app.mainloop()
