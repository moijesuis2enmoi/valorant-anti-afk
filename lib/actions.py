import time
import keyboard
import threading
import logging

from config import Keys

logger = logging.getLogger(__name__)

class Actions:
    _running_action = None
    _stop_flag = threading.Event()
    _last_toggle_time = 0
    _debounce_interval = 0.3

    @staticmethod
    def interruptible_sleep(duration, stop_flag, check_interval=0.1):
        """Sleep that can be interrupted by stop_flag"""
        end_time = time.time() + duration
        while time.time() < end_time:
            if stop_flag.is_set():
                return True
            time.sleep(min(check_interval, end_time - time.time()))
        return False

    @classmethod
    def _run_action(cls, action_func):
        logger.debug(f"Starting action: {cls._running_action}")
        try:
            action_func(cls._stop_flag)
        except Exception as e:
            logger.error(f"Error during action {cls._running_action}: {e}")
        finally:
            logger.debug(f"Exiting action: {cls._running_action}")
    
    @classmethod
    def toggle_action(cls, action_name, action_func):
        current_time = time.time()
        if current_time - cls._last_toggle_time < cls._debounce_interval:
            logger.debug(f"Debouncing toggle for {action_name}")
            return
        
        cls._last_toggle_time = current_time
        
        try:
            if cls._running_action:
                if cls._running_action == action_name:
                    logger.info(f"Stopping action: {action_name}")
                    cls._stop_flag.set()
                    time.sleep(0.2)
                    cls._running_action = None
                    logger.debug("Action stopped successfully")
                return
            
            logger.info(f"Starting new action: {action_name}")
            cls._stop_flag.clear()
            cls._running_action = action_name
            thread = threading.Thread(target=cls._run_action, args=(action_func,))
            thread.daemon = True
            thread.start()
            logger.debug("Action thread started successfully")
        except Exception as e:
            logger.error(f"Error toggling action {action_name}: {e}")
    
    @staticmethod
    def afk_1(stop_flag):
        keyboard.press(Keys.FORWARD)
        try:
            while not stop_flag.is_set():
                if Actions.interruptible_sleep(0.5, stop_flag):
                    break
        finally:
            keyboard.release("z")

    @staticmethod
    def afk_2(stop_flag):
        while not stop_flag.is_set():
            for touche in [Keys.FORWARD, Keys.LEFT, Keys.BACKWARD, Keys.RIGHT]:
                keyboard.press(touche)
                if Actions.interruptible_sleep(0.5, stop_flag):
                    keyboard.release(touche)
                    return
                keyboard.release(touche)
                if Actions.interruptible_sleep(0.5, stop_flag):
                    return