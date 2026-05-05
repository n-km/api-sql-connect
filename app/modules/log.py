
import logging
from pydoc import writedoc
log = True
if (log):
    logInConsole = True
    logInFile = True

    logging.basicConfig(
        filename="../log/justA.log",
        level=logging.INFO,
        format='%(asctime)s - %(message)s'
    )

    def log_user_action(desc, email, exception):
        if exception:
            logging.info(f"{desc} - {email} | Exception: {exception}")
        else:
            logging.info(f"{desc} - {email}")

    def log(now: str, desc: str, email: str, exception: str = None):
        if (logInConsole):
            print(now, desc, email)
        if (logInFile):
            log_user_action(desc, email, exception)