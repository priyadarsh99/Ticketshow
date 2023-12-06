from .database import db 
# creation of the models to integrate the tables in database to python for use via sqlalchemy
class User(db.Model): #for table user
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    username = db.Column(db.String, unique = True)
    password = db.Column(db.String)
    email = db.Column(db.String)
    is_admin = db.Column(db.Integer)

class Theatre(db.Model): #for table theatre
    __tablename__ = 'theatre'
    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    name = db.Column(db.String,unique = True)
    location = db.Column(db.String)
    place = db.Column(db.String)
    capacity = db.Column(db.Integer)
    def serialize(self):
        return{
        "id": self.id,
        "name": self.name,
        "location": self.location,
        "place": self.place,
        "capacity":self.capacity
        }
    
class Show(db.Model): #for table show
    __tablename__ = 'show'
    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    showname = db.Column(db.String)
    ratings = db.Column(db.Numeric)
    tags = db.Column(db.String)
    price = db.Column(db.Integer)
    theatre_id = db.Column(db.Integer, db.ForeignKey('theatre.id'))
    time = db.Column(db.String)
    counts = db.Column(db.Integer)
    capacity = db.Column(db.Integer)
    def serialize(self):
        return{
        "id": self.id,
        "showname": self.showname,
        "ratings": self.ratings,
        "tags": self.tags,
        "price":self.price,
        "theatre_id": self.theatre_id,
        "time": self.time,
        "capacity":self.capacity
        }
    

class Booking(db.Model): #for table booking
    __tablename__ = 'booking'
    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    show_id = db.Column(db.Integer, db.ForeignKey('show.id'))
    theatre_id = db.Column(db.Integer, db.ForeignKey('theatre.id'))
    count = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class BookingList(): #class used to serialize the bookings 

    def serialize(self):
        return{
        "id": self.id,
        "theatre_id": self.theatre_id,
        "show_id": self.show_id,
        "theatre_name": self.theatre_name,
        "show_name":self.show_name,
        "timing": self.timing
        }