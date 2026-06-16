# ui/settings_frame.py

import customtkinter as ctk

from core.profile import ProfileManager


class SettingsFrame(ctk.CTkFrame):

    def __init__(
        self,
        master,
        on_profile_selected=None
    ):
        super().__init__(master)

        self.profile_manager = ProfileManager()
        self.on_profile_selected = on_profile_selected

        self.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            self,
            text="Профили",
            font=("Arial", 18, "bold")
        )
        self.title_label.pack(
            anchor="w",
            padx=10,
            pady=(10, 10)
        )

        self.profile_list = ctk.CTkOptionMenu(
            self,
            values=["Нет профилей"],
            command=self.profile_changed
        )
        self.profile_list.pack(
            fill="x",
            padx=10,
            pady=5
        )

        self.profile_name = ctk.CTkEntry(
            self,
            placeholder_text="Название профиля"
        )
        self.profile_name.pack(
            fill="x",
            padx=10,
            pady=5
        )

        self.create_button = ctk.CTkButton(
            self,
            text="Создать профиль",
            command=self.create_profile
        )
        self.create_button.pack(
            fill="x",
            padx=10,
            pady=5
        )

        self.delete_button = ctk.CTkButton(
            self,
            text="Удалить профиль",
            command=self.delete_profile
        )
        self.delete_button.pack(
            fill="x",
            padx=10,
            pady=5
        )

        self.refresh_profiles()

    def refresh_profiles(self):

        profiles = self.profile_manager.get_profiles()

        if not profiles:
            profiles = ["Нет профилей"]

        self.profile_list.configure(
            values=profiles
        )

        self.profile_list.set(
            profiles[0]
        )

    def profile_changed(
            self,
            profile_name
    ):

        if profile_name == "Нет профилей":
            return

        profile = self.profile_manager.load_profile(
            profile_name
        )

        if self.on_profile_selected:
            self.on_profile_selected(
                profile,
                profile_name
            )

    def create_profile(self):

        profile_name = (
            self.profile_name
            .get()
            .strip()
        )

        if not profile_name:
            return

        self.profile_manager.create_profile(
            profile_name
        )

        self.refresh_profiles()

        self.profile_name.delete(
            0,
            "end"
        )

    def delete_profile(self):

        profile_name = (
            self.profile_list.get()
        )

        if profile_name == "Нет профилей":
            return

        self.profile_manager.delete_profile(
            profile_name
        )

        self.refresh_profiles()