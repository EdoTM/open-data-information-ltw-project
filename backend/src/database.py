import os
import sqlite3
from utils.errors import *


def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


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

    def connect(self):
        conn = sqlite3.connect(self.db_dir)
        conn.row_factory = dict_factory
        return conn

    def __store_user(self, email, username, password_hash, birthday, profile_pic):
        query = "INSERT INTO users VALUES (?, ?, ?, ?, ?)"
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (email, username, password_hash, birthday, profile_pic))
            cursor.close()

    def register_user_and_get_info(self, email, username, password_hash, birthday, profile_pic):
        try:
            self.__store_user(email, username, password_hash, birthday, profile_pic)
            return self.get_user_by_email(email)
        except sqlite3.IntegrityError as e:
            if "users.email" in str(e):
                raise EmailAlreadyExists()
            elif "users.username" in str(e):
                raise UserAlreadyExists()
            raise e

    def get_user_by_email(self, email: str):
        query = "SELECT * FROM users WHERE email=?"
        with self.connect() as conn:
            cursor = conn.execute(query, (email,))
            user = cursor.fetchone()
            cursor.close()
        if user is None:
            raise UserNotFound()
        return user

    def get_posts_for_user(self, email: str):
        query = """
            select p.*, coalesce(sum(v.value), 0) as score, coalesce(v2.value, 0) as userVote
            from posts p left join votes v on p.id = v.post
                        left join votes v2 on p.id = v2.post and v2.email = ?
            group by p.id
        """
        with self.connect() as conn:
            cursor = conn.execute(query, (email,))
            posts = cursor.fetchall()
            cursor.close()
        return posts

    def get_posts_without_user(self):
        return self.get_posts_for_user("")

    def create_post(self, email: str, title: str, content: str, img: str):
        query = "INSERT INTO posts (author_email, title, content, img) VALUES (?, ?, ?, ?)"
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (email, title, content, img))
            cursor.close()

    def vote_post(self, email: str, post_id: int, value: int):
        query = """
        INSERT INTO votes (email, post, value)
        VALUES (?, ?, ?)
        ON CONFLICT(email, post) DO UPDATE SET value = ?
        """
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (email, post_id, value, value))
            cursor.close()
