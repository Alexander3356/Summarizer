from sqlalchemy import func
from werkzeug.security import check_password_hash, generate_password_hash

from models.conn import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(260), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())

    summaries = db.relationship(
        'Summary',
        back_populates='user',
        cascade='all, delete-orphan'
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)



class Summary(db.Model):
    __tablename__ = 'summary'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', ondelete='CASCADE'),
        nullable=False
    )
    title = db.Column(db.String(150), nullable=False)
    original_text = db.Column(db.Text, nullable=False)
    summary_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())

    user = db.relationship('User', back_populates='summaries')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'original_text': self.original_text,
            'summary_text': self.summary_text,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
