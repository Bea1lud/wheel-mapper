# core/wheel.py

import pygame


class WheelManager:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()

        self.joystick = None

        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()

    @property
    def connected(self):
        return self.joystick is not None

    @property
    def name(self):
        if not self.connected:
            return "Не подключен"

        return self.joystick.get_name()

    def update(self):
        pygame.event.pump()

    def get_axes(self):
        if not self.connected:
            return []

        return [
            round(self.joystick.get_axis(i), 3)
            for i in range(self.joystick.get_numaxes())
        ]

    def get_buttons(self):
        if not self.connected:
            return []

        return [
            bool(self.joystick.get_button(i))
            for i in range(self.joystick.get_numbuttons())
        ]

    def get_hats(self):
        if not self.connected:
            return []

        return [
            self.joystick.get_hat(i)
            for i in range(self.joystick.get_numhats())
        ]

    def get_state(self):
        self.update()

        return {
            "name": self.name,
            "axes": self.get_axes(),
            "buttons": self.get_buttons(),
            "hats": self.get_hats()
        }

    def detect_input(self):

        self.update()

        if not self.connected:
            return None

        for i in range(
                self.joystick.get_numbuttons()
        ):

            if self.joystick.get_button(i):
                return {
                    "type": "button",
                    "index": i
                }

        for i in range(
                self.joystick.get_numaxes()
        ):

            value = self.joystick.get_axis(i)

            if value > 0.7:
                return {
                    "type": "axis",
                    "index": i,
                    "direction": "right"
                }

            if value < -0.7:
                return {
                    "type": "axis",
                    "index": i,
                    "direction": "left"
                }

        return None