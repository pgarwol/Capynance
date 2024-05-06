from services import read_user_from_db


class Session:
    def __init__(self, user_id):
        self.logged_user = read_user_from_db(id=user_id)


# Initialized after login
# Terminated after log out
# @TODO: Settings mechanics: dark mode, lang etc.
