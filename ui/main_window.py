# ui/main_window.py

import customtkinter as ctk

from core.wheel import WheelManager

from ui.settings_frame import SettingsFrame
from ui.bindings_frame import BindingsFrame


class MainWindow(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.wheel = WheelManager()

        self.title("WheelMapper")
        self.geometry("1000x650")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # -------------------
        # Левая панель
        # -------------------

        self.settings_frame = SettingsFrame(
            self,
            on_profile_selected=self.load_profile
        )

        self.settings_frame.grid(
            row=0,
            column=0,
            sticky="ns",
            padx=10,
            pady=10
        )

        # -------------------
        # Правая панель
        # -------------------

        self.right_frame = ctk.CTkFrame(self)

        self.right_frame.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(0, 10),
            pady=10
        )

        self.right_frame.grid_columnconfigure(
            0,
            weight=1
        )

        # -------------------
        # Руль
        # -------------------

        wheel_name = (
            self.wheel.name
            if self.wheel.connected
            else "Не подключен"
        )

        self.wheel_label = ctk.CTkLabel(
            self.right_frame,
            text=f"Руль: {wheel_name}",
            font=("Arial", 16, "bold")
        )

        self.wheel_label.pack(
            anchor="w",
            padx=15,
            pady=(15, 10)
        )

        # -------------------
        # Бинды
        # -------------------

        self.bindings_frame = BindingsFrame(
            self.right_frame
        )

        self.bindings_frame.pack(
            fill="x",
            padx=15,
            pady=10
        )

        # -------------------
        # Оси
        # -------------------

        self.axes_label = ctk.CTkLabel(
            self.right_frame,
            text="Оси"
        )

        self.axes_label.pack(
            anchor="w",
            padx=15
        )

        self.axes_text = ctk.CTkTextbox(
            self.right_frame,
            height=180
        )

        self.axes_text.pack(
            fill="x",
            padx=15,
            pady=(5, 15)
        )

        # -------------------
        # Кнопки
        # -------------------

        self.buttons_label = ctk.CTkLabel(
            self.right_frame,
            text="Кнопки"
        )

        self.buttons_label.pack(
            anchor="w",
            padx=15
        )

        self.buttons_text = ctk.CTkTextbox(
            self.right_frame
        )

        self.buttons_text.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(5, 15)
        )

        self.update_wheel()

    def load_profile(
            self,
            profile,
            profile_name
    ):

        self.bindings_frame.load_profile(
            profile,
            profile_name
        )

    def update_wheel(self):

        if self.wheel.connected:

            state = self.wheel.get_state()

            if self.bindings_frame.waiting_for_binding:

                source = self.wheel.detect_input()

                if source:
                    print("Поймано:", source)

                    self.bindings_frame.waiting_for_binding = False

            axes_text = "\n".join(
                [
                    f"Axis {i}: {value}"
                    for i, value
                    in enumerate(state["axes"])
                ]
            )

            self.axes_text.delete(
                "1.0",
                "end"
            )

            self.axes_text.insert(
                "1.0",
                axes_text
            )

            button_lines = []

            for i, value in enumerate(
                state["buttons"]
            ):
                button_lines.append(
                    f"Button {i}: {value}"
                )

            for i, value in enumerate(
                state["hats"]
            ):
                button_lines.append(
                    f"Hat {i}: {value}"
                )

            self.buttons_text.delete(
                "1.0",
                "end"
            )

            self.buttons_text.insert(
                "1.0",
                "\n".join(button_lines)
            )

        self.after(
            50,
            self.update_wheel
        )