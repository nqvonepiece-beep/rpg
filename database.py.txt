# database.py - Lưu và tải dữ liệu người chơi

import json
import os

DATA_FILE = "players.json"

class Database:
    def __init__(self):
        self.data = {}
        self.load()

    def load(self):
        """Tải dữ liệu từ file"""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except:
                self.data = {}
        else:
            self.data = {}

    def save(self):
        """Lưu dữ liệu vào file"""
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def get_player(self, user_id):
        """Lấy dữ liệu người chơi"""
        return self.data.get(str(user_id))

    def save_player(self, user_id, char_data):
        """Lưu dữ liệu người chơi"""
        self.data[str(user_id)] = char_data
        self.save()

    def delete_player(self, user_id):
        """Xóa nhân vật"""
        if str(user_id) in self.data:
            del self.data[str(user_id)]
            self.save()
            return True
        return False

    def get_all_players(self):
        """Lấy tất cả người chơi (cho leaderboard)"""
        return self.data

    def has_player(self, user_id):
        """Kiểm tra người chơi có nhân vật chưa"""
        return str(user_id) in self.data
