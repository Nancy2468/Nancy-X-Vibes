from database import Database

class MemberManager:
    def __init__(self):
        self.database = Database()

    def add_member(self, user_id, name, date_of_birth=None):
        self.database.add_member(user_id, name, date_of_birth)

    def remove_member(self, user_id):
        self.database.remove_member(user_id)

    def get_member_info(self, user_id):
        return self.database.get_member(user_id)