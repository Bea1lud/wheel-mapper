# core/profile.py

import json
import os

from core.config import Config


class ProfileManager:

    def __init__(self):
        Config.create_folders()

    def get_profile_path(self, profile_name):

        if not profile_name.endswith(".json"):
            profile_name += ".json"

        return os.path.join(
            Config.PROFILES_DIR,
            profile_name
        )

    def create_profile(self, profile_name):

        profile = {
            "name": profile_name,

            "settings": {
                "deadzone": 0.10,
                "smoothing": 0.20
            },

            "bindings": []
        }

        self.save_profile(
            profile_name,
            profile
        )

        return profile

    def save_profile(
        self,
        profile_name,
        profile
    ):

        path = self.get_profile_path(
            profile_name
        )

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                profile,
                file,
                indent=4,
                ensure_ascii=False
            )

    def load_profile(
        self,
        profile_name
    ):

        path = self.get_profile_path(
            profile_name
        )

        if not os.path.exists(path):
            return self.create_profile(
                profile_name
            )

        try:

            with open(
                path,
                "r",
                encoding="utf-8"
            ) as file:

                return json.load(file)

        except Exception:

            return self.create_profile(
                profile_name
            )

    def delete_profile(
        self,
        profile_name
    ):

        path = self.get_profile_path(
            profile_name
        )

        if os.path.exists(path):
            os.remove(path)

    def get_profiles(self):

        profiles = []

        for file in os.listdir(
            Config.PROFILES_DIR
        ):

            if file.endswith(".json"):

                profiles.append(
                    file.replace(
                        ".json",
                        ""
                    )
                )

        return sorted(profiles)

    # ------------------------
    # БИНДЫ
    # ------------------------

    def add_binding(
        self,
        profile,
        binding
    ):

        profile["bindings"].append(
            binding
        )

        return profile

    def remove_binding(
        self,
        profile,
        index
    ):

        if (
            0 <= index <
            len(profile["bindings"])
        ):

            profile["bindings"].pop(
                index
            )

        return profile