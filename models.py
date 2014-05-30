from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class BlockageReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blocked_url = db.Column(db.String(200), nullable=False)
    reported_from_addr = db.Column(db.String(100), nullable=False)
    landing_url = db.Column(db.String(200))
    reported_at = db.Column(db.DateTime, nullable=False)

    title = db.Column(db.String(200))
    observed_at = db.Column(db.DateTime)
    accessing_from = db.Column(db.String(200))
    comments = db.Column(db.Text)

    def __init__(self, blocked_url, reported_from_addr, reported_at=None):
        self.blocked_url = blocked_url
        self.reported_from_addr = reported_from_addr
        if reported_at:
            self.reported_at = reported_at
        else:
            self.reported_at = datetime.now()

    def __repr__(self):
        return '<URL: %s >' % self.blocked_url

    
