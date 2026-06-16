# core/mapper.py

import time

import pydirectinput


class Mapper:

    def __init__(self):

        pydirectinput.FAILSAFE = False

        self.pressed = set()
        self.pulse_timers = {}

    def press(self, key):

        if key in self.pressed:
            return

        pydirectinput.keyDown(key)
        self.pressed.add(key)

    def release(self, key):

        if key not in self.pressed:
            return

        pydirectinput.keyUp(key)
        self.pressed.remove(key)

    def tap(self, key):

        pydirectinput.press(key)

    def release_all(self):

        for key in list(self.pressed):

            try:
                pydirectinput.keyUp(key)
            except:
                pass

        self.pressed.clear()

    def update(
        self,
        profile,
        wheel_state
    ):

        bindings = profile.get(
            "bindings",
            []
        )

        deadzone = (
            profile
            .get("settings", {})
            .get("deadzone", 0.10)
        )

        for binding in bindings:

            source = binding.get(
                "source",
                {}
            )

            target = binding.get(
                "target",
                {}
            )

            key = target.get("key")

            if not key:
                continue

            source_type = source.get(
                "type"
            )

            if source_type == "button":
                self.handle_button(
                    binding,
                    wheel_state,
                    key
                )

            elif source_type == "axis":
                self.handle_axis(
                    binding,
                    wheel_state,
                    key,
                    deadzone
                )

    def handle_button(
        self,
        binding,
        wheel_state,
        key
    ):

        index = (
            binding["source"]
            ["index"]
        )

        buttons = wheel_state.get(
            "buttons",
            []
        )

        if index >= len(buttons):
            return

        if buttons[index]:
            self.press(key)
        else:
            self.release(key)

    def handle_axis(
        self,
        binding,
        wheel_state,
        key,
        deadzone
    ):

        source = binding["source"]

        axis_index = source["index"]

        axes = wheel_state.get(
            "axes",
            []
        )

        if axis_index >= len(axes):
            return

        value = axes[axis_index]

        direction = source.get(
            "direction"
        )

        if direction == "left":

            active = (
                value <
                -binding.get(
                    "trigger",
                    deadzone
                )
            )

            if active:
                self.press(key)
            else:
                self.release(key)

            return

        if direction == "right":

            active = (
                value >
                binding.get(
                    "trigger",
                    deadzone
                )
            )

            if active:
                self.press(key)
            else:
                self.release(key)

            return

        mode = binding.get(
            "mode",
            "hold"
        )

        trigger = binding.get(
            "trigger",
            0.30
        )

        strength = abs(value)

        if strength < trigger:

            self.release(key)

            if key in self.pulse_timers:
                del self.pulse_timers[key]

            return

        if mode == "hold":

            self.press(key)

        elif mode == "pulse":

            self.handle_pulse(
                binding,
                key,
                strength
            )

    def handle_pulse(
        self,
        binding,
        key,
        strength
    ):

        pulse = binding.get(
            "pulse",
            {}
        )

        min_interval = pulse.get(
            "min_interval",
            0.25
        )

        max_interval = pulse.get(
            "max_interval",
            0.02
        )

        strength = min(
            max(strength, 0),
            1
        )

        interval = (
            min_interval -
            (
                min_interval -
                max_interval
            ) * strength
        )

        now = time.time()

        last = self.pulse_timers.get(
            key,
            0
        )

        if now - last >= interval:

            pydirectinput.press(key)

            self.pulse_timers[key] = now