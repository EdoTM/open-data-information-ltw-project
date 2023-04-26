import os
import sqlite3


class Database:
    __INSTANCE = None

    @staticmethod
    def get_instance():
        if Database.__INSTANCE is None:
            Database.__INSTANCE = Database()
        return Database.__INSTANCE

    def __init__(self, db_dir=None):
        if db_dir is None:
            db_dir = os.path.join(os.path.dirname(__file__), '../db/opinf.db')
        self.db_dir = db_dir
        self.users_headers = self.get_users_headers()
        print(self.db_dir)

    def __store_user(self, email, username, password_hash, birthday):
        with sqlite3.connect(self.db_dir) as conn:
            cursor = conn.cursor()
            query = "INSERT INTO users VALUES (?, ?, ?, ?)"
            cursor.execute(query, (email, username, password_hash, birthday))
            cursor.close()

    def register_user_and_get_info(self, email, username, password_hash, birthday):
        try:
            self.__store_user(email, username, password_hash, birthday)
            return self.get_user_by_email(email)
        except sqlite3.IntegrityError as e:
            if "users.email" in str(e):
                raise EmailAlreadyExistsError()
            elif "users.username" in str(e):
                raise UserAlreadyExistsError()
            raise e

    def _get_user_by_email(self, email):
        conn = sqlite3.connect(self.db_dir)
        query = "SELECT * FROM users WHERE email=?"
        cursor = conn.execute(query, (email,))
        user = cursor.fetchone()
        conn.close()
        if user is None:
            raise UserNotFoundError()
        return user

    def get_user_by_email(self, email):
        user = self._get_user_by_email(email)
        return dict(zip(self.users_headers, user))

    def get_users_headers(self):
        conn = sqlite3.connect(self.db_dir)
        query = "SELECT * FROM users where email = 1"
        cursor = conn.execute(query)
        headers = [description[0] for description in cursor.description]
        conn.close()
        return headers


class UserNotFoundError(Exception):
    pass


class UserAlreadyExistsError(Exception):
    pass


class EmailAlreadyExistsError(Exception):
    pass
