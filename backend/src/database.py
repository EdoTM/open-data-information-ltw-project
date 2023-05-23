import datetime
import os
import sqlite3
from utils.errors import *

wg_whitelist = ["All", "CT", "OP", "PCG", "RAN", "SA", "CT 1", "CT 3", "CT 4", "CT 6", "RAN 1", "RAN 2", "RAN 3", "RAN 4", "RAN 5", "SA 1", "SA 2", "SA 3", "SA 4", "SA 5", "SA 6"]

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
        self.db_data_dir = os.path.join(os.path.dirname(__file__), '../db/3gppdata.db')

    def connect(self):
        conn = sqlite3.connect(self.db_dir)
        conn.row_factory = dict_factory
        return conn
    
    def connect_data(self, row_factory=dict_factory):
        conn = sqlite3.connect(self.db_data_dir)
        conn.row_factory = row_factory
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
            select p.*, coalesce(sum(v.value), 0) as score, coalesce(v2.value, 0) as userVote, coalesce(f.starred, 0) as starred, coalesce(h.hidden, 0) as hidden
            from posts p left join votes v on p.id = v.post
            left join votes v2 on p.id = v2.post and v2.email = ?
            left join favorites f on p.id = f.post and f.email = ?
            left join hidden h on p.id = h.post and h.email = ?
            where h.hidden = 0 or h.hidden is null
            group by p.id
            order by p.timestamp desc
        """
        with self.connect() as conn:
            cursor = conn.execute(query, (email,email,email))
            posts = cursor.fetchall()
            cursor.close()
        return posts
    
    def get_favorite_posts_for_user(self, email: str):
        query = """
            select p.*, coalesce(sum(v.value), 0) as score, coalesce(v2.value, 0) as userVote, coalesce(f.starred, 0) as starred, coalesce(h.hidden, 0) as hidden
            from posts p left join votes v on p.id = v.post
            left join votes v2 on p.id = v2.post and v2.email = ?
            left join favorites f on p.id = f.post and f.email = ?
            left join hidden h on p.id = h.post and h.email = ?
            where f.starred = 1
            group by p.id
            order by p.timestamp desc
        """
        with self.connect() as conn:
            cursor = conn.execute(query, (email,email,email))
            posts = cursor.fetchall()
            cursor.close()
        return posts
    
    def get_hidden_posts_for_user(self, email: str):
        query = """
            select p.*, coalesce(sum(v.value), 0) as score, coalesce(v2.value, 0) as userVote, coalesce(f.starred, 0) as starred, coalesce(h.hidden, 0) as hidden
            from posts p left join votes v on p.id = v.post
            left join votes v2 on p.id = v2.post and v2.email = ?
            left join favorites f on p.id = f.post and f.email = ?
            left join hidden h on p.id = h.post and h.email = ?
            where h.hidden = 1
            group by p.id
            order by p.timestamp desc
        """
        with self.connect() as conn:
            cursor = conn.execute(query, (email,email,email))
            posts = cursor.fetchall()
            cursor.close()
        return posts

    def get_posts_without_user(self):
        return self.get_posts_for_user("")

    def create_post(self, email: str, title: str, content: str, img: str):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = "INSERT INTO posts (author_email, title, content, img, timestamp) VALUES (?, ?, ?, ?, ?)"
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (email, title, content, img, timestamp))
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

    def count_meetings(self, index, wg):
        if index not in ["nation", "company"]:
            raise InvalidIndex()
        if wg not in wg_whitelist:
            raise InvalidFilterKey()
        if wg == "All":
            wg = "' OR '1'='1"
        query = f"""
            SELECT attendee.{index}, count(*) as cnt
            FROM AttendeesParticipation attendee JOIN Meetings meeting 
            ON attendee.meeting_id = meeting.meeting_id
            WHERE meeting.wg = '{wg}'
            GROUP BY attendee.{index}
        """
        with self.connect_data() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            meetings = cursor.fetchall()
            cursor.close()
        return meetings
    
    def count_tdocs(self, index, tdoc_status):
        if index not in ["nation", "company"]:
            raise InvalidIndex()
        if tdoc_status == 'all':
            tdoc_status = ('agreed','approved','withdrawn','rejected','not concluded','not pursued')
        elif tdoc_status == 'accepted':
            tdoc_status = ('agreed','approved')
        elif tdoc_status == 'rejected':
            tdoc_status = ('withdrawn','rejected','not concluded','not pursued')
        else:
            raise InvalidFilterKey()

        query = f"""
            SELECT attendee.{index}, count(*) as cnt
            FROM AttendeesParticipation attendee JOIN Tdocs tdocs 
            ON attendee.meeting_id = tdocs.meeting_id
            AND tdocs.contact_id = attendee.person_id
            WHERE tdocs.type = 'CR'
            AND tdocs.tdoc_status in {tdoc_status}
            GROUP BY attendee.{index}
            """
        with self.connect_data() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            tdocs = cursor.fetchall()
            cursor.close()
        return tdocs
    
    def get_all_nations(self):
        query = """
            SELECT DISTINCT nation
            FROM AttendeesParticipation
        """
        with self.connect_data() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            nations = cursor.fetchall()
            cursor.close()
        return nations
    
    def get_all_companies(self):
        query = """
            SELECT DISTINCT company
            FROM AttendeesParticipation
        """
        with self.connect_data() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            companies = cursor.fetchall()
            cursor.close()
        return companies

    def star_post(self, email, post, starred):
        query = """
            INSERT INTO favorites (email, post, starred)
            VALUES (?, ?, ?)
            ON CONFLICT(email, post) DO UPDATE SET starred = ?
        """
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (email, post, int(starred), int(starred)))
            cursor.close()

    def hide_post(self, email, post, hidden):
        query = """
            INSERT INTO hidden (email, post, hidden)
            VALUES (?, ?, ?)
            ON CONFLICT(email, post) DO UPDATE SET hidden = ?
        """
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (email, post, int(hidden), int(hidden)))
            cursor.close()

    def comment(self, email, post, content):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = "INSERT INTO comments (email, post, content, timestamp) VALUES (?, ?, ?, ?)"
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (email, post, content, timestamp))
            cursor.close()

    def get_comments_for_post(self, post_id):
        query = """
            select u.username, c.content, c.timestamp
            from comments c join users u on c.email = u.email
            where c.post = ?
            order by c.timestamp asc
        """
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (post_id,))
            comments = cursor.fetchall()
            cursor.close()
        return comments
        
    
    