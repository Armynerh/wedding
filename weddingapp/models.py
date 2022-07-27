from datetime import datetime
from weddingapp import db 


class Guests(db.Model): 
    guest_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    guest_fname =db.Column(db.String(50), nullable=False)
    guest_lname =db.Column(db.String(50), nullable=False)
    guest_email=db.Column(db.String(80), nullable=False)
    guest_image= db.Column(db.String(80), nullable=False)
    guest_pwd =db.Column(db.String(100), nullable=False)
    guest_address =db.Column(db.String(255), nullable=True)
    guest_regdate=db.Column(db.DateTime(), default=datetime.utcnow())
    
	
class Gifts(db.Model): 
    gift_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    gift_name =db.Column(db.String(50), nullable=False) 

class Admin(db.Model):
    #columname=db.Column(db.datatype())
    admin_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    admin_name =db.Column(db.String(50), nullable=False)
    admin_username =db.Column(db.String(50), nullable=False)
    admin_pwd =db.Column(db.String(30), nullable=False)
    

class Uniform(db.Model):
    #columname=db.Column(db.datatype())
    uni_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    uni_name =db.Column(db.String(50), nullable=False)
    uni_price =db.Column(db.Float(), nullable=False)

class Guest_gift(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g_giftid = db.Column(db.Integer(), db.ForeignKey('gifts.gift_id'))
    g_guestid =db.Column(db.Integer(), db.ForeignKey('guests.guest_id')) 

    #set relationship
    #Relationship 1: When I am on Gifts table and want to know the guests that brought a particular gift, I will check inside variable 'dguests', when I am on this table (Guest_gift) and I want to know the details of a gift, I can check gift_deets.
    
    #Relationship 2: When I am on Guests table and I want to know the gifts brought by a particular guest, I will see it via variable 'dgifts' and When I am on this table (Guest_gift) and I want to know the details of a particular Guest, I will check guest_deets  
    gift_deets = db.relationship("Gifts", backref="dguests")
    guest_deets = db.relationship("Guests", backref="dgifts")

class Contact(db.Model):
    con_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    con_fullname= db.Column(db.String(50), nullable=True)
    con_email = db.Column(db.String(50), nullable=True)
    con_message = db.Column(db.Text(),nullable=True )
    con_date = db.Column(db.DateTime(), default=datetime.utcnow())
class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment_guestid=db.Column(db.Integer(), db.ForeignKey('guests.guest_id')) 
    comment_content = db.Column(db.String(255), nullable=True)
    comment_date = db.Column(db.DateTime(), default=datetime.utcnow())
    
    comdeets= db.relationship("Guests", backref="guestcom")
class Lga(db.Model):
    lga_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    state_id=db.Column(db.Integer(), db.ForeignKey('state.state_id')) 
    lga_name = db.Column(db.String(50), nullable=True)
class State(db.Model):
    state_id=db.Column(db.Integer(), primary_key=True, autoincrement=True)
    state_name = db.Column(db.String(50), nullable=True)
    