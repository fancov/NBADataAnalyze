from db import db


class NBA(db.Model):
    __tablename__ = 'nba'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    year_time = db.Column(db.VARCHAR(16))
    store_time = db.Column(db.VARCHAR(16))
    team_info = db.Column(db.Text)
