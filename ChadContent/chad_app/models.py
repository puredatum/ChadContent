from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    brand_voice = db.Column(db.String(120))
    last_prompt = db.Column(db.String(120))
    last_response = db.Column(db.String(120))
    last_edit_prompt = db.Column(db.String(120))
    last_edit_response = db.Column(db.String(120))
    response_list = db.relationship("ChadResponse")
    api_list = db.relationship("APITokens")
    keyword_list = db.relationship("KeywordList")


class ChadResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chad_prompt = db.Column(db.String())
    chad_response = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class APITokens(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    api_key = db.Column(db.String(120))
    org_id = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class KeywordList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keywords = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))