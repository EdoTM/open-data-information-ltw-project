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
        self.users_headers = self.__get_users_headers()

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

    def get_user_by_email(self, email):
        with sqlite3.connect(self.db_dir) as conn:
            query = "SELECT * FROM users WHERE email=?"
            cursor = conn.execute(query, (email,))
            user = cursor.fetchone()
            cursor.close()
        if user is None:
            raise UserNotFoundError()
        return dict(zip(self.users_headers, user))

    def __get_users_headers(self):
        with sqlite3.connect(self.db_dir) as conn:
            query = "SELECT * FROM users where email = 1"
            cursor = conn.execute(query)
            headers = [description[0] for description in cursor.description]
            cursor.close()
        return headers


class UserNotFoundError(Exception):
    pass


class UserAlreadyExistsError(Exception):
    pass


class EmailAlreadyExistsError(Exception):
    pass
