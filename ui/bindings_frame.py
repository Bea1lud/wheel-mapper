# ui/bindings_frame.py

import customtkinter as ctk
import threading
import keyboard

from core.profile import ProfileManager


class BindingsFrame(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(master)

        self.profile = None
        self.profile_name = None
        self.profile_manager = ProfileManager()
        self.waiting_for_binding = False

        self.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            self,
            text="Бинды",
            font=("Arial", 18, "bold")
        )

        self.title_label.pack(
            anchor="w",
            padx=10,
            pady=(10, 10)
        )

        self.bindings_container = ctk.CTkScrollableFrame(
            self,
            height=300
        )

        self.bindings_container.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=5
        )

        self.add_button = ctk.CTkButton(
            self,
            text="+ Добавить бинд",
            command=self.add_binding
        )

        self.add_button.pack(
            fill="x",
            padx=10,
            pady=(5, 10)
        )

    def load_profile(
            self,
            profile,
            profile_name
    ):

        self.profile = profile
        self.profile_name = profile_name

        self.refresh()

    def refresh(self):

        for widget in self.bindings_container.winfo_children():
            widget.destroy()

        if not self.profile:
            return

        bindings = self.profile.get(
            "bindings",
            []
        )

        if not bindings:

            label = ctk.CTkLabel(
                self.bindings_container,
                text="Нет биндов"
            )

            label.pack(
                anchor="w",
                padx=5,
                pady=5
            )

            return

        for index, binding in enumerate(bindings):

            self.create_binding_row(
                index,
                binding
            )

    def create_binding_row(
        self,
        index,
        binding
    ):

        row = ctk.CTkFrame(
            self.bindings_container
        )

        row.pack(
            fill="x",
            padx=5,
            pady=3
        )

        source = self.format_source(
            binding.get(
                "source",
                {}
            )
        )

        target = (
            binding
            .get("target", {})
            .get("key", "?")
        )

        label = ctk.CTkLabel(
            row,
            text=f"{source}  →  {target}",
            anchor="w"
        )

        label.pack(
            side="left",
            padx=10,
            pady=8
        )

        delete_btn = ctk.CTkButton(
            row,
            text="✕",
            width=35
        )

        delete_btn.pack(
            side="right",
            padx=5
        )

    def format_source(
        self,
        source
    ):

        source_type = source.get(
            "type"
        )

        if source_type == "button":

            return (
                f"Button "
                f"{source.get('index', 0)}"
            )

        if source_type == "axis":

            axis = source.get(
                "index",
                0
            )

            direction = source.get(
                "direction"
            )

            if direction:

                return (
                    f"Axis {axis} "
                    f"{direction}"
                )

            return (
                f"Axis {axis}"
            )

        return "Unknown"

    def add_binding(self):

        if not self.profile:
            return

        self.waiting_for_binding = True

    def binding_wizard(self):

        wheel = (
            self.master.master.wheel
        )

        source = None

        while source is None:
            source = wheel.detect_input()

        key = keyboard.read_key()

        binding = {
            "source": source,
            "target": {
                "key": key
            }
        }

        self.profile["bindings"].append(
            binding
        )

        self.profile_manager.save_profile(
            self.profile_name,
            self.profile
        )

        self.after(
            0,
            self.refresh
        )