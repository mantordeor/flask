from registerdb import db
from sqlalchemy import Column, Integer, String, ARRAY
import json

class UserMixin(object):
    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return str(self.id)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')
        
class UserReister(UserMixin, db.Model):
    __tablename__ = 'UserRegisters'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    item_bought_id = db.Column(db.String(500), nullable=True, default='')
    def serialize(self):
        return{"id":self.id,
                "username":self.username,
                "email":self.email,
                "password":self.password
        }
    def add_item_bought(self, item_id):
        item_bought_list = json.loads(self.ITEM_BOUGHT) if self.ITEM_BOUGHT else []
        item_bought_list.append(item_id)
        self.ITEM_BOUGHT = json.dumps(item_bought_list)

    def get_item_bought(self):
        return json.loads(self.ITEM_BOUGHT) if self.ITEM_BOUGHT else []
    def check_password(self, password):
        return self.password == password
    
class Product(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key = True)
    item_name = db.Column(db.String(80),unique=True,nullable=False)
    item_price = db.Column(db.Integer,unique=True,nullable=False)