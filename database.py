import sqlite3
from config import DATABASE_FILE

class Database:
    def __init__(self):
        self.connection = sqlite3.connect(DATABASE_FILE)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS playlist
                               (id INTEGER PRIMARY KEY, group_id INTEGER, song TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS members
                               (id INTEGER PRIMARY KEY, user_id INTEGER, name TEXT, date_of_birth TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS settings
                               (group_id INTEGER PRIMARY KEY, auto_stop_enabled INTEGER, 
                               ask_resume_enabled INTEGER, admin_only INTEGER)''')
        self.connection.commit()

    def add_song(self, group_id, song):
        self.cursor.execute('INSERT INTO playlist (group_id, song) VALUES (?, ?)', (group_id, song))
        self.connection.commit()

    def remove_song(self, group_id, song_id):
        self.cursor.execute('DELETE FROM playlist WHERE group_id = ? AND id = ?', (group_id, song_id))
        self.connection.commit()

    def get_playlist(self, group_id):
        self.cursor.execute('SELECT id, song FROM playlist WHERE group_id = ?', (group_id,))
        return self.cursor.fetchall()

    def update_song(self, group_id, song_id, new_song):
        self.cursor.execute('UPDATE playlist SET song = ? WHERE group_id = ? AND id = ?', (new_song, group_id, song_id))
        self.connection.commit()

    def add_member(self, user_id, name, date_of_birth):
        self.cursor.execute('INSERT INTO members (user_id, name, date_of_birth) VALUES (?, ?, ?)',
                            (user_id, name, date_of_birth))
        self.connection.commit()

    def remove_member(self, user_id):
        self.cursor.execute('DELETE FROM members WHERE user_id = ?', (user_id,))
        self.connection.commit()

    def get_member(self, user_id):
        self.cursor.execute('SELECT name, date_of_birth FROM members WHERE user_id = ?', (user_id,))
        return self.cursor.fetchone()

    def set_group_setting(self, group_id, setting, value):
        self.cursor.execute('REPLACE INTO settings (group_id, {0}) VALUES (?, ?)'.format(setting), (group_id, value))
        self.connection.commit()

    def get_group_setting(self, group_id, setting):
        self.cursor.execute('SELECT {0} FROM settings WHERE group_id = ?'.format(setting), (group_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None
