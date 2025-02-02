import logging
from lib.event_handler import EventHandler

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    try:
        logger.info("Starting event handler")
        event_handler = EventHandler.run()
    except Exception as e:
        logger.error(f"An error occurred: {e}")