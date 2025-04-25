import logging
from database.connect_database import insert_log

# Configure logging
logging.basicConfig(
    filename="features/app.log",
    level=logging.INFO,  
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def log_action(user_email, action, log_level="info"):
    try:
        log_message = f"{user_email} - {action}"

        if log_level.lower() == "info":
            logging.info(log_message)
        elif log_level.lower() == "warning":
            logging.warning(log_message)
        else:
            logging.error(log_message)

        if user_email:
            insert_log(user_email, log_level, action)
        else:
            insert_log(log_level, action, user_email="")
    except Exception as e:
        logging.error(f"Failed to log action for '{user_email}'. Error: {e}")

