from db.database import db
import enum
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, DECIMAL, JSON, ForeignKey, Enum
from sqlalchemy.orm import relationship


class Role(enum.Enum):
    BASIC = 'BASIC'
    ADMIN = 'ADMIN'


class User(db.Model):
    __tablename__ = 'scraped_urls'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    bids = db.relationship('Bid', backref='user', lazy=True)
    role = db.Column(Enum(Role), nullable=False)


class AuctionItem(db.Model):
    __tablename__ = 'scraped_urls'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    starting_price = db.Column(db.Float, nullable=False)
    current_price = db.Column(db.Float, nullable=False, default=0.0)
    bids = db.relationship('Bid', backref='auction_item', lazy=True)


class Bid(db.Model):
    __tablename__ = 'scraped_urls'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    auction_item_id = db.Column(db.Integer, db.ForeignKey(
        'auction_item.id'), nullable=False)


class AuctionItemImages(db.Model):
