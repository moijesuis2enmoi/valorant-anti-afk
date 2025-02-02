import keyboard
import logging

from lib.actions import Actions

logger = logging.getLogger(__name__)

class EventHandler:
    def __init__(self):
        self.setup_hotkeys()

    def setup_hotkeys(self):
        keyboard.add_hotkey('f2', lambda: Actions.toggle_action('afk_1', Actions.afk_1))
        keyboard.add_hotkey('f3', lambda: Actions.toggle_action('afk_2', Actions.afk_2))
        keyboard.add_hotkey('f12', lambda: exit())
        logger.info("Raccourcis clavier initialisés")

    @staticmethod
    def run():
        try:
            EventHandler().setup_hotkeys()
            logger.info("Event handler started")
            print("Welcome to the Valorant anti-afk by @moijesuis2enmoi (https://github.com/moijesuis2enmoi)")
            print("Press F2 to start/stop AFK 1 -> Move forward")
            print("Press F3 to start/stop AFK 2 -> Move in square")
            print("Press F12 to exit")
            print("Enjoy!")
            keyboard.wait()
        except Exception as e:
            logger.error(f"An error occurred: {e}")