import sys
from time import sleep
import customtkinter as ctk
import subprocess
import threading
from threading import Thread
import os

from config_manager import JsonTwin
from gui_elements import (
    SmallButton,
    NormalButton,
    BigButton,
    Entry,
    SmallLabel,
    BigLabel,
)

# import connection_check, preparator, automator, enterer

# --- INITIALIZATION ---
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ctk.set_appearance_mode("light")
# ctk.set_default_color_theme("blue")


class AutomatorGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        # self.iconbitmap("components/icon.ico")
        self.title("Автоматизатор EMIS v2.7.2")
        self.geometry("850x600")
        # self.resizable(False, False)
        self.minsize(700, 600)

        # Layout Configuration: Sidebar and Main Content
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=5)

        # --- SIDEBAR (Navigation & Branding) ---
        self.sidebar = ctk.CTkFrame(self, corner_radius=0)
        self.sidebar.pack(side="left", fill="both", expand=True)

        self.logo = ctk.CTkLabel(
            self.sidebar,
            text="EMIS AUTOMATOR",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.logo.pack(padx=20, pady=(50, 40))

        # Login
        self.credentials_container = ctk.CTkFrame(self.sidebar)
        self.credentials_container.pack()

        self.login_entry: Entry = Entry(
            self.credentials_container, placeholder_text="Login"
        )
        self.login_entry.pack()

        self.password_entry: Entry = Entry(
            self.credentials_container, placeholder_text="Password"
        )
        self.password_entry.pack(after=self.login_entry)

        self.save_credentials_button: SmallButton = SmallButton(
            self.credentials_container, text="Save"
        )
        self.save_credentials_button.pack(after=self.password_entry)

        self.status_indicator = SmallLabel(
            self.sidebar, text="● System Ready", text_color="gray"
        )
        self.status_indicator.pack(padx=20, pady=10)

        self.mode_switch = ctk.CTkOptionMenu(
            self.sidebar, values=["План предмета", "План группы"]
        )
        self.mode_switch.set("План предмета")
        self.mode_switch.pack(padx=20, pady=10)

        self.update_button = NormalButton(
            self.sidebar,
            text="UPDATE",
            command=self.update,
        )
        self.update_button.pack(anchor="center", side="bottom", padx=20, pady=(10, 30))

        self.relaunch_button = NormalButton(
            self.sidebar,
            text="RELAUNCH",
            command=self.relaunch,
        )
        self.relaunch_button.pack(anchor="center", side="bottom", padx=20, pady=10)

        # --- MAIN PANEL ---
        self.main_container = ctk.CTkFrame(self, corner_radius=15)
        self.main_container.pack(
            side="right", padx=20, pady=20, fill="both", expand=True
        )
        self.main_container.grid_columnconfigure(0, weight=1)

        # Header
        self.header = BigLabel(
            self.main_container,
            text="Configuration & Control",
        )
        self.header.grid(row=0, column=0, pady=(20, 10))

        # --- OPTIONS SECTION (De-stepped inputs) ---
        self.credentials_json = JsonTwin("credentials.json")
        self.current_settings = JsonTwin("current_settings.json")
        self.saves = JsonTwin("user_input_memory.json", is_dict=False)
        try:
            if self.saves.length() == 0:
                raise Exception
            self.current_settings = self.saves(-1)
        except Exception:
            self.default_settings = JsonTwin("default.json")
            self.default_settings_dict: dict = self.default_settings.get()
            self.current_settings = JsonTwin(
                self.default_settings_dict["current_settings.json"]
            )
            self.saves.set(0, self.current_settings.get())
        self.options_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.options_frame.grid(row=2, column=0, padx=40, pady=10)
        self.options_frame_row_counter = 1

        # --- CONSOLE OUTPUT (Replaces the CMD window) ---
        self.console_box = ctk.CTkTextbox(
            self.main_container, height=250, font=("Consolas", 12)
        )
        self.console_box.grid(row=2, column=0, padx=20, pady=20)
        self.log("System initialized. Ready to automate.")

        # --- ACTION BUTTON ---
        self.run_button: ctk.CTkButton = BigButton(
            self.main_container,
            text="START AUTOMATION",
            command=self.start_automation_thread,
        )
        self.stop_button: ctk.CTkButton = BigButton(
            self.main_container,
            text="STOP AUTOMATION",
            fg_color="red",
            command=self.stop_automation_thread,
        )
        
        self.run_button.grid(row=3, column=0, pady=(0, 20))

        # Background activities
        Thread(target=self.cycle, args=(lambda: self.save_settings(), 5), daemon=True).start()

    def update(self): ...

    def cycle(self, function: callable, interval: int = 5, end_after: int = None):
        while True:
            function()

    def log(self, message):
        """Adds text to the internal console box."""
        self.console_box.insert("end", f"> {message}\n")
        self.console_box.see("end")

    def relaunch(self):
        # """Relaunches the application."""
        concur = subprocess.Popen([sys.executable, __file__])
        sleep(0.5)
        if concur.poll() is None:
            self.destroy()

    def save_settings(self):
        """Saves the current settings to a JSON file."""
        self.current_settings.set("automation_mode", self.mode_switch.get())

    def start_automation_thread(self):
        """Runs the scripts in a background thread to keep the GUI from freezing."""

        def print(message):
            self.log(message)

        self.save_settings()
        self.run_button = self.stop_button
        self.status_indicator.configure(text="● Running...", text_color="yellow")
        self.automation = Thread(target=self.run_scripts, daemon=True)
        while self.automation.is_alive():
            sleep(3)
        sleep(3)
        self.run_button.configure(state=self.run_button_default)

    def stop_automation_thread(self):
        """Stops the automation thread."""
        self.run_button.configure(state="disabled", text="STOPPING...")
        self.status_indicator.configure(text="● Stopping...", text_color="yellow")
        self.automation.stop()

    def run(self, script): ...

    def run_scripts(self):
        """The core logic migrated from .cmd file."""

        python = "components/python314/python"
        pythonw = "start \"\" components/python314/pythonw"

        def print(message):
            self.log(message)

        try:
            # 1. Internet Check
            self.log("Checking internet connection...")
            subprocess.run(
                [pythonw, "components/connection_check.py"], capture_output=True
            )

            # 2. Playwright Install
            self.log("Preparing components (Playwright)...")
            subprocess.run(
                [python, "-m", "playwright", "install", "chromium"], capture_output=True
            )

            # 3. Login
            self.log("Preparing other stuff...")
            result = subprocess.run(
                [pythonw, "components/preparator.py"], capture_output=True
            )

            if result.returncode == 0:
                self.log("Prepared successfully!")
                # Determine which script to run based on the UI choice
                mode = self.mode_switch.get()
                if mode == "План предмета":
                    subprocess.run(
                        [pythonw, "components/automator.py"], capture_output=True
                    )
                else:
                    subprocess.run(
                        [pythonw, "components/enterer.py"], capture_output=True
                    )

                self.log("Process complete.")
                self.status_indicator.configure(text="● Success", text_color="green")
            else:
                self.log("Error: Preparation failed.")
                self.status_indicator.configure(text="● Failed", text_color="red")

        except Exception as e:
            self.log(f"System Error: {str(e)}")
            self.status_indicator.configure(text="● Error", text_color="red")

        self.run_button.configure(state=self.run_button_default)


def main():
    app = AutomatorGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
